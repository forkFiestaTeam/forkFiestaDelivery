import json
from babel.numbers import format_currency


# Function to add the price of each order's product
def add_product_price_to_order(order, menu_prices):
    order_dict = json.loads(order)
    for item in order_dict["order"]:
        index = next(
            index for (index, d) in enumerate(menu_prices) if d["id"] == item["id"]
        )
        item["price"] = menu_prices[index]["price"]
    return json.dumps(order_dict)


# Calculate the total price of the order
def calculate_total_price(order):
    total_price = 0
    order_dict = json.loads(order)
    for item in order_dict["order"]:
        total_price += item["price"] * item["quantity"]

    order_dict["total_price"] = total_price

    # Generate a resume of the order
    order_dict["order_summary"] = summarize_order(order_dict)

    order_dict["order"] = json.dumps(order_dict["order"])

    return order_dict


# Generate a resume of the order
def summarize_order(order):
    order_summary = ""
    for item in order["order"]:
        order_summary += (
            str(item["quantity"])
            + " x "
            + item["name"]
            + " ("
            + format_currency(item["price"], "COP", locale="es_CO")
            + ") "
            + " = "
            + format_currency(item["price"] * item["quantity"], "COP", locale="es_CO")
            + "\n"
        )

    order_summary += "Total: " + format_currency(
        order["total_price"], "COP", locale="es_CO"
    ) + " + Costo domicilio\n"
    return order_summary
