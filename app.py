from flask import Flask, render_template, request, redirect, jsonify, session ,url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'aX93qhd987y##12JKLlk9asdkj@!#KJLWq'

app.config["MONGO_URI"] = "mongodb://localhost:27017/bookstore"
mongo = PyMongo(app)

@app.route('/')
def index():
    books = mongo.db.books.find()
    return render_template('index.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = mongo.db.users.find_one({'email': email, 'password': password})
        if user:
            return jsonify({'message': 'Login Successful'}), 200
        return jsonify({'message': 'Invalid Credentials'}), 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('username')  
        email = data.get('email')
        dob = data.get('dob')
        gender = data.get('gender')
        phone = data.get('phno')

        if name and email and phone:
            mongo.db.users.insert_one({
                'name': name,
                'email': email,
                'dob': dob,
                'gender': gender,
                'phone': phone
            })
            return jsonify({'message': 'Registered Successfully'}), 201
        return jsonify({'message': 'Missing Fields'}), 400
    return render_template('register.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Initialize cart in session
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = []

@app.route('/cart')
def view_cart():
    initialize_cart()
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template('cart.html', cart=session['cart'], total=total)

@app.route('/add-to-cart/<string:book_id>')
def add_to_cart(book_id):
    initialize_cart()
    book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    if book:
        for item in session['cart']:
            if item['id'] == str(book['_id']):
                item['quantity'] += 1
            break
    else:
        session['cart'].append({
            "id": str(book['_id']),
            "title": book['title'],
            "price": book['price'],
            "quantity": 1
        })
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/remove-from-cart/<string:book_id>')
def remove_from_cart(book_id):
    initialize_cart()
    session['cart'] = [item for item in session['cart'] if item['id'] != book_id]
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session.modified = True
    return redirect(url_for('view_cart'))
@app.route('/book/<string:book_id>')
def book_datail(book_id):
    book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    if book:
        return render_template("book_detail.html", book=book)
    else:
        return "Book not found",404
    return render_template("book_detail.html", book=book)

@app.route('/api/admin/stats')
def admin_stats():
    users = mongo.db.users.count_documents({})
    books = mongo.db.books.count_documents({})
    orders = mongo.db.orders.count_documents({})
    return jsonify({'users': users, 'books': books, 'orders': orders})

if __name__ == '__main__':
    app.run(debug=True)
