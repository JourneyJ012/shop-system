import csv
from os import system
import platform
from datetime import datetime


import csv
from os import system
import platform
from datetime import datetime


class Item:
    def __init__(self, name: str, num_in_stock: int, ORIGINAL_PRICE: float, num_sold: int, current_discount_percentage: float) -> None:
        if type(num_in_stock) != int or type(ORIGINAL_PRICE) != float or type(num_sold) != int or type(current_discount_percentage) != float:
            raise TypeError(
                "Malformed inputs! num in stock should be int, original price should be a float, num sold should be int, and current discount should be float!")

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

    def edit_product(self, changing_variable: str, value: float):
        if changing_variable == "current_discount_percentage":
            if 0.0 <= value <= 100.0:
                self.current_discount_percentage = value
                print(
                    f"Discount for {self.name} updated to {self.current_discount_percentage}%")
            else:
                print("Invalid discount percentage. Must be between 0 and 100.")
        elif changing_variable == "num_in_stock":
            self.num_in_stock = int(value)

class Shop:
    def __init__(self, items_path: str, sales_path: str):
        self.items_path = items_path
        self.sales_path = sales_path
        with open(items_path, 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            next(reader)  # Skip the header row
            item_list = []
            for row in reader:
                print(len(row), row)  # Debug print to see the content and length of each row
                if len(row) != 5:
                    continue
                name, num_in_stock, ORIGINAL_PRICE, num_sold, current_discount_percentage = row
                item_list.append(Item(
                    name=str(name),
                    num_in_stock=int(num_in_stock),
                    ORIGINAL_PRICE=float(ORIGINAL_PRICE),
                    num_sold=int(num_sold),
                    current_discount_percentage=float(current_discount_percentage)
                ))
            self.item_list = item_list
            print(item_list)

    def save(self):
        try:
            with open(self.items_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'num_in_stock', 'ORIGINAL_PRICE',
                                 'num_sold', 'current_discount_percentage'])
                for item in self.item_list:
                    
                    writer.writerow([
                        item.name, item.num_in_stock, item.ORIGINAL_PRICE, item.num_sold, item.current_discount_percentage
                    ])
            return "File written successfully!"
        except Exception as e:
            return f"File failed to write! Error: {e}"

    def add_sale(self, product: Item):
        if product.num_sold < 1:
            raise ValueError(
                f"Product {product.name} cannot sell, as the number of {product.name} left is less than 1!")

        with open(self.sales_path, "a") as f:
            try:
                f.write(
                    f"{product.name},{datetime.now()}, {str((product.ORIGINAL_PRICE-(product.ORIGINAL_PRICE / 1 / 100*product.current_discount_percentage)))}\n")
            except ZeroDivisionError:
                f.write(
                    f"{product.name},{datetime.now()}, {str(product.ORIGINAL_PRICE)}\n")
        product.num_sold += 1
        product.num_in_stock -= 1


def handle_input(user_input: str, shop: Shop):
    if user_input in ["clear shell", "cls", "clear", "1"]:
        if platform.system() == "Windows":
            system('cls')
        else:
            system('clear')

    elif user_input in ["ls", "list", "2"]:
        for item in shop.item_list:
            print(item)

    elif user_input in ["apply discount", "manage discount", "3"]:
        discounted_item_name = str(
            input("Which item do you want to apply the discount to?    ")).strip()
        for item in shop.item_list:
            if item.name.lower() == discounted_item_name.lower():  # looks bad if I don't put lower here :D
                try:
                    discount = float(
                        input(f"Enter discount percentage for {item.name}:    "))
                    item.edit_product(
                        changing_variable="current_discount_percentage", value=discount)
                except ValueError:
                    print("Invalid discount value. Please enter a number. Enter 3 to retry.")
                break
        else:
            print(f"Item '{discounted_item_name}' not found in the shop.")
        shop.save()

    elif user_input in ["4", "add sale", "new sale"]:
        sold_item_name = str(
            input("Enter the name of the product that sold:    ")).lower()
        for item in shop.item_list:
            # both lower, but i use it multiple times so its a very very slight optimisation.
            if item.name.lower() == sold_item_name:
                shop.add_sale(product=item)
                break
        else:
            print(f"Item '{sold_item_name}' not found in the shop. Enter 4 to retry.")

    elif user_input in ["5", "change stock count"]:
        stock_product = str(input(
            "Enter the name of the product that you want to change the stock total of:    ")).lower()
        for item in shop.item_list:
            # both lower, but i use it multiple times so its a very very slight optimisation.
            if item.name.lower() == stock_product:
                item.edit_product(changing_variable="num_in_stock")
                break
        else:
            print(f"Item '{stock_product}' not found in the shop. Enter 5 to retry.")

    '''elif user_input in ["6", "add new product", "new product"]: #TODO: FIX GLITCHES
        try:
            new_item = Item(
                name=str(input("What is the item's name?:    ")),
                num_in_stock=int(input("How many do you have right now?:    ")),
                ORIGINAL_PRICE=float(input("How much are you selling this for?:    ")),
                num_sold=int(input(f"How many of these have you sold?:    ")),
                current_discount_percentage=float(input("What is the current discount for this? (type 0 for no discount):    "))
            )
            shop.item_list.append(
                (str(new_item.name), int(new_item.num_in_stock), float(new_item.ORIGINAL_PRICE),
                 int(new_item.num_sold), float(new_item.current_discount_percentage)))
        except ValueError:
            print("Please input numbers in the number boxes. Operation cancelled.")
    '''
    # shop save is called outside of the if statement. This means that every action is auto saved.
    shop.save()


if __name__ == "__main__":
    shop = Shop("items.csv", "sales.csv")
    while True:
        user_input = str(input()).lower()
        handle_input(user_input, shop)
