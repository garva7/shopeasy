from app import app
from models import db, User, Category, Product
from werkzeug.security import generate_password_hash


def img(filename):
    return f"/static/images/{filename}"


with app.app_context():
    db.drop_all()
    db.create_all()

    men = Category(
        name="Men",
        image=img("men/black-jeans.avif"),
        description="Shirts, pants, jackets and more.",
    )
    women = Category(
        name="Women",
        image=img("women/floral-dress.webp"),
        description="Dresses, tops, ethnic wear and more.",
    )
    kids = Category(
        name="Kids",
        image=img("kids/hoodie.jpeg"),
        description="Comfortable clothes for kids.",
    )
    db.session.add_all([men, women, kids])
    db.session.commit()

    men_shirts = Category(
        name="Shirts", parent_id=men.id, description="Casual and formal shirts for men."
    )
    men_jeans = Category(
        name="Jeans", parent_id=men.id, description="Slim fit and regular jeans for men."
    )
    women_dresses = Category(
        name="Dresses", parent_id=women.id, description="Casual and party dresses."
    )
    women_tops = Category(
        name="Tops", parent_id=women.id, description="Casual tops and blouses."
    )
    kids_hoodies = Category(
        name="Hoodies", parent_id=kids.id, description="Warm hoodies for kids."
    )
    db.session.add_all([men_shirts, men_jeans, women_dresses, women_tops, kids_hoodies])
    db.session.commit()

    products = [
        # Men — Shirts (3 products)
        Product(
            subcategory_id=men_shirts.id,
            name="White T-Shirt",
            image=img("men/white-tshirt.jpeg"),
            price=499,
            stock=8,
            discount_percent=10,
            description="A comfortable and stylish white t-shirt made from 100% cotton.",
        ),
        Product(
            subcategory_id=men_shirts.id,
            name="White Shirt",
            image=img("men/white-shirt.avif"),
            price=699,
            stock=12,
            discount_percent=5,
            description="A crisp formal white shirt, ideal for office wear.",
        ),
        Product(
            subcategory_id=men_shirts.id,
            name="Blue Check Shirt",
            image=img("men/blue-check.avif"),
            price=749,
            stock=10,
            discount_percent=0,
            description="A smart blue checked shirt for casual outings.",
        ),
        # Men — Jeans (3 products)
        Product(
            subcategory_id=men_jeans.id,
            name="Black Jeans",
            image=img("men/black-jeans.avif"),
            price=999,
            stock=5,
            discount_percent=10,
            description="Slim fit black jeans with a classic look and durable denim.",
        ),
        Product(
            subcategory_id=men_jeans.id,
            name="Blue Denim Jeans",
            image=img("men/blue-jeans.jpeg"),
            price=1099,
            stock=7,
            discount_percent=0,
            description="Classic blue denim jeans with a regular fit.",
        ),
        Product(
            subcategory_id=men_jeans.id,
            name="Grey Joggers",
            image=img("men/grey-joggers.jpeg"),
            price=599,
            stock=15,
            discount_percent=5,
            description="Comfortable grey joggers for everyday wear.",
        ),
        # Women — Dresses (3 products)
        Product(
            subcategory_id=women_dresses.id,
            name="Floral Dress",
            image=img("women/floral-dress.webp"),
            price=799,
            stock=3,
            discount_percent="15",
            description="A light summer floral dress, perfect for warm days.",
        ),
        Product(
            subcategory_id=women_dresses.id,
            name="Evening Gown",
            image=img("women/evening-gown.avif"),
            price=1499,
            stock=4,
            discount_percent=0,
            description="An elegant evening gown for special occasions.",
        ),
        Product(
            subcategory_id=women_dresses.id,
            name="Kurti",
            image=img("women/kurti.webp"),
            price=549,
            stock=10,
            discount_percent=10,
            description="A stylish cotton kurti for daily ethnic wear.",
        ),
        # Women — Tops (3 products)
        Product(
            subcategory_id=women_tops.id,
            name="Casual Top",
            image=img("women/casual-top.avif"),
            price=449,
            stock=7,
            discount_percent="10",
            description="An everyday casual top that is light and breathable.",
        ),
        Product(
            subcategory_id=women_tops.id,
            name="Women's Shirt",
            image=img("women/women-shirt.avif"),
            price=599,
            stock=6,
            discount_percent=0,
            description="A chic shirt for work or play.",
        ),
        Product(
            subcategory_id=women_tops.id,
            name="Denim Jacket",
            image=img("women/denim-women.avif"),
            price=1299,
            stock=5,
            discount_percent=20,
            description="A trendy denim jacket that goes with everything.",
        ),
        # Kids — Hoodies (3 products)
        Product(
            subcategory_id=kids_hoodies.id,
            name="Kids Hoodie",
            image=img("kids/hoodie.jpeg"),
            price=599,
            stock=0,
            discount_percent="10",
            description="A warm and cosy hoodie for kids, made from soft fleece.",
        ),
        Product(
            subcategory_id=kids_hoodies.id,
            name="Kids T-Shirt Set",
            image=img("kids/kids-set.avif"),
            price=399,
            stock=12,
            discount_percent=0,
            description="A pack of 3 colourful t-shirts for kids.",
        ),
        Product(
            subcategory_id=kids_hoodies.id,
            name="Kids Track Pants",
            image=img("kids/kids-tracks.jpeg"),
            price=449,
            stock=8,
            discount_percent=5,
            description="Soft and stretchy track pants for active kids.",
        ),
    ]
    db.session.add_all(products)

    demo = User(
        name="Demo User",
        email="demo@shopeasy.com",
        phone="9999999999",
        address="123 Demo Street",
        password=generate_password_hash("demo123"),
    )
    db.session.add(demo)
    db.session.commit()
    print("Database seeded!")
    print(" Categories: ", Category.query.filter_by(parent_id=None).count())
    print(" Subcategories: ", Category.query.filter(Category.parent_id != None).count())
    print(" Products: ", Product.query.count())
    print(" Login with: demo@shopeasy.com / demo123")