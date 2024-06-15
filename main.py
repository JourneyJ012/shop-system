import csv
from os import system
import platform

class Shop:
    def __init__(self, path: str):
        self.path = path 
        with open(path, 'r') as f:
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
            with open(self.path, 'w', newline='') as f:
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

    def update_discount(self, discount: float, shop: Shop):
        if 0.0 <= discount <= 100.0:
            self.current_discount_percentage = discount
            print(f"Discount for {self.name} updated to {self.current_discount_percentage}%")
        else:
            print("Invalid discount percentage. Must be between 0 and 100.")
        shop.save() 



def handle_input(user_input: str, shop: Shop):
    if user_input in ["clear shell","cls","clear"]:
        if platform.system() == "Windows":
            system('cls')
        else:
            system('clear')
    elif user_input in ["ls", "list"]:
        for item in shop.item_list:
            print(item)
    elif user_input == "apply discount":
        discounted_item_name = str(input("Which item do you want to apply the discount to?    ")).strip()
        for item in shop.item_list:
            if item.name.lower() == discounted_item_name.lower(): #looks bad if I don't put lower here :D
                try:
                    discount = float(input(f"Enter discount percentage for {item.name}:    "))
                    item.update_discount(discount, shop)
                except ValueError:
                    print("Invalid discount value. Please enter a number.")
                break
        else:
            print(f"Item '{discounted_item_name}' not found in the shop.")



if __name__ == "__main__":
    shop = Shop("items.csv")
    while True:
        user_input = str(input()).lower()
        handle_input(user_input, shop)
