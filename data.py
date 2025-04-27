# In-memory data storage for the e-commerce application

# Product data
products = [
    # Electronics Category
    {
        "id": 1,
        "name": "SoundWave Pro Headphones",
        "description": "Premium wireless headphones with active noise cancellation, 30-hour battery life, and plush memory foam ear cushions.",
        "price": 149.99,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.7,
        "stock": 25
    },
    {
        "id": 2,
        "name": "UltraPhone 15",
        "description": "Flagship smartphone with 6.7-inch AMOLED display, 256GB storage, 5G capability, and revolutionary AI-powered camera system.",
        "price": 899.99,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.9,
        "stock": 18
    },
    {
        "id": 3,
        "name": "FitTrack Luxe Smartwatch",
        "description": "Premium smartwatch with health monitoring, GPS, 7-day battery life, and customizable watch faces. Water-resistant up to 50m.",
        "price": 229.99,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.6,
        "stock": 32
    },
    {
        "id": 4,
        "name": "PowerBook Ultra Laptop",
        "description": "Ultra-thin laptop with 16GB RAM, 1TB SSD, dedicated graphics card, and stunning 4K display perfect for professionals.",
        "price": 1299.99,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.8,
        "stock": 12
    },
    {
        "id": 5,
        "name": "GameStation 5 Console",
        "description": "Next-gen gaming console with 1TB storage, 4K gaming at 120fps, ray tracing, and includes one wireless controller.",
        "price": 499.99,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1605901309584-818e25960a8f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.9,
        "stock": 7
    },
    
    # Clothing Category
    {
        "id": 6,
        "name": "Premium Cotton Crew Neck",
        "description": "Ultra-soft 100% organic cotton t-shirt with a modern slim fit. Available in multiple colors.",
        "price": 29.99,
        "category": "Clothing",
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.5,
        "stock": 120
    },
    {
        "id": 7,
        "name": "Designer Denim Jeans",
        "description": "Premium stretch denim jeans with perfect slim fit and vintage wash. Sustainably manufactured.",
        "price": 79.99,
        "category": "Clothing",
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.6,
        "stock": 45
    },
    {
        "id": 8,
        "name": "All-Weather Winter Jacket",
        "description": "Waterproof and windproof jacket with thermal insulation. Perfect for outdoor adventures in any weather.",
        "price": 149.99,
        "category": "Clothing",
        "image_url": "https://images.unsplash.com/photo-1544923246-77307dd654cb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.8,
        "stock": 28
    },
    {
        "id": 9,
        "name": "Luxury Cashmere Sweater",
        "description": "Ultra-soft 100% cashmere sweater that provides exceptional warmth without the bulk. Timeless design.",
        "price": 129.99,
        "category": "Clothing",
        "image_url": "https://images.unsplash.com/photo-1609587312208-cea54be969e7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.7,
        "stock": 22
    },
    
    # Watches Category
    {
        "id": 10,
        "name": "Classic Chronograph Watch",
        "description": "Elegant stainless steel watch with chronograph function, sapphire crystal, and genuine leather strap.",
        "price": 249.99,
        "category": "Watches",
        "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.8,
        "stock": 18
    },
    {
        "id": 11,
        "name": "Minimalist Swiss Watch",
        "description": "Ultra-thin Swiss-made watch with minimalist design, premium leather band, and scratch-resistant crystal.",
        "price": 199.99,
        "category": "Watches",
        "image_url": "https://images.unsplash.com/photo-1585123334904-845d60e97b29?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.5,
        "stock": 24
    },
    {
        "id": 12,
        "name": "Dive Master Pro Watch",
        "description": "Professional dive watch water-resistant to 300m with rotating bezel, luminous indices, and stainless steel bracelet.",
        "price": 349.99,
        "category": "Watches",
        "image_url": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80",
        "rating": 4.9,
        "stock": 10
    },
    
    # Home Products Category
    {
        "id": 13,
        "name": "Modern Scandinavian Sofa",
        "description": "Elegant mid-century modern sofa with oak legs, premium upholstery, and plush cushions for ultimate comfort and style.",
        "price": 899.99,
        "category": "Home",
        "image_url": "https://images.unsplash.com/photo-1567016432779-094069958ea5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "rating": 4.8,
        "stock": 8
    },
    {
        "id": 14,
        "name": "Minimalist Floating Shelf Set",
        "description": "Set of 3 premium wooden floating shelves with hidden brackets for a clean, contemporary look. Perfect for displaying decor items.",
        "price": 129.99,
        "category": "Home",
        "image_url": "https://images.unsplash.com/photo-1591129841117-3adfd313a592?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "rating": 4.6,
        "stock": 20
    },
    {
        "id": 15,
        "name": "Artisan Ceramic Vase Collection",
        "description": "Set of 3 handcrafted ceramic vases in complementary earth tones, each with unique textures and finishes. Perfect centerpiece for any room.",
        "price": 179.99,
        "category": "Home",
        "image_url": "https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "rating": 4.9,
        "stock": 12
    },
    {
        "id": 16,
        "name": "Luxury Velvet Accent Chair",
        "description": "Statement accent chair with plush velvet upholstery, gold-toned metal legs, and ergonomic design for both style and comfort.",
        "price": 449.99,
        "category": "Home",
        "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "rating": 4.7,
        "stock": 7
    },
    {
        "id": 17,
        "name": "Nordic Pendant Light",
        "description": "Modern pendant light with natural wood finish and adjustable height. Provides warm ambient lighting for dining rooms or kitchen islands.",
        "price": 189.99,
        "category": "Home",
        "image_url": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "rating": 4.5,
        "stock": 15
    },
    {
        "id": 18,
        "name": "Geometric Area Rug",
        "description": "Soft, plush area rug with contemporary geometric patterns. Made from premium materials with non-slip backing. Size: 5'x7'.",
        "price": 249.99,
        "category": "Home",
        "image_url": "https://images.unsplash.com/photo-1575414774607-989bac80aa0e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "rating": 4.8,
        "stock": 10
    }
]

# Categories
categories = [
    "Electronics",
    "Clothing",
    "Watches",
    "Home"
]

# FAQs
faqs = [
    {
        "question": "How long does shipping take?",
        "answer": "Standard shipping takes 3-5 business days. Express shipping is available for 1-2 business day delivery."
    },
    {
        "question": "What is your return policy?",
        "answer": "We offer a 30-day return policy for most items. Products must be in original condition with tags attached."
    },
    {
        "question": "Do you ship internationally?",
        "answer": "Yes, we ship to most countries worldwide. International shipping typically takes 7-14 business days."
    },
    {
        "question": "How can I track my order?",
        "answer": "Once your order ships, you'll receive a tracking number via email that you can use to monitor your delivery."
    },
    {
        "question": "Do you offer gift wrapping?",
        "answer": "Yes, gift wrapping is available for an additional $5 per item. You can select this option during checkout."
    }
]

# Data access functions
def get_all_products():
    return products

def get_product_by_id(product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    return None

def get_products_by_category(category):
    return [product for product in products if product["category"] == category]

def search_products(query):
    query = query.lower()
    return [
        product for product in products 
        if query in product["name"].lower() or query in product["description"].lower()
    ]

def get_all_categories():
    return categories

def get_faqs():
    return faqs
