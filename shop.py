import re

class ValidateInput:

    def __init__(self, products=None):
        self.products = products if products else {}

    def find_product(self, products):
        '''
        search for a product in the store to purchase
        '''
        while True:
            product_name = input("Product Name: ")
            if product_name in products:
                return product_name
            else:
                print("The product is not in stock")
                print("The products available for purchase are:")
                for available_product in products:
                    print(f"• {available_product}")

    def validate_product_name(self):
        while True:
            product_name = input("Product Name: ")
            if re.match(r'^[a-zA-Z\s]+$', product_name):
                return product_name
            else:
                print("The product name must contain only alphabetic letters")

    def validate_quantity(self):
        while True:
            try:
                quantity = int(input("Quantity: "))
                if quantity <= 0:
                    print("The quantity cannot be zero or negative")
                    continue
                return quantity
            except ValueError:
                print('Please enter a valid integer quantity.')

    def get_valide_quantity(self, product_name, products):
        '''
        check the quantity of product to purchase
        '''
        while True:
            try:
                quantity = int(input("Quantity: "))
                if quantity > 0 and quantity <= products[product_name]['quantity']:
                    products[product_name]['quantity'] -= quantity
                    return quantity
                else:
                    print("Please enter a valid quantity within available stock")
            except ValueError:
                print("Please enter a valid numeric quantity")


    def validate_purchase_price(self):
        while True:
            purchase_price = input("Purchase price: ")
            if float(purchase_price) <= 0:
                print('The purchase price cannot be negative')
            elif '.' in purchase_price:
                integer_part, decimal_part = purchase_price.split('.')
                if len(integer_part) == 1 and integer_part.isdigit() and len(
                        decimal_part) == 2 and decimal_part.isdigit():
                    purchase_price = float(purchase_price)
                    return purchase_price
                else:
                    print("Enter only 1 value before the decimal point and 2 after it")
            elif purchase_price.isdigit():
                return purchase_price
            else:
                print("Purchase price must be a decimal number")

    def validate_selling_price(self, purchase_price):
        while True:
            selling_price = input("Selling price: ")
            if float(selling_price) <= 0:
                print('The purchase price cannot be negative')
            elif '.' in selling_price:
                integer_part, decimal_part = selling_price.split('.')
                if len(integer_part) == 1 and integer_part.isdigit() and len(
                        decimal_part) == 2 and decimal_part.isdigit():
                    selling_price = float(selling_price)
                    if float(selling_price) > float(purchase_price):
                        return selling_price
                    else:
                        print("Selling price must be greater than the purchase price")
                else:
                    print("Enter only 1 value before the decimal point and 2 after it")
            elif purchase_price.isdigit():
                return purchase_price
            else:
                print("Selling price must be a decimal number")