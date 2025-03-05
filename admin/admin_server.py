from flask import Flask, request, jsonify
from flask_cors import CORS  # Добавьте CORS
import json
import os
from threading import Lock

app = Flask(__name__)
CORS(app)  # Включите CORS
JSON_FILE = os.path.join(os.path.dirname(__file__), "..", "frontend", "products.json")
lock = Lock()

def read_products():
    with lock:
        if not os.path.exists(JSON_FILE):
            return []
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

def write_products(products):
    with lock:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(read_products())

@app.route("/api/products", methods=["POST"])
def add_products():
    new_products = request.get_json()
    if not isinstance(new_products, list):
        new_products = [new_products]
    
    products = read_products()
    max_id = max(p["id"] for p in products) if products else 0
    for product in new_products:
        max_id += 1
        product["id"] = max_id
        products.append(product)
    write_products(products)
    return jsonify({"message": "Products added", "count": len(new_products)}), 201

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    products = read_products()
    for product in products:
        if product["id"] == product_id:
            product.update(data)
            write_products(products)
            return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    products = read_products()
    new_products = [p for p in products if p["id"] != product_id]
    if len(new_products) == len(products):
        return jsonify({"error": "Product not found"}), 404
    write_products(new_products)
    return jsonify({"message": "Product deleted"})

if __name__ == "__main__":
    app.run(port=8080, debug=True)  # Убедитесь, что порт 8080