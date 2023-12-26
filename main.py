import asyncio
import random

from data.checker import Checker
from data.writer import Writer
from utils.config import WALLETS, PROXIES
from settings import RANDOM_WALLETS

def zip_to_table():
    wallet_dict = {
        pair: proxy for pair, proxy in zip(WALLETS, PROXIES * len(WALLETS))
    }
    
    return wallet_dict

def format_output(message: str):
    print(f"{message:^80}")

def greetings():
    brand_label = "========== M A K E D 0 N 1 A N =========="
    name_label = "========= StarkRocket Checker ========="
    
    print("")
    format_output(brand_label)
    format_output(name_label)

async def main():
    greetings()
    
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
    
    exit_label = "========= It's all! ========="
    format_output(exit_label)