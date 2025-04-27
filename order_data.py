"""
Sample order data for the e-commerce site.
This file contains fake order numbers, customer details, and order histories
to showcase how the system would work with real data.
"""

def get_orders():
    """Return a list of sample orders"""
    return [
        {
            "order_id": "ORD-166225567",
            "customer_id": "CUST-12345",
            "customer_name": "Alex Johnson",
            "date_placed": "2025-03-24T14:22:15",
            "status": "Processing",
            "total": 128.97,
            "items": [
                {
                    "product_id": 3,
                    "name": "Wireless Headphones",
                    "quantity": 1,
                    "price": 89.99,
                    "subtotal": 89.99
                },
                {
                    "product_id": 8,
                    "name": "Smart Watch",
                    "quantity": 1,
                    "price": 38.98,
                    "subtotal": 38.98
                }
            ],
            "shipping": {
                "method": "Standard",
                "cost": 4.99,
                "address": {
                    "street": "123 Main St",
                    "city": "Springfield",
                    "state": "IL",
                    "zip": "62704"
                },
                "tracking_number": "USPS9405511899561463892538",
                "estimated_delivery": "2025-03-29"
            },
            "payment": {
                "method": "Credit Card",
                "card_last4": "1234",
                "subtotal": 128.97,
                "tax": 7.74,
                "total": 141.70
            },
            "notes": "Customer requested gift wrapping"
        },
        {
            "order_id": "ORD-166225892",
            "customer_id": "CUST-67890",
            "customer_name": "Jamie Smith",
            "date_placed": "2025-03-25T09:45:30",
            "status": "Shipped",
            "total": 214.95,
            "items": [
                {
                    "product_id": 12,
                    "name": "Winter Coat",
                    "quantity": 1,
                    "price": 149.99,
                    "subtotal": 149.99
                },
                {
                    "product_id": 15,
                    "name": "Wool Scarf",
                    "quantity": 1,
                    "price": 29.99,
                    "subtotal": 29.99
                },
                {
                    "product_id": 18,
                    "name": "Leather Gloves",
                    "quantity": 1,
                    "price": 34.97,
                    "subtotal": 34.97
                }
            ],
            "shipping": {
                "method": "Express",
                "cost": 12.99,
                "address": {
                    "street": "456 Oak Avenue",
                    "city": "Portland",
                    "state": "OR",
                    "zip": "97204"
                },
                "tracking_number": "FDX7816935492",
                "estimated_delivery": "2025-03-27"
            },
            "payment": {
                "method": "PayPal",
                "subtotal": 214.95,
                "tax": 10.75,
                "total": 238.69
            },
            "notes": ""
        },
        {
            "order_id": "ORD-166226104",
            "customer_id": "CUST-24680",
            "customer_name": "Taylor Williams",
            "date_placed": "2025-03-26T16:32:10",
            "status": "Processing",
            "total": 319.96,
            "items": [
                {
                    "product_id": 21,
                    "name": "Coffee Table",
                    "quantity": 1,
                    "price": 199.99,
                    "subtotal": 199.99
                },
                {
                    "product_id": 24,
                    "name": "Table Lamp",
                    "quantity": 2,
                    "price": 59.99,
                    "subtotal": 119.98
                }
            ],
            "shipping": {
                "method": "Standard",
                "cost": 0,  # Free shipping
                "address": {
                    "street": "789 Pine Street, Apt 3B",
                    "city": "Austin",
                    "state": "TX",
                    "zip": "78704"
                },
                "tracking_number": "",  # Not shipped yet
                "estimated_delivery": "2025-04-01"
            },
            "payment": {
                "method": "Credit Card",
                "card_last4": "5678",
                "subtotal": 319.96,
                "tax": 26.40,
                "total": 346.36
            },
            "notes": "Call before delivery"
        },
        {
            "order_id": "ORD-166226438",
            "customer_id": "CUST-13579",
            "customer_name": "Morgan Lee",
            "date_placed": "2025-03-27T10:17:45",
            "status": "Confirmed",
            "total": 699.98,
            "items": [
                {
                    "product_id": 36,
                    "name": "4K Smart TV",
                    "quantity": 1,
                    "price": 699.98,
                    "subtotal": 699.98
                }
            ],
            "shipping": {
                "method": "Premium",
                "cost": 24.99,
                "address": {
                    "street": "1010 Maple Road",
                    "city": "Chicago",
                    "state": "IL",
                    "zip": "60614"
                },
                "tracking_number": "",  # Not shipped yet
                "estimated_delivery": "2025-04-02"
            },
            "payment": {
                "method": "Credit Card",
                "card_last4": "9012",
                "subtotal": 699.98,
                "tax": 63.00,
                "total": 787.97
            },
            "notes": "Signature required for delivery"
        }
    ]

def get_order_by_id(order_id):
    """Return a specific order by ID"""
    orders = get_orders()
    for order in orders:
        if order["order_id"] == order_id:
            return order
    return None

def get_customer_orders(customer_id):
    """Return all orders for a specific customer"""
    orders = get_orders()
    return [order for order in orders if order["customer_id"] == customer_id]

def get_orders_by_status(status):
    """Return all orders with a specific status"""
    orders = get_orders()
    return [order for order in orders if order["status"] == status]

def get_recent_orders(limit=5):
    """Return the most recent orders"""
    orders = get_orders()
    # Sort by date (newest first) and return the specified limit
    sorted_orders = sorted(orders, key=lambda x: x["date_placed"], reverse=True)
    return sorted_orders[:limit]

def cancel_order(order_id):
    """Cancel an order if it's in a cancellable state"""
    order = get_order_by_id(order_id)
    if not order:
        return {"success": False, "message": "Order not found"}
    
    # Only allow cancellation for Processing or Confirmed orders
    if order["status"] == "Confirmed":
        # In a real system, we would update the database and remove from orders list
        # For this demo, we'll update the order in memory
        order["status"] = "Cancelled"
        return {"success": True, "message": "Confirmed order has been cancelled successfully and removed from your orders."}
    elif order["status"] == "Processing":
        # In a real system, we would update the database
        # For this demo, we'll update the order in memory
        order["status"] = "Cancelled"
        return {"success": True, "message": "Processing order has been cancelled successfully."}
    elif order["status"] == "Shipped":
        return {"success": False, "message": "Cannot cancel a shipped order. Please contact customer support for return options."}
    else:
        return {"success": False, "message": f"Cannot cancel order with status: {order['status']}."}