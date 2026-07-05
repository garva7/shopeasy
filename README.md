# ShopEasy

A full-stack eCommerce web application built with Flask, MySQL, Bootstrap, and jQuery. The project was built incrementally over four weeks as part of a training curriculum, starting from static HTML pages and ending with a working admin panel, server-side pagination, and AJAX form submission.

---

## What it does

- Displays clothing products across three categories: Men, Women, and Kids
- Each category has subcategories, and products are linked to those subcategories
- Users can register, log in, and log out
- Passwords are stored as hashes, never plain text
- A logged-in admin user can manage categories, subcategories, and products through an admin panel
- The product listing page supports server-side search and pagination
- A contact form on the homepage submits via AJAX and stores enquiries in the database

---

## Tech stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** MySQL (via PyMySQL), with SQLite as an optional fallback
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript, jQuery
- **Templating:** Jinja2

---

## Project structure

```
app.py                  Flask routes (public pages and authentication)
admin.py                Admin blueprint (CRUD for categories, subcategories, products, enquiries)
models.py               SQLAlchemy models (User, Category, Product, Enquiry)
config.py               Database connection settings
seed.py                 Creates tables and inserts sample data
schema.sql              Raw MySQL schema for reference
requirements.txt        Python dependencies

templates/
    base.html           Base layout (navbar, flash messages, footer)
    header.html         Navbar (includes Admin link for admin user)
    footer.html         Footer
    index.html          Homepage with category cards and enquiry modal
    products.html       Product listing with search and pagination
    product_detail.html Single product view with discount and stock status
    login.html          Login form
    register.html       Registration form
    about.html          About page

    admin/
        base_admin.html     Admin base layout
        dashboard.html      Dashboard with counts
        categories.html     Category list
        category_form.html  Add / edit category
        subcategories.html  Subcategory list
        subcategory_form.html  Add / edit subcategory
        products.html       Product list
        product_form.html   Add / edit product
        enquiries.html      Submitted enquiries

static/
    style.css           Site-wide styles
    main.js             Cart counter
    login.js            Show / hide password toggle
    catalog.js          Client-side product search (Week 2 version, kept for reference)
    enquiry.js          jQuery validation and AJAX submission for enquiry form
```

---

## Setup

### Requirements

- Python 3.10 or higher
- MySQL running via XAMPP or any local MySQL installation

### Install dependencies

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Git Bash)
source .venv/Scripts/activate

pip install -r requirements.txt
```

### Database setup

The app supports both MySQL and SQLite. By default, it uses SQLite for development (no external database required).

**For SQLite (default, no setup needed):**
```bash
python seed.py
python app.py
```

**For MySQL:**
1. Start MySQL from the XAMPP control panel
2. Open phpMyAdmin at `http://localhost/phpmyadmin`
3. Create a database named `shopeasy`
4. Set the `DATABASE_URL` environment variable:
   ```bash
   # Windows PowerShell
   $env:DATABASE_URL = "mysql+pymysql://root:@localhost/shopeasy"
   
   # Or create a .env file with:
   # DATABASE_URL=mysql+pymysql://root:@localhost/shopeasy
   ```
5. Run seed and app:
   ```bash
   python seed.py
   python app.py
   ```

The app will automatically use SQLite if no `DATABASE_URL` is set.

---

## Demo credentials

| Role  | Email                  | Password |
|-------|------------------------|----------|
| Admin | demo@shopeasy.com      | demo123  |

Only this account can access the admin panel at `/admin/`. Any other registered account is a regular user.

---

## Key routes

| URL | Description |
|-----|-------------|
| `/` | Homepage |
| `/products` | All products |
| `/products?category=Men` | Filtered by category |
| `/products?search=shirt` | Search by name |
| `/products?page=2` | Paginated results |
| `/product/<id>` | Product detail page |
| `/register` | Create an account |
| `/login` | Log in |
| `/logout` | Log out |
| `/enquiry` | POST endpoint for enquiry form (JSON) |
| `/admin/` | Admin dashboard (login required, admin only) |
| `/admin/categories` | Manage categories |
| `/admin/subcategories` | Manage subcategories |
| `/admin/products` | Manage products |
| `/admin/enquiries` | View submitted enquiries |

---

## How the main features work

**Template inheritance:** Every page extends `base.html` using Jinja2 blocks. The base file holds the navbar, flash messages, and footer. Individual pages only define their own content block. The admin panel has its own `base_admin.html` for the same reason.

**Authentication:** Passwords are hashed with `werkzeug.security.generate_password_hash` before being stored. On login, `check_password_hash` compares the input against the stored hash. The user's id and name are saved in Flask's session cookie on success.

**Admin access control:** The `admin_required` decorator on every admin route checks that the logged-in user's email matches the admin email constant. Any other user is redirected to the homepage with an error message.

**Category and subcategory structure:** Both are stored in the same `categories` table. Top-level categories have `parent_id = NULL`. Subcategories have `parent_id` set to their parent's id. The `Category` model has a self-referential relationship so `category.subcategories` and `subcategory.parent` work directly in code and templates.

**Product filtering:** When a category is selected, the app collects the category's own id and all its subcategory ids, then queries for products whose `subcategory_id` is in that set. This means filtering by "Men" returns products from Men's Shirts, Men's Jeans, and any other subcategory under Men.

**Pagination:** SQLAlchemy's `.paginate()` method takes a page number and a per-page limit. The current page is read from the URL query string. The template renders previous, next, and numbered page links, and preserves the active search and category filters across page changes.

**Enquiry form:** Validation runs client-side with jQuery before anything is sent. Each field is checked individually and Bootstrap's `is-invalid` class is applied to show error messages inline. On passing validation, `$.ajax()` sends the data as JSON to `/enquiry`. Flask validates again server-side, saves the record to the `enquiries` table, and returns a JSON response. jQuery then shows a success or error alert inside the modal without reloading the page.