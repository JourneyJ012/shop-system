import csv
from os import system
import platform
from datetime import datetime


class Item:
    def __init__(self, name: str, num_in_stock: int, ORIGINAL_PRICE: float, num_sold: int, current_discount_percentage: float) -> None:
        if type(num_in_stock) != int or type(ORIGINAL_PRICE) != float or type(num_sold) != int or type(current_discount_percentage) != float:
            raise TypeError("Malformed inputs! num in stock should be int, original price should be a float, num sold should be int, and current discount should be float!")

        self.name = name
        self.num_in_stock = num_in_stock if num_in_stock > -1 else 0
        self.ORIGINAL_PRICE = round(ORIGINAL_PRICE, 2)
        self.num_sold = num_sold if num_sold > -1 else 0
        self.current_discount_percentage = current_discount_percentage

    def __str__(self) -> str:
        return f"Name: {self.name}, Stock: {self.num_in_stock}, Price: £{self.ORIGINAL_PRICE}, Sold: {self.num_sold}, Discount: {self.current_discount_percentage}%"

    def __repr__(self) -> str:
        return str(self.dictify())



    def dictify(self) -> dict:
        return {
            "Name": self.name,
            "Stock": self.num_in_stock,
            "Price": self.ORIGINAL_PRICE,
            "Sold": self.num_sold,
            "Discount": self.current_discount_percentage
        }

    def item_sold(self) -> bool:
        if self.num_in_stock > 0:
            self.num_in_stock -= 1
            self.num_sold += 1
            print(f"{self.name} sold! {self.num_in_stock} left!")
            return True
        else:
            print(f"{self.name} is out of stock!")
            return False

    def calculate_revenue(self):
        discount_multiplier = (100 - self.current_discount_percentage) / 100
        discounted_price = self.ORIGINAL_PRICE * discount_multiplier
        return self.num_sold * discounted_price

    def update_discount(self, discount: float):
        if 0.0 <= discount <= 100.0:
            self.current_discount_percentage = discount
            print(f"Discount for {self.name} updated to {self.current_discount_percentage}%")
        else:
            print("Invalid discount percentage. Must be between 0 and 100.")

class Shop:
    def __init__(self, items_path: str, sales_path):
        self.items_path = items_path 
        self.sales_path = sales_path
        with open(items_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            item_list = []

            for row in reader:
                if len(row) != 5:
                    continue
                name, num_in_stock, ORIGINAL_PRICE, num_sold, current_discount_percentage = row
                item_list.append(Item(str(name), int(num_in_stock), float(ORIGINAL_PRICE), int(num_sold), float(current_discount_percentage)))
            self.item_list = item_list

    def save(self):
        try:
            with open(self.items_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'num_in_stock', 'ORIGINAL_PRICE', 'num_sold', 'current_discount_percentage'])
                for item in self.item_list:
                    writer.writerow([
                        item.name,
                        item.num_in_stock,
                        item.ORIGINAL_PRICE,
                        item.num_sold,
                        item.current_discount_percentage
                    ])
            return "File written successfully!"
        except Exception as e:
            return f"File failed to write! Error: {e}"
        
    def add_sale(self, product: Item):
        if product.num_sold < 1:
            raise ValueError(f"Product {product.name} cannot sell, as the number of {product.name} left is less than 1!")
        
        with open(self.sales_path,"a") as f:
            try:
                f.write(f"{product.name},{datetime.now()}, {str((product.ORIGINAL_PRICE-(product.ORIGINAL_PRICE / 1 / 100*product.current_discount_percentage)))}\n")
            except ZeroDivisionError:
                f.write(f"{product.name},{datetime.now()}, {str(product.ORIGINAL_PRICE)}\n")
        product.num_sold+=1
        product.num_in_stock-=1

def handle_input(user_input: str, shop: Shop):
    if user_input in ["clear shell","cls","clear","1"]:
        if platform.system() == "Windows":
            system('cls')
        else:
            system('clear')
    
    elif user_input in ["ls", "list","2"]:
        for item in shop.item_list:
            print(item)
    
    elif user_input in ["apply discount","manage discount","3"]:
        discounted_item_name = str(input("Which item do you want to apply the discount to?    ")).strip()
        for item in shop.item_list:
            if item.name.lower() == discounted_item_name.lower(): #looks bad if I don't put lower here :D
                try:
                    discount = float(input(f"Enter discount percentage for {item.name}:    "))
                    item.update_discount(discount)
                except ValueError:
                    print("Invalid discount value. Please enter a number.")
                break
        else:
            print(f"Item '{discounted_item_name}' not found in the shop.")
        shop.save()
    
    elif user_input in ["new purchase","handle new", "4", "add sale", "new sale"]:
        sold_item_name = str(input("Enter the name of the product that sold:    ")).lower()
        for item in shop.item_list:
            if item.name.lower() == sold_item_name: #both lower, but i use it multiple times so its a very very slight optimisation.
                shop.add_sale(product=item)
                break
        else:
            print(f"Item '{sold_item_name}' not found in the shop. Enter 4 to retry.")
        shop.save()



if __name__ == "__main__":
    shop = Shop("items.csv", "sales.csv")
    while True:
        user_input = str(input()).lower()
        handle_input(user_input, shop)
