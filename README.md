# ForkFiesta Delivery Microservice

Welcome to the ForkFiesta Delivery Microservice! This Flask-based microservice is designed to handle all aspects of the delivery process for the ForkFiesta restaurant. Whether you're a developer looking to integrate delivery functionality into ForkFiesta's ecosystem or a curious soul interested in understanding how ForkFiesta manages its deliveries, you're in the right place.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features
- **Order Management:** Handle incoming orders and keep track of their status throughout the delivery process.
- **Restaurant Integration:** Seamlessly integrate with ForkFiesta's existing systems, ensuring a smooth experience for both customers and restaurant staff.
- **Restaurant Feedback:** Handle incoming feedback from users.

## Getting Started

### Prerequisites
- Python 3.x
- Flask (install via `pip install Flask`)
- Database (MongoDB)

### Installation
1. **Clone this repository:**
   ```sh
   git clone https://github.com/your-username/forkfiesta-delivery-microservice.git
   cd forkfiesta-delivery-microservice
    ```
2. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
    ```

3. **Create `.env` file and add your MongoDB URI**
   ```env
   MONGODB_SRV=
    ```

4. **Start the local server:**
   ```sh
   python run.py
    ```

## Usage
Once the microservice is up and running, it can be accessed via its API endpoints. These endpoints allow you to interact with the delivery management system, create new orders, track deliveries, and more.

### API Endpoints
- GET /api/forkfiesta/orders: Get details about all orders.
- GET /api/forkfiesta/orders/:id: Get details about a specific order.
- POST /api/forkfiesta/write-order: Give the order based on food given food id and quantity
- POST /api/forkfiesta/create-order: Create an order with the delivery info and save it to the database
- PATCH /api/forkfiesta/orders:id: Update the status of an order (e.g., en proceso, entregado, cancelado).


## License
This project is licensed under the MIT License