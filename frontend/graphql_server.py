from ariadne import QueryType, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
JSON_FILE = os.path.join(os.path.dirname(__file__), "products.json")

type_defs = """
    type Product {
        id: ID!
        name: String!
        price: Int!
        description: String
        categories: [String!]!
    }

    type Query {
        products(fields: [String!]!): [Product]!
        product(id: ID!, fields: [String!]!): Product
    }
"""

query = QueryType()

@query.field("products")
def resolve_products(_, info, fields):
    try:
        with open(JSON_FILE, encoding="utf-8") as f:
            products = json.load(f)
        return [{k: v for k, v in item.items() if k in fields} for item in products]
    except Exception as e:
        return {"error": str(e)}

@query.field("product")
def resolve_product(_, info, id, fields):
    try:
        with open(JSON_FILE, encoding="utf-8") as f:
            products = json.load(f)
        product = next((p for p in products if p["id"] == int(id)), None)
        return {k: v for k, v in product.items() if k in fields} if product else None
    except Exception as e:
        return {"error": str(e)}

schema = make_executable_schema(type_defs, query)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data)
    return jsonify(result), 200 if success else 400

if __name__ == "__main__":
    app.run(port=3000, debug=True)