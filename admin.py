from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Category, Product

admin = Blueprint("admin", __name__, url_prefix="/admin")

# Rows per page in the admin list tables.
PER_PAGE = 10


from functools import wraps
from flask import session

ADMIN_EMAIL = "demo@shopeasy.com"

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access the admin panel.", "warning")
            return redirect(url_for("login"))
        from models import User
        user = User.query.get(session["user_id"])
        if not user or user.email != ADMIN_EMAIL:
            flash("You do not have permission to access the admin panel.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated


@admin.route("/")
@admin_required
def dashboard():
    total_categories = Category.query.filter_by(parent_id=None).count()
    total_subcategories = Category.query.filter(Category.parent_id != None).count()
    total_products = Product.query.count()
    return render_template("admin/dashboard.html",
                           total_categories=total_categories,
                           total_subcategories=total_subcategories,
                           total_products=total_products)


@admin.route("/categories")
@admin_required
def categories():
    page = request.args.get("page", 1, type=int)
    pagination = Category.query.filter_by(parent_id=None).paginate(
        page=page, per_page=PER_PAGE, error_out=False)
    return render_template("admin/categories.html",
                           categories=pagination.items, pagination=pagination)


@admin.route("/categories/add", methods=["GET", "POST"])
@admin_required
def add_category():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        image = request.form.get("image", "").strip()
        if not name:
            flash("Category name is required.", "danger")
            return render_template("admin/category_form.html", action="Add", category=None)
        db.session.add(Category(name=name, description=description, image=image))
        db.session.commit()
        flash("Category added successfully.", "success")
        return redirect(url_for("admin.categories"))
    return render_template("admin/category_form.html", action="Add", category=None)


@admin.route("/categories/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_category(id):
    cat = Category.query.get_or_404(id)
    if request.method == "POST":
        cat.name = request.form.get("name", "").strip()
        cat.description = request.form.get("description", "").strip()
        cat.image = request.form.get("image", "").strip()
        if not cat.name:
            flash("Category name is required.", "danger")
            return render_template("admin/category_form.html", action="Edit", category=cat)
        db.session.commit()
        flash("Category updated.", "success")
        return redirect(url_for("admin.categories"))
    return render_template("admin/category_form.html", action="Edit", category=cat)


@admin.route("/categories/delete/<int:id>", methods=["POST"])
@admin_required
def delete_category(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash("Category deleted.", "success")
    return redirect(url_for("admin.categories"))


@admin.route("/subcategories")
@admin_required
def subcategories():
    page = request.args.get("page", 1, type=int)
    pagination = Category.query.filter(Category.parent_id != None).paginate(
        page=page, per_page=PER_PAGE, error_out=False)
    return render_template("admin/subcategories.html",
                           subcategories=pagination.items, pagination=pagination)


@admin.route("/subcategories/add", methods=["GET", "POST"])
@admin_required
def add_subcategory():
    parents = Category.query.filter_by(parent_id=None).all()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        parent_id = request.form.get("parent_id")
        description = request.form.get("description", "").strip()
        image = request.form.get("image", "").strip()
        if not name or not parent_id:
            flash("Name and parent category are required.", "danger")
            return render_template("admin/subcategory_form.html", action="Add",
                                   subcategory=None, parents=parents)
        db.session.add(Category(name=name, parent_id=int(parent_id),
                                description=description, image=image))
        db.session.commit()
        flash("Subcategory added.", "success")
        return redirect(url_for("admin.subcategories"))
    return render_template("admin/subcategory_form.html", action="Add",
                           subcategory=None, parents=parents)


@admin.route("/subcategories/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_subcategory(id):
    sub = Category.query.get_or_404(id)
    parents = Category.query.filter_by(parent_id=None).all()
    if request.method == "POST":
        sub.name = request.form.get("name", "").strip()
        sub.parent_id = int(request.form.get("parent_id"))
        sub.description = request.form.get("description", "").strip()
        sub.image = request.form.get("image", "").strip()
        if not sub.name:
            flash("Name is required.", "danger")
            return render_template("admin/subcategory_form.html", action="Edit",
                                   subcategory=sub, parents=parents)
        db.session.commit()
        flash("Subcategory updated.", "success")
        return redirect(url_for("admin.subcategories"))
    return render_template("admin/subcategory_form.html", action="Edit",
                           subcategory=sub, parents=parents)


@admin.route("/subcategories/delete/<int:id>", methods=["POST"])
@admin_required
def delete_subcategory(id):
    sub = Category.query.get_or_404(id)
    db.session.delete(sub)
    db.session.commit()
    flash("Subcategory deleted.", "success")
    return redirect(url_for("admin.subcategories"))


@admin.route("/products")
@admin_required
def products():
    page = request.args.get("page", 1, type=int)
    pagination = Product.query.paginate(page=page, per_page=PER_PAGE, error_out=False)
    return render_template("admin/products.html",
                           products=pagination.items, pagination=pagination)


@admin.route("/products/add", methods=["GET", "POST"])
@admin_required
def add_product():
    subcategories = Category.query.filter(Category.parent_id != None).all()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        subcategory_id = request.form.get("subcategory_id")
        price = request.form.get("price", "").strip()
        stock = request.form.get("stock", "0").strip()
        discount_percent = request.form.get("discount_percent", "0").strip()
        image = request.form.get("image", "").strip()
        description = request.form.get("description", "").strip()
        if not name or not subcategory_id or not price:
            flash("Name, subcategory, and price are required.", "danger")
            return render_template("admin/product_form.html", action="Add",
                                   product=None, subcategories=subcategories)
        db.session.add(Product(name=name, subcategory_id=int(subcategory_id),
                               price=float(price), stock=int(stock),
                               discount_percent=discount_percent,
                               image=image, description=description))
        db.session.commit()
        flash("Product added.", "success")
        return redirect(url_for("admin.products"))
    return render_template("admin/product_form.html", action="Add",
                           product=None, subcategories=subcategories)


@admin.route("/products/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    subcategories = Category.query.filter(Category.parent_id != None).all()
    if request.method == "POST":
        product.name = request.form.get("name", "").strip()
        product.subcategory_id = int(request.form.get("subcategory_id"))
        product.price = float(request.form.get("price", 0))
        product.stock = int(request.form.get("stock", 0))
        product.discount_percent = request.form.get("discount_percent", "0").strip()
        product.image = request.form.get("image", "").strip()
        product.description = request.form.get("description", "").strip()
        if not product.name:
            flash("Name is required.", "danger")
            return render_template("admin/product_form.html", action="Edit",
                                   product=product, subcategories=subcategories)
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("admin.products"))
    return render_template("admin/product_form.html", action="Edit",
                           product=product, subcategories=subcategories)


@admin.route("/products/delete/<int:id>", methods=["POST"])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("admin.products"))

@admin.route("/enquiries")
@admin_required
def enquiries():
    from models import Enquiry
    page = request.args.get("page", 1, type=int)
    pagination = Enquiry.query.order_by(Enquiry.created_at.desc()).paginate(
        page=page, per_page=PER_PAGE, error_out=False)
    return render_template("admin/enquiries.html",
                           enquiries=pagination.items, pagination=pagination)