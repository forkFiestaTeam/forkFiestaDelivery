from flask import Blueprint, jsonify, request
import requests
import json
import os
from datetime import datetime


# MongoDB instance
from app.config import mdb_client

# ? Functions
from functions.orders import add_product_price_to_order, calculate_total_price

# ENV
from dotenv import load_dotenv

# Initializations
load_dotenv()
forkfiesta_delivery_db = mdb_client.forkfiesta_delivery
orders_collection = forkfiesta_delivery_db.orders
feedback_collection = forkfiesta_delivery_db.feedback

# Microservices APIs
api_gateway_url = os.environ.get("API_GATEWAY_URL")
print("MENU API:",api_gateway_url)

# GraphQL query string to retrieve the menu
menu_query = """
{
  foods {
    id
    name
    price
    description
    category
  }
}
"""

# GraphQL request headers 
headers = {
    "Content-Type": "application/json",
}

# Send a POST request to the GraphQL menu microservice
response = requests.get(f'{api_gateway_url}/menu')

# Parse and handle the response
if response.status_code == 200:
    data = response.json()
    menu_prices = data.get("foods", [])
else:
    print(f"GraphQL Request Failed with Status Code: {response.status_code}")
    print("Response:")
    print(response.text)

# menu_prices = [
#     {"id": 1, "name": "Combo 1", "price": 22000},
#     {"id": 2, "name": "Combo 2", "price": 25000},
#     {"id": 3, "name": "Combo 3", "price": 33000},
#     {"id": 4, "name": "Combo 4", "price": 60000},
#     {"id": 5, "name": "Combo 5", "price": 70000},
#     {"id": 6, "name": "Combo 6", "price": 25000},
#     {"id": 7, "name": "Burger pollo peperoni", "price": 20000},
#     {"id": 8, "name": "Burger pollo peperoni en combo", "price": 25000},
#     {"id": 9, "name": "Burger mixta", "price": 25000},
#     {"id": 10, "name": "Burger mixta en combo", "price": 29500},
#     {"id": 11, "name": "Burger artesanal", "price": 20000},
#     {"id": 12, "name": "Burger artesanal en combo", "price": 25000},
#     {"id": 13, "name": "Burger ropa vieja", "price": 20000},
#     {"id": 14, "name": "Burger ropa vieja en combo", "price": 25000},
#     {"id": 15, "name": "Maicitos gratinados", "price": 22000},
#     {"id": 16, "name": "Chuzo gratinado", "price": 23000},
#     {"id": 17, "name": "Salchipapa mini", "price": 12000},
#     {"id": 18, "name": "Salchipapa personal", "price": 22000},
#     {"id": 19, "name": "Carne de res", "price": 19500},
#     {"id": 20, "name": "Carne de cerdo", "price": 19500},
#     {"id": 21, "name": "Punta de anca", "price": 26000},
#     {"id": 22, "name": "Churrasco", "price": 26000},
#     {"id": 23, "name": "Cañón de cerdo", "price": 19500},
#     {"id": 24, "name": "Pechuga", "price": 22000},
#     {"id": 25, "name": "Papa", "price": 5500},
#     {"id": 26, "name": "Tocinetas (2)", "price": 4000},
#     {"id": 27, "name": "Salchichas (2)", "price": 4000},
#     {"id": 28, "name": "Alita", "price": 3500},
#     {"id": 29, "name": "Queso", "price": 5500},
#     {"id": 30, "name": "Queso cheddar", "price": 4000},
#     {"id": 31, "name": "Salsa de queso", "price": 4000},
#     {"id": 32, "name": "Carne hamburguesa", "price": 7000},
#     {"id": 33, "name": "Aros de cebolla", "price": 4000},
#     {"id": 34, "name": "Pollo hamburguesa", "price": 7000},
#     {"id": 35, "name": "Tornados (1)", "price": 3000},
#     {"id": 36, "name": "Pepinillo", "price": 3000},
#     {"id": 37, "name": "Jalapeños", "price": 3000},
#     {"id": 38, "name": "Arepa", "price": 2000},
#     {"id": 39, "name": "Trozos", "price": 5500},
#     {"id": 40, "name": "Yukas", "price": 4000},
#     {"id": 41, "name": "Carne desmechada", "price": 7000},
#     {"id": 42, "name": "Ensalada", "price": 4000},
#     {"id": 43, "name": "Vaso frutas", "price": 4000},
#     {"id": 44, "name": "Gaseosa 250 ml", "price": 2500},
#     {"id": 45, "name": "Jugo Hit", "price": 3700},
#     {"id": 46, "name": "Mr. te", "price": 3700},
#     {"id": 47, "name": "Gatorade", "price": 4500},
#     {"id": 48, "name": "Canada Dry", "price": 4000},
#     {"id": 49, "name": "Jugo agua", "price": 5000},
#     {"id": 50, "name": "Jugo en leche", "price": 7000},
#     {"id": 51, "name": "Limonada natural", "price": 5000},
#     {"id": 52, "name": "Soda de frutas", "price": 8000},
#     {"id": 53, "name": "Limonada de mango biche", "price": 9000},
#     {"id": 54, "name": "Limonada de coco", "price": 10000},
#     {"id": 55, "name": "Limonada de cereza", "price": 10000},
#     {"id": 56, "name": "Botella de agua", "price": 2500},
#     {"id": 57, "name": "Redbull", "price": 6000},
#     {"id": 58, "name": "Andina", "price": 5000},
#     {"id": 59, "name": "Club Colombia", "price": 5000},
#     {"id": 60, "name": "Poker", "price": 5000},
#     {"id": 61, "name": "Aguila light", "price": 5000},
#     {"id": 62, "name": "Corona", "price": 7000},
#     {"id": 63, "name": "Miller lite", "price": 7000},
#     {"id": 64, "name": "3 Cordilleras", "price": 7000},
#     {"id": 65, "name": "sol", "price": 7000},
#     {"id": 66, "name": "Stella", "price": 9000},
#     {"id": 67, "name": "Vaso michelado", "price": 1700},
#     {"id": 68, "name": "Papas locas", "price": 45000},
#     {"id": 69, "name": "Tocipapas", "price": 10000},
#     {"id": 70, "name": "AD Maíz", "price": 3500},
#     {"id": 71, "name": "Tarro salsa maíz", "price": 23000},
#     {"id": 72, "name": "Heineken", "price": 7000},
#     {"id": 73, "name": "Helado para perros", "price": 5000},
# ]


