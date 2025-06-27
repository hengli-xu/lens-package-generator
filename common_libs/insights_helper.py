from test_data.insights_data import PaymentType, Cash_Card_Merchant, \
    Cash_App_Pay_Merchant, Afterpay_Merchant


def generate_merchant_infos(payment_type_collection):
    payment_type_list = []
    if payment_type_collection == "all":
        payment_type_list = ["cash_card", "cash_app_pay", "afterpay"]
    elif "+" in payment_type_collection:
        payment_type_list = payment_type_collection.split("+")
    else:
        payment_type_list.append(payment_type_collection)

    merchant_infos = []
    for type in payment_type_list:
        if type == PaymentType["cash_card"]:
            merchant_infos.append(Cash_Card_Merchant)
        elif type == PaymentType["cash_app_pay"]:
            merchant_infos.append(Cash_App_Pay_Merchant)
        elif type == PaymentType["afterpay"]:
            merchant_infos.append(Afterpay_Merchant)
        else:
            raise Exception("invalid payment type!")
    return merchant_infos


def convert_number_to_float(number):
    if number is None or number == "":
        value = 0
    else:
        value = float(number)

    return value


def calculate_aov(total_sales, transaction_number):
    sales = convert_number_to_float(total_sales)
    transaction = convert_number_to_float(transaction_number)

    print("AOV: {0} / {1}".format(sales, transaction))

    aov = 0
    if transaction == 0:
        return aov
    else:
        aov = sales / transaction

    return aov
