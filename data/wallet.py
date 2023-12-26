class Wallet:
    def __init__(self,order_number: int, address: str):
        self.order_number = order_number
        self.address = address.lower()
    
    def format_display(self, message):
        print(f"{self.order_number:4} | {self.address:68} | {message} |")