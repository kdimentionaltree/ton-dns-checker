import base64
import struct

from hashlib import sha256
from tvm_valuetypes import Cell
from tvm_valuetypes import deserialize_boc
from pytonlib.utils.tlb import Slice
from pytonlib.utils.address import detect_address
from bitarray import bitarray
from bitarray.util import ba2int

from typing import Iterable

# Encode domain name to a format suitable for blockchain queries.
def encode_domain(domain):
    if not domain:
        raise ValueError('empty domain')

    domain = domain.lower()
    # Check for invalid characters in the domain name.
    for ch in domain:
        code = ord(ch)
        if code <= 32 or (code >= 127 and code <= 159):
            raise ValueError('Invalid characters in domain names')

    # Split the domain and check for empty components.
    domain_arr = domain.split('.')
    for part in domain_arr:
        if not part:
            raise ValueError('domain name cannot have an empty component')

    # Encode the domain in reverse order, separated by null characters.
    raw_domain = '\0'.join(domain_arr[::-1]) + '\0'
    if len(raw_domain) < 126:
        raw_domain = '\0' + raw_domain
    return raw_domain.encode()
    

# Convert the raw domain into a cell and serialize it into Base64.
def domain_to_cell(raw_domain):
    cell = Cell()
    cell.data.from_bytes(raw_domain)
    boc = cell.serialize_boc(False)
    return base64.b64encode(boc).decode('utf-8')


# Encode the category into a numeric hash.
def encode_category(category):
    category_bytes = category.encode()
    category_hash = sha256(category_bytes)
    category_bn = int(category_hash.hexdigest(), base=16)
    return f"{category_bn}"


# Parse a stack item from the response.
def parse_stack_item(item):
    tp, val = item
    if tp == 'num':
        return int(val, base=16)
    elif tp in ['list', 'tuple']:
        raise NotImplementedError('parsing of list and tuple is not implemented')
    elif tp == 'cell':
        content = base64.b64decode(val['bytes'])
        return deserialize_boc(content)
    else:
        raise ValueError(f"unknown type '{tp}'")


# Parse the entire stack.
def parse_stack(stack):
    return [parse_stack_item(item) for item in stack]


# Parse a cell to extract the smart contract address.
def _parse_smart_contract_address(cell, prefix0, prefix1):
    s = Slice(cell)
    # Check for valid prefixes in the cell data.
    p0 = s.read_next(8)
    p1 = s.read_next(8)
    if not (ba2int(p0) == prefix0 and ba2int(p1) == prefix1):
        raise RuntimeError('Invalid dns record value prefix')
    _ = s.read_next(3)
    n = ba2int(s.read_next(8))
    if n > 127:
        n -= 256
    hs = ba2int(s.read_next(256))
    addr = detect_address(f'{n}:{hs:x}')
    return addr


# Parse the cell to extract the next resolver record.
def parse_next_resolver_record(cell):
    return _parse_smart_contract_address(cell, 0xba, 0x93)


# Parse the cell to extract the smart contract address record.
def parse_smart_contract_address_record(cell):
    return _parse_smart_contract_address(cell, 0x9f, 0xd3)


# Parse the cell to extract the ADNL address record.
def parse_adnl_address_record(cell):
    s = Slice(cell)
    p0 = s.read_next(8)
    p1 = s.read_next(8)
    if not (ba2int(p0) == 0xad and ba2int(p1) == 0x01):
        raise RuntimeError(f'Invalid dns record value prefix: {p0}, {p1}')
    adnl = s.read_next(256)
    return f"{ba2int(adnl):x}".upper()


# The main function to perform the resolution of a domain.
async def _resolve_impl(tonlib, address, domain_raw, category, one_step=False):
    # Encode the category and prepare the request parameters.
    category_raw = encode_category(category)
    domain_raw_len = len(domain_raw) * 8
    domain_cell = domain_to_cell(domain_raw)
    
    # Execute the 'dnsresolve' method on the blockchain.
    res = await tonlib.raw_run_method(address, 
                                      'dnsresolve',
                                      [['tvm.Slice', domain_cell],
                                       ['num', category_raw]])
    stack = parse_stack(res['stack'])

    # Validate the response.
    if len(stack) != 2:
        raise RuntimeError('invalid dnsresolve response')
        
    result_len, cell = stack
    # Handle empty cell cases.
    if isinstance(cell, Iterable) and len(cell) == 0:
        cell = None
        
    if not isinstance(cell, Cell):
        raise RuntimeError('invalid dnsresolve response')
        
    if result_len == 0:
        return None
    
    # Validate result length.
    if result_len % 8 != 0:
        raise RuntimeError('domain split not at a component boundary')

    if result_len > domain_raw_len:
        raise RuntimeError(f'invalid response {result_len}/{domain_raw_len}')
    elif result_len == domain_raw_len:
        # Based on the category, parse the cell to get the required record.
        if category == 'dns_next_resolver':
            return parse_next_resolver_record(cell) if cell else None
        elif category == 'wallet':
            return parse_smart_contract_address_record(cell) if cell else None
        elif category == 'site':
            return parse_adnl_address_record(cell) if cell else None
        else:
            return cell
    else:
        if cell is None:
            return None
        # Get the address of the next resolver and perform a recursive resolution if required.
        next_address = parse_next_resolver_record(cell)
        if one_step:
            if category == 'dns_next_resolver':
                return next_address
            return None
        return await _resolve_impl(tonlib, next_address['raw_form'], domain_raw[result_len//8:], category, one_step=one_step)
    return
