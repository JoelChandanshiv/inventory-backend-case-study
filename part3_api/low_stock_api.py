from datetime import datetime, timedelta
@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    try:
        alerts = []
        # Check if company exists
        company = Company.query.get(company_id)
        if not company:
            return {"error": "Company not found"}, 404
        # Define recent sales window (last 30 days)
        recent_date = datetime.utcnow() - timedelta(days=30)
        results = db.session.query(
            Product.id,
            Product.name,
            Product.sku,
            Warehouse.id,
            Warehouse.name,
            Inventory.quantity,
            Product.low_stock_threshold,
            Supplier.id,
            Supplier.name,
            Supplier.contact_email
        ).join(Inventory, Product.id == Inventory.product_id)\
         .join(Warehouse, Warehouse.id == Inventory.warehouse_id)\
         .join(ProductSupplier, Product.id == ProductSupplier.product_id)\
         .join(Supplier, Supplier.id == ProductSupplier.supplier_id)\
         .filter(Product.company_id == company_id)\
         .all()
        for row in results:
            product_id, pname, sku, wid, wname, qty, threshold, sid, sname, email = row
            # Check recent sales activity
            recent_sales = db.session.query(Sales)\
                .filter(Sales.product_id == product_id)\
                .filter(Sales.created_at >= recent_date)\
                .count()
            if recent_sales == 0:
                continue
            # Check low stock condition
            if qty < threshold:
                # Estimate daily sales rate
                total_sales = db.session.query(Sales.quantity)\
                    .filter(Sales.product_id == product_id)\
                    .filter(Sales.created_at >= recent_date)\
                    .all()
                total_quantity_sold = sum([s[0] for s in total_sales]) if total_sales else 0
                avg_daily_sales = total_quantity_sold / 30 if total_quantity_sold > 0 else 0
                # Avoid division by zero
                days_until_stockout = int(qty / avg_daily_sales) if avg_daily_sales > 0 else None
                alerts.append({
                    "product_id": product_id,
                    "product_name": pname,
                    "sku": sku,
                    "warehouse_id": wid,
                    "warehouse_name": wname,
                    "current_stock": qty,
                    "threshold": threshold,
                    "days_until_stockout": days_until_stockout,
                    "supplier": {
                        "id": sid,
                        "name": sname,
                        "contact_email": email
                    } if sid else None
                })
        return {
            "alerts": alerts,
            "total_alerts": len(alerts)
        }, 200
    except Exception as e:
        return {"error": "Internal server error"}, 500
