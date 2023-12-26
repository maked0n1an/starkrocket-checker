import csv

from data.wallet import Wallet
from utils.helpers import format_output

total_point = 0

class Writer(Wallet):
    def __init__(self, order_number: int, address: str):
        super().__init__(order_number, address)
    
    async def write_to_csv(self, points: int):
        with open('results/result.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            if file.tell() == 0:
                writer.writerow(['order_number', 'address', 'amount_of_points'])
            
            writer.writerow([self.order_number, self.address, points])
    
    @staticmethod
    def write_total_result(total_points: int):
        with open('results/result.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            format_output(f"Total points: {total_points}")            
            writer.writerow(['total_amount', total_points])            