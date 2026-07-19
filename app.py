from flask import (
    Flask, render_template, request, redirect, url_for, session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
import re

from config import Config
from models import db, User, Category, Product, Enquiry
from admin import admin


app = Flask(__name__)
app.register_blueprint(admin)
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect(app)


def get_cart():
    """Get cart from session, initialize if not exists"""
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']


def get_cart_count():
    """Get total item count in cart"""
    cart = get_cart()
    return sum(cart.values())


@app.context_processor
def inject_cart_count():
    """Make cart_count available in all templates"""
    return dict(cart_count=get_cart_count())
@app.route("/")
def index():
    categories = Category.query.filter_by(parent_id=None).all()
    # For each top-level category, get up to 6 products from its subcategories
    category_products = {}
    for cat in categories:
        sub_ids = [sub.id for sub in cat.subcategories]
        if sub_ids:
            products = Product.query.filter(Product.subcategory_id.in_(sub_ids)).limit(6).all()
        else:
            products = []
        category_products[cat.id] = products
    return render_template("index.html", categories=categories, category_products=category_products)


@app.route("/products")
def products():
    category_name = request.args.get("category")
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 6

    query = Product.query
    heading = "All Products"

    if category_name:
        category = Category.query.filter_by(name=category_name).first()
        if category:
            ids = [category.id] + [sub.id for sub in category.subcategories]
            query = query.filter(Product.subcategory_id.in_(ids))
            possessive = category_name + "'" if category_name.endswith("s") else category_name + "'s"
            heading = possessive + " Products"
        else:
            # Invalid category - show empty results with default heading
            heading = "All Products"
    else:
        heading = "All Products"

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
        heading = f'Search results for "{search}"'

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("products.html",
                           products=pagination.items,
                           heading=heading,
                           pagination=pagination,
                           category=category_name or "",
                           search=search)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)

    discount = product.discount_percent or 0
    final_price = round(float(product.price) - float(product.price) * discount / 100)

    return render_template("product_detail.html", product=product, final_price=final_price)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        error = None
        if not name or not email or not password:
            error = "Name, email and password are required."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            error = "Enter a valid email address."
        elif phone and not re.match(r'^[0-9]{10}$', phone):
            error = "Phone must be a 10-digit number."
        elif User.query.filter_by(email=email).first():
            error = "An account with that email already exists."

        if error:
            flash(error, "danger")
            return render_template("register.html", name=name, email=email,
                                   phone=phone, address=address)

        user = User(
            name=name, email=email, phone=phone, address=address,
            password=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        error = None
        if not email:
            error = "Email is required."
        elif not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            error = "Enter a valid email address."
        elif not password:
            error = "Password is required."

        if error:
            flash(error, "danger")
            return render_template("login.html", email=email)

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_email"] = user.email
            flash("Welcome back, " + user.name + "!", "success")
            return redirect(url_for("index"))

        flash("Invalid email or password.", "danger")
        return render_template("login.html", email=email)

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))

@app.route("/enquiry", methods=["POST"])
@csrf.exempt
def enquiry():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    enquiry_type = data.get("type", "").strip()
    description = data.get("description", "").strip()

    if not name or not email or not phone or not enquiry_type or not description:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    enq = Enquiry(name=name, email=email, phone=phone,
                  type=enquiry_type, description=description)
    db.session.add(enq)
    db.session.commit()

    return jsonify({"success": True, "message": "Thank you! We'll get back to you soon."})


@app.route("/cart")
def cart():
    cart = get_cart()
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            discount = product.discount_percent or 0
            final_price = round(float(product.price) - float(product.price) * discount / 100)
            item_total = final_price * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'final_price': final_price,
                'item_total': item_total
            })
    
    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = get_cart()
    
    current_qty = cart.get(str(product_id), 0)
    if current_qty < product.stock:
        cart[str(product_id)] = current_qty + 1
        session.modified = True
        flash(f"{product.name} added to cart!", "success")
    else:
        flash("Cannot add more - out of stock!", "danger")
    
    return redirect(request.referrer or url_for('products'))


@app.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    cart = get_cart()
    quantity = int(request.form.get("quantity", 1))
    product = Product.query.get_or_404(product_id)
    
    if quantity > 0 and quantity <= product.stock:
        cart[str(product_id)] = quantity
        session.modified = True
        flash("Cart updated!", "success")
    elif quantity > product.stock:
        flash(f"Only {product.stock} items available!", "danger")
    else:
        cart.pop(str(product_id), None)
        session.modified = True
        flash("Item removed from cart!", "info")
    
    return redirect(url_for('cart'))


@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    session.modified = True
    flash("Item removed from cart!", "info")
    return redirect(url_for('cart'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
