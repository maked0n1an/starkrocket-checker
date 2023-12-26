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
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url,
                                    params=params, proxy=self.proxy) as response:
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

