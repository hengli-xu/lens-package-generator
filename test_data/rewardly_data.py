import datetime


class TransactionType:
    CNP = ["ANDROID_PAY_NOT_PRESENT_PURCHASE",
           "APPLE_PAY_NOT_PRESENT_PURCHASE",
           "CARD_NOT_PRESENT_PURCHASE",
           "NETFLIX_TOKEN_PURCHASE",
           "ONLINE_PURCHASE"]

    CP = ["ANDROID_PAY_PURCHASE",
          "APPLE_PAY_PURCHASE",
          "CARD_PRESENT_PURCHASE",
          "DIGITAL_WALLET_PURCHASE",
          "MICROSOFT_PAY_PURCHASE",
          "PINDEBIT",
          "SAMSUNG_PAY_PURCHASE"]

    CNP_and_CP = CNP + CP


class TransactionDiscountType:
    CENTS = "Cents"
    BASIS_POINTS = "Basis Points"

    def generate_transaction_discount_specification(self, total_num_uses=1, duration=24, time_unit="HOURS",
                                                    discount_type=CENTS, cents_discount=300, basis_points="1000",
                                                    basis_points_max_discount="300"):
        transaction_discount_specification = {
            "reward_type": "SINGLE_CURRENCY",
            "total_num_uses": total_num_uses,
            "rate_limit": {
                "count": 1,  # always set to 1 by default
                "duration": duration,  # work with time unit
                "time_unit": time_unit  # user can use coupon once during 24 hours
            }
        }

        if discount_type == TransactionDiscountType.CENTS:
            transaction_discount_specification["amount"] = {
                "amount": cents_discount,  # discount amount
                "currency_code": "USD"
            }
        elif discount_type == TransactionDiscountType.BASIS_POINTS:
            transaction_discount_specification["basis_points"] = basis_points
            transaction_discount_specification["maximum_amount"] = {
                "amount": basis_points_max_discount,
                "currency_code": "USD"
            }

        else:
            raise Exception("Do not support discount type")

        return transaction_discount_specification


def generate_anywhere_boost_info(title, description, discount_type, transaction_type=TransactionType.CNP_and_CP):
    # generate hi_hints
    ui_hints = {
        "title": "{0}".format(title),
        "avatars": [
            {
                "avatar_url": "https://franklin-assets.s3.amazonaws.com/static/dd_boost_100.png",
                "avatar_color": "#FFFFFF",
                "image": None,
                "color": None
            }
        ],
        "program_details_url": "http://cash.me"
    }
    # generate application criteria
    application_criteria = {
        "criteria": {
            "transaction_application_criteria": {
                "criteria": [
                    {"transaction_reason_code_criterion": {"reason_codes": transaction_type}},
                    {"minimum_transaction_amount_criterion": {"minimum_amount_cents": "1000"}}
                ]
            }
        }
    }

    # generate application specification
    specification = {}
    specification = {"transaction_discount_specification": TransactionDiscountType.generate_transaction_discount_specification(discount_type)}
    application_specification = {"specification": specification}

    # application_specification["specification"]["transaction_discount_specification"] = {
    #     TransactionDiscountType.generate_transaction_discount_specification(discount_type)
    # }

    boost_info = {}
    boost_info["ui_hints"] = ui_hints
    boost_info["description"] = description
    boost_info["application_criteria"] = application_criteria
    boost_info["application_specification"] = application_specification

    boost_data = {"boost": boost_info}

    print(boost_data)

    return boost_data


