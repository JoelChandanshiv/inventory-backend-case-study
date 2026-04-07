@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.json or {}
        # Basic validation
        required_fields = ['name', 'sku', 'price']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400
        # Price validation
        try:
            price = float(data['price'])
            if price < 0:
                return {"error": "Price cannot be negative"}, 400
        except:
            return {"error": "Invalid price format"}, 400
        # SKU uniqueness check
        if Product.query.filter_by(sku=data['sku']).first():
            return {"error": "SKU already exists"}, 400
        # Create product (no warehouse binding here)
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=price
        )
        db.session.add(product)
        db.session.flush()  # ensures product.id is available
        # Optional inventory creation
        if data.get('warehouse_id') and data.get('initial_quantity') is not None:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data['initial_quantity']
            )
            db.session.add(inventory)
        db.session.commit()
        return {
            "message": "Product created",
            "product_id": product.id
        }, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Something went wrong"}, 500
