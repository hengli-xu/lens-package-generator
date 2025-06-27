PaymentType = {
    "cash_card": "cash_card",
    "cash_app_pay": "cash_app_pay",
    "afterpay": "afterpay"
}

Payment_Type_List = ["cash_card", "cash_app_pay", "afterpay", "cash_card+cash_app_pay", "cash_card+afterpay",
                     "cash_app_pay+afterpay", "all"]
Short_Payment_Type_List = ["cash_card", "cash_app_pay", "afterpay", "all"]
Channel = ["in_app", "in_store", "merchant_online", "all"]
Customer_Type = ["new", "existing", "all"]
Time_Frame = ["7d", "28d", "90d", "lm", "ly", "mtd", "qtd", "ytd"]
Comparison_Period = ["previous_period", "same_period_last_year"]


"""
Finish Line
"""
# Cash_Card_Merchant = {
#     "merchant_token": "M_psdxqurn",
#     "payment_type": PaymentType["cash_card"]
# }
#
# Cash_App_Pay_Merchant = {
#     "merchant_token": "M_psdxqurn",
#     "payment_type": PaymentType["cash_app_pay"]
# }
#
# Afterpay_Merchant = {
#     "merchant_token": "ee587f466198eb5915ccab6abf508eee",
#     "payment_type": PaymentType["afterpay"]
# }

"""
American Eagle
"""
Cash_Card_Merchant = {
    "merchant_token": "M_ysfq5y66",
    "payment_type": PaymentType["cash_card"]
}

Cash_App_Pay_Merchant = {
    "merchant_token": "M_ysfq5y66",
    "payment_type": PaymentType["cash_app_pay"]
}

Afterpay_Merchant = {
    "merchant_token": "566cd42ed72effcf7529a968cb1071e2",
    "payment_type": PaymentType["afterpay"]
}

