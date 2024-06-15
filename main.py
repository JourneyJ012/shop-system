import csv
from os import system
from datetime import time
class Shop:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            item_list = []
            for row in reader:
                if len(row) != 5:
                    continue
                name, num_in_stock, original_price, num_sold, current_discount_percentage = row
                item_list.append(Item(str(name), int(num_in_stock), float(original_price), int(num_sold), float(current_discount_percentage)))
            self.item_list = item_list
    

    

class Item:
    def __init__(self, name: str, num_in_stock: int, ORIGINAL_PRICE: float, num_sold: int, current_discount_percentage: float) -> None:


        if type(num_in_stock) != int or type(ORIGINAL_PRICE) != float or type(num_sold) != int or type(current_discount_percentage) != float:
            raise TypeError("Malformed inputs! num in stock should be int, original price should be a float, num sold should be int, and current discount should be float!")
            

        self.name = name
        self.ORIGINAL_PRICE = round(ORIGINAL_PRICE, 2)
        self.current_discount_percentage = current_discount_percentage
        while True:
            if num_in_stock > -1:
                self.num_in_stock = num_in_stock
                confirmed_1 = True
            if num_sold > -1:
                self.num_sold = num_sold
                confirmed_2 = True
            if confirmed_1 and confirmed_2:
                break
            
        

        
    def __str__(self) -> str:
        return f"""Name: {self.name}, Stock: {self.num_in_stock}, Price: £{self.ORIGINAL_PRICE}, Sold: {self.num_sold}, discount: {self.current_discount_percentage}"""

    def item_sold(self) -> bool:
        self.num_in_stock -= 1
        self.num_sold += 1
        print(f"{self.name} sold! {self.num_in_stock} left!")

    def calculate_revenue(self):
        return self.num_sold * self.ORIGINAL_PRICE #TODO: change this to work with percentage discounts!
    

def handle_input(user_input: str):
    if user_input == "clear shell":
        system('ctl')
    elif user_input == "ls" or user_input == "list":
        for item in shop.item_list:
            print(item)
    elif user_input == "Apply discount": #TODO: change item data, do different elifs for discounts etc, and then for showing discounts, new prices, blah blah blah 
        discounted_item = str(input("Which item do you want to apply the discount to?"))
        if discounted_item in Shop.item_list:
            ...

if __name__ == "__main__":
    shop = Shop("items.csv")
    while True:
        handle_input(str(input()).lower())