""" Product Catalog Service:
Styrer listen over tilgængelige produkter, inklusive detaljer såsom navn, beskrivelse, pris og billeder.
Tilbyder funktionalitet til at søge, filtrere og kategorisere produkter. """


from flask import Flask, jsonify, request, make_response
import requests

app = Flask(__name__)

# DATABASE 
products_db = []
data = requests.get('https://dummyjson.com/products')
products_db = data.json()['products']


# Get all products
@app.route('/products', methods=['GET'])
def view_products():
    return jsonify(products_db), 200

# Get product from id
@app.route('/products/<int:id>', methods=['GET'])
def view_product(id):
    #Iterer gennem produktlisten og finder matchende produkt
    for product in products_db:
        if product['id'] == id:
            return jsonify(product), 200
        
# Search products by category
@app.route('/products/search', methods=['GET'])
def search_product():
    # Get the query parameter 'q' from the request URL
    category = request.args.get('q')

    # Check if category is provided
    if not category:
        return jsonify({"error": "Category is required"}), 400
    
     # Iterate through product list to find a matching product by category
            # .lower converts all letters to lowercase 
    matching_products = [product for product in products_db if product['category'].lower() == category.lower()]

     # If any products match, return them, else return a not found error
    if matching_products:
        return jsonify(matching_products), 200
    else:
        return jsonify({"error": "No products found for the category"}), 404


# Filter and sort products by price
@app.route('/products/filter', methods=['GET'])
def filter_product_by_price():
    # Get min. and max price
    min_price = float(request.args.get('min_price', 0)) #Standard to 0
    max_price = float(request.args.get('max_price', float('inf'))) #Standard to infinity

    # Sort product by price
    sorted_products = sorted(
        (product for product in products_db if min_price <= product['price'] <= max_price),
        key=lambda product: product['price']  
    )
    return jsonify(sorted_products), 200

"""
'Key' fortæller hvilket element i hvert objekt der skal bruges som basis for sortering
'Lambda product:' tager et element fra listen (i dette tilfælde er det et produkt). 'product' er så hvert element i listen 'matching_products'
'product['price']' er hvad funktionen returnerer. I vores tilfælde tager den hvert produkt og kigger på dens pris '(price)' og sorterer ud fra den.

Ved at gøre brug af overstående, undgår vi at skulle definere en seperat funktion til sortering.


I postman skrives: 
    http://localhost:5000/products/filter?min_price=<min>&max_price=<max>
"""

    
app.run(debug=True, host='0.0.0.0')

