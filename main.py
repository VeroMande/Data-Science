import json
from tabulate import tabulate
from shop import ValidateInput


def choise_command():
    '''
    :return: user input
    '''
    user_input = input("Insert a command (insert [close] to terminate): ")
    if user_input.lower() == 'close':
        print('Bye bye')
        return user_input, False
    else:
        return user_input, True


def help_user():
    print("The available commands are the following: "
          "\n• add: add a product to the warehouse"
          "\n• list: lists the products in stock"
          "\n• sale: records a sale made"
          "\n• Profits: Shows total profits"
          "\n• help: shows possible commands"
          "\n• close: exit the program\n")


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
    print(f"Added {quantity} X {product_name}\n")
    return products


def list_products(products):
    '''
    shows the list of products available in the store
    '''
    if len(products) == 0:
        print("There are no products in stock")
    else:
        print("PRODUCT", "QUANTITY", "PRICE")
        #table = [["PRODUCT", "QUANTITY", "PRICE"]]
        for key, value in products.items():
            print(f"{key} {value['quantity']} ${value['selling_price']}")
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
        print("No products to purchase in stock")
        return
    while True:
        product_name = validate_products.find_product(products)
        quantity = validate_products.get_valide_quantity(product_name, products)

        selling_price = products[product_name]['selling_price']
        purchase_price = products[product_name]['purchase_price']
        product_data = {'quantity': quantity, 'selling_price': selling_price, 'purchase_price': purchase_price}
        added_product[product_name] = product_data

        choose = input("Add another product? [yes/NO]")
        if choose.lower() != 'yes':
            print(f"REGISTERED SALE:")
            for key, value in added_product.items():
                tot_sale += value['quantity'] * value['selling_price']
                tot_purchase += value['quantity'] * float(value['purchase_price'])
                print(f"- {value['quantity']} X {key}: ${value['selling_price']}")
            print(f"Totale: ${round(tot_sale, 2)}\n")

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
        print('Impossible to calculate profits. No purchases have been made yet.')
        return
    gross_profit = dict_input_user['gross_profit']['tot']
    net_profit = dict_input_user['net_profit']['tot']
    print(f"Profit: Gross profit = ${round(gross_profit, 2)} Net profit = ${round(gross_profit-net_profit, 2)}\n")


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
            if cmd.lower() == 'help':
                help_user()
            elif cmd.lower() == 'add':
                add_product(dict_products, validate_products)
            elif cmd.lower() == 'list':
                list_products(dict_products)
            elif cmd.lower() == 'sale':
                product_sales(dict_products, dict_input_user, validate_products)
            elif cmd.lower() == 'profit':
                profits(dict_input_user)
            elif cmd.lower() == 'close':
                print('Bye bye')
            else:
                print("Enter [help] to see options")


if __name__ == '__main__':
    main()
