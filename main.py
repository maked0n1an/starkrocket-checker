import asyncio
import random

from data.checker import Checker
from data.writer import Writer
from utils.config import WALLETS, PROXIES
from settings import RANDOM_WALLETS, USE_PROXIES

def zip_to_table():
    wallet_dict = { 
        index: wallet for wallet, index in enumerate(WALLETS)
    }
    
    if USE_PROXIES:           
        # wallet_dict = { 
        #     str(key): proxy for (_, key), proxy in zip(wallet_dict.items(), PROXIES * len(WALLETS)) 
        # }
        
        wallet_dict = {
            pair: proxy for pair, proxy in zip(WALLETS, PROXIES * len(WALLETS))
        }
    
    return wallet_dict

async def main():
    print("===========")
    print("===START===")
    
    tuples = zip_to_table()
        
    if RANDOM_WALLETS:
        items = list(tuples.items())
        random.shuffle(items)
        tuples = dict(items)   
            
    tasks = []
    
    for i, (wallet, proxy) in enumerate(tuples.items(), 1):
        checker = Checker(i, wallet, proxy)
        tasks.append(checker.check_for_eligibility())
           
    result = await asyncio.gather(*tasks)
    
    for i, (wallet, drop) in enumerate(result, 1):
        writer = Writer(i, wallet)
        await writer.write_to_csv(drop)


if __name__ == "__main__":
    asyncio.run(main())
    print("It's all!")