import json

# ---------------------------
# Class: Product (Clothing Item)
# ---------------------------
class Product:
    def __init__(self, product_id, name, category, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

    def display(self):
        print(f"{self.product_id}. {self.name} ({self.category}) - ₹{self.price}")

# ---------------------------
# Class: CartItem
# ---------------------------
class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total_price(self):
        return self.product.price * self.quantity

    def display(self):
        print(f"{self.product.name} x{self.quantity} = ₹{self.get_total_price()}")

# ---------------------------
# Class: Cart
# ---------------------------
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                print(f"✅ Updated quantity for {product.name}")
                return
        self.items.append(CartItem(product, quantity))
        print(f"🛍️ Added {product.name} to cart")

    def remove_item(self, product_id):
        for item in self.items:
            if item.product.product_id == product_id:
                self.items.remove(item)
                print(f"❌ Removed {item.product.name}")
                return
        print("⚠️ Item not found in cart!")

    def display_cart(self):
        if not self.items:
            print("🛒 Your cart is empty.")
            return
        print("\n🧺 Your Cart:")
        for item in self.items:
            item.display()

    def get_total_amount(self):
        return sum(item.get_total_price() for item in self.items)

# ---------------------------
# Class: Coupon
# ---------------------------
class Coupon:
    def __init__(self, code, discount_percent):
        self.code = code
        self.discount_percent = discount_percent

    def apply_discount(self, amount):
        discount = (self.discount_percent / 100) * amount
        return amount - discount

# ---------------------------
# Class: Checkout
# ---------------------------
class Checkout:
    def __init__(self, cart, coupon=None):
        self.cart = cart
        self.coupon = coupon

    def calculate_total(self):
        total = self.cart.get_total_amount()
        if self.coupon:
            total = self.coupon.apply_discount(total)
            print(f"🎟️ Coupon '{self.coupon.code}' applied ({self.coupon.discount_percent}% off)!")
        return total

    def display_bill(self):
        print("\n===== Final Bill =====")
        self.cart.display_cart()
        total = self.calculate_total()
        print(f"\nTotal Payable Amount: ₹{total:.2f}")
        print("======================")

# ---------------------------
# Class: OrderRepository
# ---------------------------
class OrderRepository:
    def __init__(self, filename="clothes_orders.json"):
        self.filename = filename

    def save_order(self, cart, total):
        order_data = {
            "items": [
                {"name": item.product.name, "category": item.product.category,
                 "quantity": item.quantity, "price": item.product.price}
                for item in cart.items
            ],
            "total_amount": total
        }
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        data.append(order_data)
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)
        print("💾 Order saved successfully!")

# ---------------------------
# Main Program
# ---------------------------
if __name__ == "__main__":
    # Sample clothing products
    products = [
        Product(1, "Formal Shirt", "Men", 1200),
        Product(2, "Jeans Pant", "Men", 1800),
        Product(3, "T-Shirt", "Unisex", 800),
        Product(4, "Jacket", "Men", 2500),
        Product(5, "Blazer Coat", "Men", 4000),
        Product(6, "Kurti", "Women", 1500)
    ]

    cart = Cart()

    while True:
        print("\n👕👖 CLOTHING SHOP MENU 👗🧥")
        for p in products:
            p.display()
        print("7. View Cart")
        print("8. Remove Item")
        print("9. Checkout")
        print("10. Exit")

        choice = input("\nEnter your choice: ")

        if choice.isdigit() and 1 <= int(choice) <= 6:
            pid = int(choice)
            qty = int(input("Enter quantity: "))
            cart.add_item(products[pid - 1], qty)

        elif choice == "7":
            cart.display_cart()

        elif choice == "8":
            pid = int(input("Enter Product ID to remove: "))
            cart.remove_item(pid)

        elif choice == "9":
            code = input("Enter coupon code (or press Enter to skip): ").upper()
            coupon = None
            if code == "CLOTH10":
                coupon = Coupon("CLOTH10", 10)
            checkout = Checkout(cart, coupon)
            total = checkout.calculate_total()
            checkout.display_bill()

            repo = OrderRepository()
            repo.save_order(cart, total)
            break

        elif choice == "10":
            print("👋 Thank you for shopping with us!")
            break

        else:
            print("⚠️ Invalid choice! Please try again.")