# ? BUSINESS FUNCTIONS
# ? ROUTES
forkfiesta_routes = Blueprint("forkfiesta_routes", __name__)

# Route to send a welcome message
@forkfiesta_routes.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to ForkFiesta API"})


# Route to list all orders
@forkfiesta_routes.route("/orders", methods=["GET"])
def get_all_orders():
    # Get all orders
    orders = orders_collection.find({})

    # Convert each document to a JSON object
    json_documents = [json.loads(json.dumps(document, default=str)) for document in orders]

    return jsonify({"message": json_documents})

# Route to list a specific order
@forkfiesta_routes.route("/order", methods=["GET"])
def get_order():
    # Get order id
    user_id = request.args.get("id")

    print("ORDER_ID:", user_id)

    # Get orders
    order = orders_collection.find({"user_id": user_id})

    # Convert each document to a JSON object
    json_documents = [json.loads(json.dumps(document, default=str)) for document in order]

    return jsonify({"message": json_documents})


# Route to create an order given some food ids and quantities
@forkfiesta_routes.route("/write-order", methods=["POST"])
def write_order():
    # Body data
    data = request.get_json()
    order_message = data["order_message"]
    order_sauces = data["order_sauces"]
    order_juices = data["order_juices"]
    order_message_splitted = []

    # ? Get order information
    # Split the input string on '-'
    substrings = order_message.split('-')

    # Iterate through the substrings and split them on ','
    for substring in substrings:
        if substring:
            pair = substring.split(',')
            # Convert the split values to integers and add them to the result list
            order_message_splitted.append([pair[0], int(pair[1])])

    # Check if there are items in the order
    if not order_message_splitted:
        return jsonify({"message": "No items in order."}), 400

    # Create the order
    order = {
        "order": [],
        "total_price": ""
    }

    # Add items to the order
    for item in order_message_splitted:
        # Find the index of the item in the menu
        try:
            index = next(
                index for (index, d) in enumerate(menu_prices) if d["id"] == item[0]
            )
        except StopIteration:
            return jsonify({"message": f"Item with id {item[0]} not found in menu."}), 400

        # Add the item to the order
        order["order"].append({
            "id": item[0],
            "name": menu_prices[index]["name"],
            "quantity": item[1],
            "price": menu_prices[index]["price"]
        })

    # Calculate the total price of the order
    order = calculate_total_price(json.dumps(order))

    # Add sauces to the order if there are any
    if order_sauces != "null":
        order_sauces_splitted = order_sauces.split('-')
        order_sauces_splitted.pop(0)
        order_sauces_message = ""

        # Create message for sauces
        for sauce in order_sauces_splitted:
            order_sauces_message += f"-{sauce}\n"
  
        order["order_sauces"] = order_sauces_message

    # Add juices to the order if there are any
    if order_juices != "null":
        order_juices_splitted = order_juices.split('-')
        order_juices_splitted.pop(0)
        order_juices_message = ""

        # Create message for juices
        for juice in order_juices_splitted:
            order_juices_message += f"-{juice}\n"
  
        order["order_juices"] = order_juices_message

    return jsonify({"message": order})


