import json
import aiohttp

from data.wallet import Wallet


class Checker(Wallet):
    def __init__(self, order_number: int, wallet: str, proxy=None):
        super().__init__(order_number, wallet)
        self.proxy = proxy
        
    async def check_for_eligibility(self) -> (str, int):
        url = "https://starkrocket.xyz/api/check_wallet"
        params = {
            'address': self.address
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru,en;q=0.9,ru-RU;q=0.8,zh-TW;q=0.7,zh;q=0.6',
            'Connection': 'keep-alive',
            'Referer': 'https://starkrocket.xyz/airdrop',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url,
                                    params=params, headers=headers,proxy=self.proxy) as response:
                    if response.status == 200:
                        return await self._get_json(response)        
                    else:
                        print(f"{self.order_number:4} | {self.address:68} | Failed with status code: {response.status}")           
        except aiohttp.ClientError as e:
            self.format_display(f"An error occured: {e}")
            
        return self.order_number, self.address, 0
      
    async def _get_json(self, response: aiohttp.ClientSession) -> (str, int):
        try:    
            drop = await response.json()
            points = drop['result']['points']
            self.format_display(f"{points}")
            
            return self.address, points
        except json.JSONDecodeError:
            self.format_display("Cannot unpacked JSON, problem with connection etc.")
            
            return self.order_number, self.address, 0