def generate_category_boost_info(category="Coffee Shop", activation_date=None, expiration_date=None,
                                 title="Auto test boost",
                                 description="Auto test description"):
    time_now = datetime.datetime.now()
    if activation_date is None:
        activation_date = (time_now + datetime.timedelta(minutes=5))
        activation_timestamp = int(datetime.datetime.timestamp(activation_date) * 1000)

    if expiration_date is None:
        expiration_date = (activation_date + datetime.timedelta(days=5))
        expiration_timestamp = int(datetime.datetime.timestamp(expiration_date) * 1000)
    ui_hints = {
        "title": "{0}".format(title),
        "avatars": [
            {
                "avatar_url": "https://franklin-assets.s3.amazonaws.com/static/dd_boost_100.png",
                "avatar_color": "#FFFFFF",
                "image": None,
                "color": None
            }
        ],
        "program_details_url": "http://cash.me"
    }
    application_criteria = {
        "criteria": {
            "transaction_application_criteria": {
                "criteria": [
                    {"merchant_category_criterion": {"categories": ["{0}".format(category)]}},
                    {
                        "transaction_reason_code_criterion": {"reason_codes": TransactionType.CNP}
                    },
                    {
                        "minimum_transaction_amount_criterion": {"minimum_amount_cents": "100"}
                    }
                ]
            }
        }
    }

    # $OFF
    application_specification = {
        "specification": {
            "transaction_discount_specification": {
                "reward_type": "SINGLE_CURRENCY",
                "total_num_uses": "500",
                "rate_limit": {
                    "count": 1,
                    "duration": 1,
                    "time_unit": "HOURS"
                },
                # Cents
                "amount": {
                    "amount": "100",  # discount amount
                    "currency_code": "USD"
                }
            }
        }
    }
    eligibility_criteria = {
        "criteria": [{
            "global_address_criterion": {
                "addresses": [
                    {
                        "administrative_district_level_1": "NA",
                        "country_code": "US"
                    }
                ]
            }
        }]
    }
    expiration_criteria = {
        "criteria": [
            {
                "type": "GLOBAL_EXPIRATION",
                "global_expiration_criterion": {
                    "expiration_date_time_ms": expiration_timestamp,
                    "activation_date_time_ms": activation_timestamp
                }
            },
            {
                "type": "TOTAL_LIFETIME_SELECTIONS",
                "lifetime_reward_selection_criterion": {"total_lifetime_selections": 1}
            }]
    }

    boost_info = {}
    boost_info["ui_hints"] = ui_hints
    boost_info["description"] = description
    boost_info["application_criteria"] = application_criteria
    boost_info["application_specification"] = application_specification
    boost_info["eligibility_criteria"] = eligibility_criteria
    boost_info["expiration_criteria"] = expiration_criteria

    boost_data = {"boost": boost_info}

    print(boost_data)

    return boost_data


def generate_merchant_boost_info(parent_merchant, title="Auto test boost", description="Auto test description",
                                 affiliate_url=None):
    ui_hints = {
        "title": "{0}".format(title),
        "program_details_url": ""
    }

    application_criteria = {
        "criteria": {
            "transaction_application_criteria": {
                "criteria": [
                    {
                        "merchant_parent_criterion": {"parent_merchant_tokens": ["{0}".format(parent_merchant)]}
                    },
                    {
                        "transaction_reason_code_criterion": {"reason_codes": TransactionType.CNP_and_CP}
                    }
                ]
            }
        }
    }
    # basis points
    application_specification = {
        "specification": {
            "transaction_discount_specification": {
                "reward_type": "SINGLE_CURRENCY",
                "total_num_uses": None,
                "rate_limit": {
                    "count": 1,
                    "duration": 3,
                    "time_unit": "HOURS"
                },
                "basis_points": "100",
                "maximum_amount": {
                    "amount": "300",
                    "currency_code": "USD"
                }
            }
        }
    }

    boost_info = {}
    if affiliate_url is not None:
        boost_info["affiliate_link_url"] = affiliate_url
    boost_info["ui_hints"] = ui_hints
    boost_info["description"] = description
    boost_info["application_criteria"] = application_criteria
    boost_info["application_specification"] = application_specification

    boost_data = {"boost": boost_info}
    print(boost_data)
    return boost_data
