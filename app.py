import os
import logging
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from flask_cors import CORS
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from email_validator import validate_email, EmailNotValidError

import data
from chat import get_groq_response
import order_data
from database import db
from models import User, Order, OrderItem, Address

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register all blueprints
def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    CORS(app)

# Main routes
@main_bp.route('/')
def index():
    return render_template('index.html')

# Add catch-all route for client-side routing
@main_bp.route('/<path:path>')
def catch_all(path):
    if path.startswith('api/'):
        return jsonify({"error": "API endpoint not found"}), 404
    return render_template('index.html')

# API Routes
@main_bp.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    search = request.args.get('search')
    
    if category:
        products = data.get_products_by_category(category)
    elif search:
        products = data.search_products(search)
    else:
        products = data.get_all_products()
        
    return jsonify(products)

@main_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = data.get_product_by_id(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@main_bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = data.get_all_categories()
    return jsonify(categories)

@main_bp.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def handle_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    if request.method == 'GET':
        cart_items = []
        for item in session['cart']:
            product = data.get_product_by_id(item['product_id'])
            if product:
                cart_item = product.copy()
                cart_item['quantity'] = item['quantity']
                cart_items.append(cart_item)
        return jsonify(cart_items)
    
    elif request.method == 'POST':
        cart_item = request.json
        product_id = cart_item.get('product_id')
        quantity = cart_item.get('quantity', 1)
        
        # Check if product exists
        product = data.get_product_by_id(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        # Check if product is already in cart
        for item in session['cart']:
            if item['product_id'] == product_id:
                # Set the quantity directly instead of incrementing it
                item['quantity'] = quantity
                session.modified = True
                return jsonify({"message": "Cart updated"})
        
        # Add new item to cart
        session['cart'].append({'product_id': product_id, 'quantity': quantity})
        session.modified = True
        return jsonify({"message": "Item added to cart"})
    
    elif request.method == 'DELETE':
        cart_item = request.json
        product_id = cart_item.get('product_id')
        
        # Remove item from cart
        session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
        session.modified = True
        return jsonify({"message": "Item removed from cart"})

@main_bp.route('/api/checkout', methods=['POST'])
def checkout():
    # Get data from request
    data = request.json
    items = data.get('items', [])
    customer = data.get('customer', {})
    
    if not items:
        return jsonify({"error": "No items in cart"}), 400
    
    # Calculate total
    total = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
    
    # Generate a unique order ID (in a real app, this would be more sophisticated)
    import random
    import string
    order_id = 'ORD-' + ''.join(random.choices(string.digits, k=9))
    
    # Create order in database if user is authenticated
    if current_user.is_authenticated:
        try:
            # Create new order
            new_order = Order(
                order_id=order_id,
                user_id=current_user.id,
                status='Confirmed',
                total=total,
                payment_method='Credit Card',
                card_last4=customer.get('cardNumber', '')[-4:] if customer.get('cardNumber') else None
            )
            db.session.add(new_order)
            db.session.flush()  # Get the ID before committing
            
            # Add order items
            for item in items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item.get('id'),
                    name=item.get('name'),
                    quantity=item.get('quantity', 1),
                    price=item.get('price', 0)
                )
                db.session.add(order_item)
            
            # Add shipping address if provided
            if all(k in customer for k in ['address', 'city', 'state', 'zipCode']):
                # Check if the user already has this address
                address = Address.query.filter_by(
                    user_id=current_user.id,
                    street=customer.get('address'),
                    city=customer.get('city'),
                    state=customer.get('state'),
                    zip=customer.get('zipCode')
                ).first()
                
                if not address:
                    address = Address(
                        user_id=current_user.id,
                        street=customer.get('address'),
                        city=customer.get('city'),
                        state=customer.get('state'),
                        zip=customer.get('zipCode'),
                        is_default=False
                    )
                    db.session.add(address)
                    db.session.flush()
                
                # Associate address with order
                new_order.shipping_address_id = address.id
            
            # Commit the transaction
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating order: {str(e)}")
            return jsonify({"error": "Failed to create order"}), 500
    
    # Clear the cart
    session['cart'] = []
    session.modified = True
    
    return jsonify({
        "message": "Order placed successfully", 
        "order_id": order_id
    })

@main_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Get response from Groq
    try:
        response = get_groq_response(user_message)
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error getting Groq response: {str(e)}")
        return jsonify({"error": "Failed to get response from support system"}), 500

@main_bp.route('/api/faqs', methods=['GET'])
def get_faqs():
    faqs = data.get_faqs()
    return jsonify(faqs)

# Order-related routes
@main_bp.route('/api/orders', methods=['GET'])
def get_orders():
    if current_user.is_authenticated:
        # Get orders from the database for the logged in user
        orders = Order.query.filter_by(user_id=current_user.id).all()
        orders_list = []
        for order in orders:
            order_dict = {
                "order_id": order.order_id,
                "date_placed": order.date_placed.isoformat(),
                "status": order.status,
                "total": order.total,
                "tracking_number": order.tracking_number
            }
            orders_list.append(order_dict)
        return jsonify(orders_list)
    else:
        # For users who aren't logged in, return sample orders
        orders = order_data.get_orders()
        return jsonify(orders)

@main_bp.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    if current_user.is_authenticated:
        # First try to get from database
        order = Order.query.filter_by(order_id=order_id, user_id=current_user.id).first()
        if order:
            # Convert to dictionary
            order_dict = {
                "order_id": order.order_id,
                "customer_id": current_user.id,
                "customer_name": f"{current_user.first_name} {current_user.last_name}",
                "date_placed": order.date_placed.isoformat(),
                "status": order.status,
                "total": order.total,
                "items": [],
                "shipping": {
                    "method": "Standard",
                    "cost": 4.99,
                    "address": {},
                    "tracking_number": order.tracking_number
                },
                "payment": {
                    "method": order.payment_method,
                    "card_last4": order.card_last4,
                    "subtotal": order.total - 4.99,
                    "tax": (order.total - 4.99) * 0.06,
                    "total": order.total
                }
            }
            
            # Get order items
            items = OrderItem.query.filter_by(order_id=order.id).all()
            for item in items:
                order_dict["items"].append({
                    "product_id": item.product_id,
                    "name": item.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "subtotal": item.subtotal
                })
            
            # Get shipping address if available
            if order.shipping_address_id:
                address = Address.query.get(order.shipping_address_id)
                if address:
                    order_dict["shipping"]["address"] = {
                        "street": address.street,
                        "city": address.city,
                        "state": address.state,
                        "zip": address.zip
                    }
            
            return jsonify(order_dict)
    
    # Fall back to sample data
    order = order_data.get_order_by_id(order_id)
    if order:
        return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

@main_bp.route('/api/orders/recent', methods=['GET'])
def get_recent_orders():
    limit = request.args.get('limit', 5, type=int)
    if current_user.is_authenticated:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date_placed.desc()).limit(limit).all()
        orders_list = []
        for order in orders:
            order_dict = {
                "order_id": order.order_id,
                "date_placed": order.date_placed.isoformat(),
                "status": order.status,
                "total": order.total
            }
            orders_list.append(order_dict)
        return jsonify(orders_list)
    
    # Fall back to sample data
    orders = order_data.get_recent_orders(limit)
    return jsonify(orders)