# Route to create an id for an order and save it in the database
@forkfiesta_routes.route("/create-order", methods=["POST"])
def create_order_id():
    try:
        # Body data
        default_value = '0'

        name = request.form.get("name", default_value)
        phone = request.form.get("phone", default_value)
        address = request.form.get("address", default_value)
        order = request.form.get("order", default_value)
        observations = request.form.get("observations", default_value)
        sauces = request.form.get("sauces", default_value)
        juices = request.form.get("juices", default_value)
        payment_method = request.form.get("payment_method", default_value)
        user_id = request.form.get("user_id", default_value)
        created_at = datetime.now()

        # Check if each attribute in the body is not undefined
        if name is None:
            return jsonify({"error": "The attribute 'name' is not defined"}), 400
        elif phone is None:
            return jsonify({"error": "The attribute 'phone' is not defined"}), 400
        elif address is None:
            return jsonify({"error": "The attribute 'address' is not defined"}), 400
        elif order is None:
            return jsonify({"error": "The attribute 'order' is not defined"}), 400
        elif observations is None:
            return jsonify({"error": "The attribute 'observations' is not defined"}), 400
        elif sauces is None:
            return jsonify({"error": "The attribute 'sauces' is not defined"}), 400
        elif juices is None:
            return jsonify({"error": "The attribute 'juices' is not defined"}), 400
        elif payment_method is None:
            return jsonify({"error": "The attribute 'payment_method' is not defined"}), 400
        elif user_id is None:
            return jsonify({"error": "The attribute 'user_id' is not defined"}), 400

        # Retrieve the highest order id and the generate a new id adding 1
        last_order = orders_collection.find_one({}, sort=[("order_id", -1)])

        if last_order:
            order_id = last_order["order_id"] + 1
        else:
            order_id = 1

        # Create the order
        order = {
            "order_id": order_id,
            "name": name,
            "phone": phone,
            "address": address,
            "order": order,
            "observations": observations,
            # "sauces": sauces,
            # "juices": juices,
            "payment_method": payment_method,
            "user_id": user_id,
            "status": "Pending",
            "created_at": created_at,
        }

        # Insert the order in the database
        orders_collection.insert_one(order)

        return jsonify({"message": order_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Route to send feedback to our database
@forkfiesta_routes.route("/feedbacks", methods=["POST"])
def feedback():
    try:
        # Body data
        default_value = '0'

        order_id = request.form.get("order_id", default_value)
        feedback = request.form.get("feedback", default_value)
        created_at = datetime.now()
        
        # Check if each attribute in the body is not undefined
        if order_id is None or order_id == '0':
            return jsonify({"error": "El número de orden no es válido"}), 400
        elif feedback is None or feedback == '0':
            return jsonify({"error": "Por favor, escribe una sugerencia"}), 400

        # Verify is order_id is a number
        try:
            order_id = int(order_id)
        except ValueError:
            return jsonify({"error": "El número de orden no es válido, por favor ingresa un número válido."}), 400

        # Create the feedback data
        feedback_data = {
            "order_id": order_id,
            "feedback": feedback,
            "created_at": created_at
        }

        # Insert the feedback in the database
        feedback_collection.insert_one(feedback_data)

        return jsonify({"message": "ok", "order_id": order_id, "feedback": feedback})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to retrieve all feedbacks from the database
@forkfiesta_routes.route("/feedbacks", methods=["GET"])
def get_feedbacks():
    try:
        # Retrieve all feedbacks from the database
        feedbacks_cursor = feedback_collection.find()

        # Convert each document to a JSON object
        json_documents = [json.loads(json.dumps(document, default=str)) for document in feedbacks_cursor]

        # Return feedbacks as JSON response
        return jsonify({"feedbacks": json_documents})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
