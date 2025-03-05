from django.db import models
from master.models import*


class Purchase(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invoices")
    order_date = models.DateField()
    order_no = models.CharField(max_length=100, unique=True)
    invoice_challan_date = models.DateField()
    invoice_challan_no = models.CharField(max_length=100, unique=True)
    transport_type = models.CharField(max_length=100)
    delivery_date = models.DateField()
    delivery_no = models.CharField(max_length=100, unique=True)
    driver_name = models.CharField(max_length=100,blank=True,null=True)
    driver_mobile_no = models.CharField(max_length=15,blank=True,null=True)
    vehicle_no = models.CharField(max_length=50,blank=True,null=True)
    godown=models.ForeignKey(Godown, on_delete=models.CASCADE, related_name="godwons")
    entry_by = models.CharField(max_length=100,blank=True,null=True)
    remarks = models.TextField(blank=True, null=True)

    previous_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    invoice_challan_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    today_paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_type =models.CharField(max_length=100)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=100, blank=True, null=True)
    cheque_no = models.CharField(max_length=100, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    def save(self, *args, **kwargs):

        total_due = self.invoice_challan_amount - self.today_paid_amount
        self.balance_amount=total_due+ self.company.previous_due
        if self.pk is None:
            self.company.previous_due = self.balance_amount
            self.company.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_challan_no} - {self.company.company_name}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Added the ForeignKey to Product
    purchase_price= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rim = models.IntegerField(default=0)
    dozen=models.IntegerField(default=0)
    only_sheet_piece = models.IntegerField(default=0)
    total_sheet_piece = models.IntegerField(default=0)
    per_rim_or_dozen_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    per_sheet_or_piece_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    labour_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    road_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    total_extra_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    total_purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    per_rim_or_dozen_additional_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_sheet_or_piece_additional_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    per_rim_or_dozen_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_sheet_or_piece_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    per_rim_or_dozen_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    per_rim_or_dozen_sell_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_sheet_or_piece_sell_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Fetch the stock associated with the product
        try:
            stock = Stock.objects.get(product=self.product)  # Get the stock for the product
        except Stock.DoesNotExist:
            pass
        if stock:
            stock.update_stock(
                self.rim, self.dozen, self.sheet_or_piece, 
                self.per_rim_or_dozen_total_cost, self.per_sheet_or_piece_total_cost, 
                self.per_rim_or_dozen_sell_amount,self.per_sheet_or_piece_sell_amount
            )
            stock.last_per_rim_or_dozen_price = self.per_rim_or_dozen_price
            stock.last_per_sheet_or_piece_price = self.per_sheet_or_piece_price
            stock.save()

        self.total_purchase_price = (
           self.sheet_or_piece_total_cost +
            self.total_extra_cost
        )
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.product.product_code} - {self.product.product_description}"


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the product
    rim = models.IntegerField(default=0)  # Stock of rims
    dozen = models.IntegerField(default=0)  # Stock of dozens
    sheet_or_piece = models.IntegerField(default=0)  # Stock of sheets/pieces
    last_per_rim_or_dozen_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    last_per_sheet_or_piece_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    per_rim_or_dozen_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  
    per_sheet_or_piece_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  

    per_rim_or_dozen_sell_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) 
    per_sheet_or_piece_sell_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)


    def update_stock(self, purchased_rim, purchased_dozen, purchased_sheet_or_piece,
     per_rim_or_dozen_purchase_price,per_sheet_or_piece_purchase_price,per_rim_or_dozen_sale_price,
     per_sheet_or_piece_sale_price):
        self.rim += purchased_rim
        self.dozen += purchased_dozen
        self.sheet_or_piece += purchased_sheet_or_piece
        
        # Update the prices to the latest values
        self.per_rim_or_dozen_total_cost = per_rim_or_dozen_purchase_price
        self.per_sheet_or_piece_total_cost = per_sheet_or_piece_purchase_price
        self.per_rim_or_dozen_sell_amount = per_rim_or_dozen_sale_price
        self.per_sheet_or_piece_sell_amount = per_sheet_or_piece_sale_price

        
        self.save()

    def reduce_stock(self, rim_sold, dozen_sold, sheet_or_piece_sold):
        """Reduce stock after a sale"""
        self.rim -= rim_sold
        self.dozen -= dozen_sold
        self.sheet_or_piece -= sheet_or_piece_sold
        
        if self.rim < 0 or self.dozen < 0 or self.sheet_or_piece < 0:
            raise ValueError("Not enough stock to complete the sale")

        self.save()

    def __str__(self):
        return f"{self.product.product_code} - {self.product.product_description} (Stock: {self.rim} rims, {self.dozen} dozens, {self.sheet_or_piece} sheets/pieces)"

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer")
    sale_date = models.DateField(auto_now_add=True)
    reference = models.CharField(max_length=255, blank=True,null=True)
    remarks = models.CharField(max_length=255, blank=True,null=True)

    previous_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    invoice_total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    today_paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_type =models.CharField(max_length=100)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=100, blank=True, null=True)
    cheque_no = models.CharField(max_length=100, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    def save(self, *args, **kwargs):

        total_due = self.invoice_total_amount - self.today_paid_amount
        self.balance_amount=total_due+ self.customer.due_amount
        if self.pk is None:
            self.customer.due_amount = self.balance_amount
            self.customer.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.id} - {self.customer_name} - {self.product.product_description}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sale_items")
    product = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="sale_products")
    rim_sold = models.IntegerField(default=0)
    dozen_sold = models.IntegerField(default=0)
    sheet_or_piece_sold = models.IntegerField(default=0)
    per_rim_or_dozen_sell_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_sheet_or_piece_sell_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        
        self.product.reduce_stock(self.rim_sold, self.dozen_sold, self.sheet_or_piece_sold)  # Call reduce_stock to update the stock


    def __str__(self):
        return f"Sale Item {self.product.product_code} - {self.product.product_description}"