@main_bp.route('/api/orders/status/<status>', methods=['GET'])
def get_orders_by_status(status):
    if current_user.is_authenticated:
        orders = Order.query.filter_by(user_id=current_user.id, status=status).all()
        orders_list = []
        for order in orders:
            order_dict = {
                "order_id": order.order_id,
                "date_placed": order.date_placed.isoformat(),
                "status": order.status,
                "total": order.total
            }
            orders_list.append(order_dict)
        return jsonify(orders_list)
    
    # Fall back to sample data
    orders = order_data.get_orders_by_status(status)
    return jsonify(orders)

@main_bp.route('/api/orders/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    if current_user.is_authenticated:
        order = Order.query.filter_by(order_id=order_id, user_id=current_user.id).first()
        if order:
            if order.status == "Confirmed":
                order.status = "Cancelled"
                db.session.commit()
                return jsonify({"success": True, "message": "Confirmed order has been cancelled successfully and removed from your orders."})
            elif order.status == "Processing":
                order.status = "Cancelled"
                db.session.commit()
                return jsonify({"success": True, "message": "Processing order has been cancelled successfully."})
            elif order.status == "Shipped":
                return jsonify({"success": False, "message": "Cannot cancel a shipped order. Please contact customer support for return options."})
            else:
                return jsonify({"success": False, "message": f"Cannot cancel order with status: {order.status}."})
    
    # Fall back to sample data
    result = order_data.cancel_order(order_id)
    if result["success"]:
        return jsonify(result)
    else:
        return jsonify(result), 400

# Form classes for authentication
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')
            
    def validate_password(self, password):
        """
        Validate password strength:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one number
        - Contains at least one special character (!@#$%^&*()_-+=<>?)
        """
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
            
        if not any(char.isupper() for char in password.data):
            raise ValidationError('Password must contain at least one uppercase letter.')
            
        if not any(char.islower() for char in password.data):
            raise ValidationError('Password must contain at least one lowercase letter.')
            
        if not any(char.isdigit() for char in password.data):
            raise ValidationError('Password must contain at least one number.')
            
        if not any(char in '!@#$%^&*()_-+=<>?' for char in password.data):
            raise ValidationError('Password must contain at least one special character (!@#$%^&*()_-+=<>?).')

class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])

# API routes for authentication
@main_bp.route('/api/auth/status')
def auth_status():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'username': current_user.username,
                'email': current_user.email,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name
            }
        })
    else:
        return jsonify({
            'authenticated': False
        })

# Authentication routes
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            flash('Logged in successfully!', 'success')
            return redirect(next_page)
        flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # In a real app, you would send a password reset email
            # For this demo, we'll just display a message
            flash('If your email is registered, you will receive password reset instructions.', 'info')
        else:
            # Don't reveal if the email is not registered for security reasons
            flash('If your email is registered, you will receive password reset instructions.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)
