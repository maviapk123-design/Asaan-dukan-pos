from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Asaan Dukan API")

# ہماری دکان کا سامان
products = [
    {"id": 1, "name": "Cheeni", "price": 180, "stock": 100},
    {"id": 2, "name": "Chawal", "price": 320, "stock": 50},
    {"id": 3, "name": "Ghee", "price": 550, "stock": 30}
]

class NewProduct(BaseModel):
    name: str
    price: int
    stock: int

class BillItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/")
def home():
    return {"message": "Asaan Dukan POS System chal raha hai - by Peshawar Developer"}

@app.get("/products")
def get_products():
    return products

@app.post("/products")
def add_product(product: NewProduct):
    new_id = len(products) + 1
    new_item = {"id": new_id, **product.model_dump()}
    products.append(new_item)
    return new_item

@app.post("/bill")
def create_bill(items: list[BillItem]):
    total = 0
    bill_details = []
    for item in items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if product and product["stock"] >= item.quantity:
            subtotal = product["price"] * item.quantity
            total += subtotal
            product["stock"] -= item.quantity
            bill_details.append(f"{product['name']} x {item.quantity} = {subtotal}")
    
    return {"bill": bill_details, "total_bill": total, "message": "Shukria!"}
