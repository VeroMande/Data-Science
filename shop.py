import re

class ValidateInput:

    def __init__(self, products=None):
        self.products = products if products else {}

    def find_product(self, products):
        '''
        search for a product in the store to purchase
        '''
        while True:
            product_name = input("Nome del prodotto: ")
            if product_name in products:
                return product_name
            else:
                print("Il prodotto non è in magazzino")
                print("I prodotti acquistabili sono:")
                for available_product in products:
                    print(f"• {available_product}")

    def validate_product_name(self):
        while True:
            product_name = input("Nome del prodotto: ")
            if re.match(r'^[a-zA-Z\s]+$', product_name):
                return product_name
            else:
                print("Il nome del prodotto deve contenere solo lettere.")

    def validate_quantity(self):
        while True:
            try:
                quantity = int(input("Quantità: "))
                if quantity <= 0:
                    print("La quantità non può essere zero o negativa")
                    continue
                return quantity
            except ValueError:
                print('Inserisci una quantità intera valida.')

    def get_valide_quantity(self, product_name, products):
        '''
        check the quantity of product to purchase
        '''
        while True:
            try:
                quantity = int(input("Quantità: "))
                if quantity > 0 and quantity <= products[product_name]['quantity']:
                    products[product_name]['quantity'] -= quantity
                    return quantity
                else:
                    print("Inserisci una quantità valida all'interno dello stock disponibile")
            except ValueError:
                print("Inserisci una quantità numerica valida")


    def validate_purchase_price(self):
        while True:
            purchase_price = input("Prezzo di acquisto: ")
            if float(purchase_price) <= 0:
                print('Il prezzo di acquisto non può essere negativo')
            elif '.' in purchase_price:
                integer_part, decimal_part = purchase_price.split('.')
                if len(integer_part) == 1 and integer_part.isdigit() and len(
                        decimal_part) == 2 and decimal_part.isdigit():
                    purchase_price = float(purchase_price)
                    return purchase_price
                else:
                    print("Inserisci solo 1 valore prima del punto decimale e 2 dopo di esso")
            elif purchase_price.isdigit():
                return purchase_price
            else:
                print("Il prezzo di acquisto deve essere un numero decimale")

    def validate_selling_price(self, purchase_price):
        while True:
            selling_price = input("Prezzo di vendita: ")
            if float(selling_price) <= 0:
                print('Il prezzo di acquisto non può essere negativo')
            elif '.' in selling_price:
                integer_part, decimal_part = selling_price.split('.')
                if len(integer_part) == 1 and integer_part.isdigit() and len(
                        decimal_part) == 2 and decimal_part.isdigit():
                    selling_price = float(selling_price)
                    if float(selling_price) > float(purchase_price):
                        return selling_price
                    else:
                        print("Il prezzo di vendita deve essere superiore al prezzo di acquisto")
                else:
                    print("Inserisci solo 1 valore prima del punto decimale e 2 dopo di esso")
            elif purchase_price.isdigit():
                return purchase_price
            else:
                print("Il prezzo di vendita deve essere un numero decimale")
