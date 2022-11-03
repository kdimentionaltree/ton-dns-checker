# from dnschecker.core.checker import DHTChecker
# from collections import Counter
# import time
# import sys


# if __name__ == "__main__":
#     checker = DHTChecker('/run/secrets/config', 
#                          resolve_binary_path='/app/binaries/dht-resolve', 
#                          ping_binary_path='/app/binaries/dht-ping-servers', 
#                          port=32768)

#     while True:
#         adnl = '2D7CF7C6238E4E8B7DA16B0707222C3A95C8DB6A8E4FA4F101052306130EEFDC'
#         res1 = checker.check_adnl(adnl, timeout=10, verbose=False)
        
#         counter = Counter(res1.values())
#         print(counter)
#         sys.stdout.flush()

#         time.sleep(0.5)
