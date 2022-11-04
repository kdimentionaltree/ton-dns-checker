import subprocess
import base64
import struct
import socket
import json
import time

from tqdm.auto import tqdm
from functools import partial
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from threading import Thread

from dnschecker.schemas.dht import DHTNode


class DHTChecker:
    def __init__(self, 
                 config_path, 
                 resolve_binary_path,
                 ping_binary_path,
                 port=32768,
                 timeout=10):
        self.config_path = config_path
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

        self.resolve_binary_path = resolve_binary_path
        self.ping_binary_path = ping_binary_path
        self.port = port
        self.timeout = timeout

        self.dht_list = {idx: DHTNode.parse_obj(dht) for idx, dht in enumerate(self.config['dht']['static_nodes']['nodes'])}
        self.dht_dict = {dht.id.key: idx for idx, dht in self.dht_list.items()}
        self.working_status = {idx: False for idx in self.dht_list}
        
        self.ping_thread = Thread(target=self._ping_loop)
        self.ping_thread.start()

    def _ping_loop(self):
        while True:
            cmd = [self.ping_binary_path, 
                   '-C', self.config_path,
                   '-p', f"{self.port}",
                   '-v', '0']
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
                lines = [line for line in p.stdout if ' : ' in line]
                for idx, line in enumerate(lines):
                    try:
                        res = line.split(' ')
                        key = res[0]
                        # print(key, base64.b64decode(key.encode('utf-8')).decode('utf-8'))
                        is_online = int(res[2].split('/')[0]) > 0
                        self.working_status[idx] = is_online
                    except Exception as ee:
                        print(ee, line)
            time.sleep(10)

    @property
    def dht_status(self):
        return [(idx, dht, self.working_status[idx]) for idx, dht in self.dht_list.items()]

    def _check_adnl(self, adnl, idx, port=None, timeout=10):
        if self.working_status[idx]:
            if port is None:
                port = self.port + idx + 1
            
            adnl_hex = bytes.fromhex(adnl)
            adnl_b64 = base64.b64encode(adnl_hex).decode('utf-8')
            
            cmd = [self.resolve_binary_path, 
                "--global-config", f"{self.config_path}", 
                "--server-idx", f"{idx}",
                "--verbosity", "0",
                "--port", f"{port}",
                "--key-name", "address",
                "--key-idx", "0",
                "--key-id", f'{adnl_b64}',
                "--timeout", f"{timeout}"]
            # print(' '.join(cmd))
            try:
                with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
                    for line in p.stdout:
                        if line.startswith('VALUE: '):
                            res = line.split(' ')[-1]
                            res = base64.b64decode(res)
                ip_int, port = struct.unpack('ih', res[12:12 + 4 + 2])
                ip = socket.inet_ntoa(struct.pack('>i', ip_int))
                return idx, {'ip': ip, 'ip_int': ip_int, 'port': port}
            except:
                pass
        return idx, {}

    @property
    def dht_count(self):
        return len(self.config['dht']['static_nodes']['nodes'])

    def check_adnl_parallel(self, adnl):
        func = partial(self._check_adnl, adnl, timeout=self.timeout)
        with ThreadPool(self.dht_count) as P:
            res = P.map(func, range(self.dht_count))
        return dict(sorted(res))

    def check_adnl(self, adnl):
        return self.check_adnl_parallel(adnl)
    
    # def check_adnl_seq(self, adnl, verbose=True, timeout=5):
    #     return dict(self._check_adnl(adnl, idx, port=self.port + 1, timeout=timeout) 
    #                 for idx in tqdm(range(self.dht_count), disable=not verbose))
