from app import app
from models import db, User, Category, Product
from werkzeug.security import generate_password_hash


def img(photo_id, w=800):
    return f"https://images.unsplash.com/photo-{photo_id}?w={w}&q=80&auto=format&fit=crop"


with app.app_context():
    db.drop_all()
    db.create_all()

    men = Category(name="Men", image=img("1488161628813-04466f872be2", 600),
                   description="Shirts, pants, jackets and more.")
    women = Category(name="Women", image=img("1515372039744-b8f02a3ae446", 600),
                     description="Dresses, tops, ethnic wear and more.")
    kids = Category(name="Kids", image=img("1519457431-44ccd64a579b", 600),
                    description="Comfortable clothes for kids.")
    db.session.add_all([men, women, kids])
    db.session.commit()

    men_shirts = Category(name="Shirts", parent_id=men.id,
                          description="Casual and formal shirts for men.")
    men_jeans = Category(name="Jeans", parent_id=men.id,
                         description="Slim fit and regular jeans for men.")
    women_dresses = Category(name="Dresses", parent_id=women.id,
                             description="Casual and party dresses.")
    women_tops = Category(name="Tops", parent_id=women.id,
                          description="Casual tops and blouses.")
    kids_hoodies = Category(name="Hoodies", parent_id=kids.id,
                            description="Warm hoodies for kids.")
    db.session.add_all([men_shirts, men_jeans, women_dresses, women_tops, kids_hoodies])
    db.session.commit()

    products = [
        Product(subcategory_id=men_shirts.id, name="White T-Shirt",
                image=img("1521572163474-6864f9cf17ab"), price=499, stock=8,
                discount_percent=10,
                description="A comfortable and stylish white t-shirt made from 100% cotton."),
        Product(subcategory_id=men_jeans.id, name="Black Jeans",
                image=img("1542272604-787c3835535d"), price=999, stock=5,
                discount_percent=10,
                description="Slim fit black jeans with a classic look and durable denim."),
        Product(subcategory_id=men_shirts.id, name="White Shirt",
                image=img("1602810318383-e386cc2a3ccf"), price=699, stock=12,
                discount_percent=5,
                description="A crisp formal white shirt, ideal for office wear."),
        Product(subcategory_id=women_dresses.id, name="Floral Dress",
                image=img("1572804013309-59a88b7e92f1"), price=799, stock=3,
                discount_percent="15",
                description="A light summer floral dress, perfect for warm days."),
        Product(subcategory_id=women_tops.id, name="Casual Top",
                image=img("1564584217132-2271feaeb3c5"), price=449, stock=7,
                discount_percent="10",
                description="An everyday casual top that is light and breathable."),
        Product(subcategory_id=kids_hoodies.id, name="Kids Hoodie",
                image=img("1556821840-3a63f95609a7"), price=599, stock=0,
                discount_percent="10",
                description="A warm and cosy hoodie for kids, made from soft fleece."),
    ]
    db.session.add_all(products)

    demo = User(
        name="Demo User", email="demo@shopeasy.com", phone="9999999999",
        address="123 Demo Street", password=generate_password_hash("demo123"),
    )
    db.session.add(demo)

    db.session.commit()
    print("Database seeded!")
    print("  Categories:    ", Category.query.filter_by(parent_id=None).count())
    print("  Subcategories: ", Category.query.filter(Category.parent_id != None).count())
    print("  Products:      ", Product.query.count())
    print("  Login with: demo@shopeasy.com / demo123")