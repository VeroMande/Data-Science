import json
from tabulate import tabulate
from shop import ValidateInput


def choise_command():
    '''
    :return: user input
    '''
    user_input = input("Inserisci un comando ([chiudi] per terminare): ")
    if user_input.lower() == 'chiudi':
        print('Bye bye')
        return user_input, False
    else:
        return user_input, True


def help_user():
    print("I comandi disponibili sono i seguenti: "
          "\n• aggiungi: aggiungi un prodotto al magazzino"
          "\n• elenca: elenca i prodotto in magazzino"
          "\n• vendita: registra una vendita effettuata"
          "\n• profitti: mostra i profitti totali"
          "\n• aiuto: mostra i possibili comandi"
          "\n• chiudi: esci dal programma\n")


def add_product(products, validate_products):
    '''
    add a product to the store
    '''
    product_name = validate_products.validate_product_name()
    quantity = validate_products.validate_quantity()

    if product_name in products:
        products[product_name]["quantity"] += quantity
    else:
        purchase_price = validate_products.validate_purchase_price()
        selling_price = validate_products.validate_selling_price(purchase_price)

        products[product_name] = {
            'quantity': quantity,
            'purchase_price': purchase_price,
            'selling_price': selling_price
        }
    save_data_to_file(products, 'product_data.txt')
    print(f"AGGIUNTO: {quantity} X {product_name}\n")
    return products


def list_products(products):
    '''
    shows the list of products available in the store
    '''
    if len(products) == 0:
        print("Non ci sono prodotti in magazzino")
    else:
        print("Prodotto", "Quantità", "Prezzo")
        #table = [["PRODUCT", "QUANTITY", "PRICE"]]
        for key, value in products.items():
            print(f"{key} {value['quantity']} €{value['selling_price']}")
            #table.append([key, value['quantity'], value['selling_price']])
        #print(tabulate(table, headers="firstrow", tablefmt="github"))
        print(' ')

def product_sales(products, dict_input_user, validate_products):
    '''
    purchasing products from stock

    :param products: dictionary with products
    :param dict_input_user: dictionary with the profits
    :return:
    '''
    added_product = {}
    tot_sale = 0
    tot_purchase = 0
    if len(products) == 0:
        print("Nessun prodotto da acquistare a magazzino")
        return
    while True:
        product_name = validate_products.find_product(products)
        quantity = validate_products.get_valide_quantity(product_name, products)

        selling_price = products[product_name]['selling_price']
        purchase_price = products[product_name]['purchase_price']
        product_data = {'quantity': quantity, 'selling_price': selling_price, 'purchase_price': purchase_price}
        added_product[product_name] = product_data

        choose = input("Aggiungere un altro prodotto? (si/NO)")
        if choose.lower() != 'si':
            print(f"VENDITA REGISTRATA:")
            for key, value in added_product.items():
                tot_sale += value['quantity'] * value['selling_price']
                tot_purchase += value['quantity'] * float(value['purchase_price'])
                print(f"- {value['quantity']} X {key}: €{value['selling_price']}")
            print(f"Totale: €{round(tot_sale, 2)}\n")

            if 'gross_profit' not in dict_input_user and 'net_profit' not in dict_input_user:
                dict_input_user['gross_profit'] = {'tot': tot_sale}
                dict_input_user['net_profit'] = {'tot': tot_purchase}
            else:
                dict_input_user['gross_profit']['tot'] += tot_sale
                dict_input_user['net_profit']['tot'] += tot_purchase
            break

    if products[product_name]['quantity'] == 0:
        del products[product_name]

    save_data_to_file(products, 'product_data.txt')
    save_data_to_file(dict_input_user, 'input_user.txt')


def profits(dict_input_user):
    '''
    Gross profit = the total sales, i.e. everything that customers have paid
    net profit = gross profit minus the purchase cost for the products
    '''
    if len(dict_input_user) == 0:
        print('Impossibile calcolare i profitti. Non è stato ancora effettuato alcun acquisto.')
        return
    gross_profit = dict_input_user['gross_profit']['tot']
    net_profit = dict_input_user['net_profit']['tot']
    print(f"Profitto: lordo = €{round(gross_profit, 2)} netto = €{round(gross_profit-net_profit, 2)}\n")


def save_data_to_file(data, filename):
    '''
    :param data: data to write in the open file using JSON formatting.
    :param filename: overwritten or created (if it does not exist) file name
    '''
    with open(filename, 'w') as file:
        json.dump(data, file)


def load_data_from_file(filename):
    '''
    :param filename: file name of the file read
    :return: the file converted into a Python object (dictionary)
    '''
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # If the file does not exist, it returns an empty dictionary


def main():
    dict_products = load_data_from_file('product_data.txt')
    dict_input_user = load_data_from_file('profit.txt')
    validate_products = ValidateInput(dict_products)

    while True:
        cmd, is_close = choise_command()
        if not is_close:
            break
        else:
            if cmd.lower() == 'aiuto':
                help_user()
            elif cmd.lower() == 'aggiungi':
                add_product(dict_products, validate_products)
            elif cmd.lower() == 'elenca':
                list_products(dict_products)
            elif cmd.lower() == 'vendita':
                product_sales(dict_products, dict_input_user, validate_products)
            elif cmd.lower() == 'profitti':
                profits(dict_input_user)
            elif cmd.lower() == 'chiudi':
                print('Bye bye')
            else:
                print("Inserisci [aiuto] per vedere le opzioni")


if __name__ == '__main__':
    main()
