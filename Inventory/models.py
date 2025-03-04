from django.db import models

# ✅ Item Model (Updated with Additional Fields)
class Item(models.Model):
    item_code = models.CharField(max_length=100, unique=True)  # Unique constraint to avoid duplicates
    product_title = models.CharField(max_length=200)

    # Quantities
    rim_quantity = models.IntegerField(default=0)  # Rim/Dozen Quantity
    sheet_quantity = models.IntegerField(default=0)  # Sheet/Piece Quantity
    only_sheet_piece = models.IntegerField(default=0)  # Only Sheet Piece
    total_sheet_piece = models.IntegerField(default=0)  # Total Sheet Piece

    # Prices
    rim_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Rim/Dozen Price
    sheet_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Sheet/Piece Price
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Total Amount

    # Remarks
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.item_code} - {self.product_title}"
class PurchaseReceive(models.Model):
    # 1. Company Name
    company_name = models.CharField(max_length=255)

    # 2. Order Date
    order_date = models.DateField()

    # 3. Order No
    order_no = models.CharField(max_length=50, unique=True)

    # 4. Delivery Date
    delivery_date = models.DateField(blank=True, null=True)

    # 5. Transport
    TRANSPORT_CHOICES = [
        ("Company Transport", "Company Transport"),
        ("Sharif Paper & Stationary Transport", "Sharif Paper & Stationary Transport"),
        ("Other Transport", "Other Transport"),
    ]
    transport = models.CharField(max_length=100, choices=TRANSPORT_CHOICES)

    # 6. Vehicle No
    vehicle_no = models.CharField(max_length=50, blank=True, null=True)

    # 7. Driver Name
    driver_name = models.CharField(max_length=100, blank=True, null=True)

    # 8. Driver Mobile No
    driver_mobile = models.CharField(max_length=15, blank=True, null=True)

    # 9. Invoice/Challan Date
    invoice_challan_date = models.DateField()

    # 10. Invoice/Challan No
    invoice_no = models.CharField(max_length=100, unique=True)

    # 11. Product Entry Date
    product_entry_date = models.DateField()

    # 12. Godown No
    godown_no = models.CharField(max_length=50, blank=True, null=True)

    # 13. Foreign Key to Item
    name_of_product = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, blank=True)

    # 14. Purchase Challan Date
    purchase_challan_date = models.DateField()

    # 15. Supplier
    supplier = models.CharField(max_length=255)

    # 16. Kind of Product
    kind_of_product = models.CharField(max_length=255)

    # 17. Product Type (Local or Import)
    product_type = models.CharField(max_length=50, choices=[('Local', 'Local'), ('Import', 'Import')])

    # 18. Remarks 1
    remarks_1 = models.TextField(blank=True, null=True)

    # 19. Remarks 2
    remarks_2 = models.TextField(blank=True, null=True)

    def __str__(self):
        # Return a string representation of the purchase receipt
        return f"{self.supplier} - {self.name_of_product.product_title if self.name_of_product else 'Unknown Product'}"


### ✅ Payment Information Model (Tracks Supplier Payments)
class PaymentInformation(models.Model):
    supplier = models.CharField(max_length=255)  # Company/Supplier Name
    previous_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    today_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Invoice/Challan Amount
    today_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Today Paid Amount

    # Payment Mode
    paid_by = models.CharField(
        max_length=50,
        choices=[('Cash', 'Cash'), ('Cheque', 'Cheque'), ('Bank Transfer', 'Bank Transfer')]
    )
    bank_name = models.CharField(max_length=255, blank=True, null=True)  # New Field
    account_no = models.CharField(max_length=255, blank=True, null=True)  # New Field
    cheque_no = models.CharField(max_length=100, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)

    # Final Amounts
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New Field
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New Field

    def __str__(self):
        return f"{self.supplier} - Paid: {self.today_paid} by {self.paid_by}"
