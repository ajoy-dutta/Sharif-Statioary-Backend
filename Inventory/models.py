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
        self.previous_due=self.company.previous_due
        total_due = self.invoice_challan_amount - self.today_paid_amount
        self.balance_amount=total_due+ self.company.previous_due
        self.company.previous_due = self.balance_amount
        self.company.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_challan_no} - {self.company.company_name}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rim = models.IntegerField(default=0)
    dozen = models.IntegerField(default=0)
    only_sheet_or_piece = models.IntegerField(default=0)
    total_sheet_or_piece = models.IntegerField(default=0)
    per_rim_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    per_dozen_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    per_sheet_or_piece_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    additional_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    per_rim_sell_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_dozen_sell_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_sheet_or_piece_sell_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def delete(self, *args, **kwargs):
        """Reduce stock before deleting a purchase item."""
        stock, created = Stock.objects.get_or_create(product=self.product)

        stock.rim -= self.rim
        stock.dozen -= self.dozen
        stock.sheet_or_piece -= self.only_sheet_or_piece
        stock.save()

        self.purchase.invoice_challan_amount = self.purchase.items.aggregate(
            total=models.Sum('purchase_price')
        )['total'] or 0  

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Ensure stock updates correctly when modifying a purchase item."""
        if self.pk:  # If editing an existing item
            old_item = PurchaseItem.objects.get(pk=self.pk)
            stock, _ = Stock.objects.get_or_create(product=self.product)
            stock.rim -= old_item.rim
            stock.dozen -= old_item.dozen
            stock.sheet_or_piece -= old_item.only_sheet_or_piece
            stock.save()

        if self.rim > 0:
            self.total_sheet_or_piece = self.rim * 500 + self.only_sheet_or_piece
        elif self.dozen > 0:
            self.total_sheet_or_piece = self.dozen * 12 + self.only_sheet_or_piece
        else:
            self.total_sheet_or_piece = self.only_sheet_or_piece  # Default to the given pieces

        if self.total_sheet_or_piece > 0:
            self.per_sheet_or_piece_price = self.purchase_price / self.total_sheet_or_piece
        else:
            self.per_sheet_or_piece_price = 0  
        if self.rim > 0:
            self.per_rim_price = self.per_sheet_or_piece_price * 500
            self.per_rim_sell_price = (self.purchase_price + self.additional_cost + self.profit) / self.total_sheet_or_piece * 500

        if self.dozen > 0:
            self.per_dozen_price = self.per_sheet_or_piece_price * 12
            self.per_dozen_sell_price = (self.purchase_price + self.additional_cost + self.profit) / self.total_sheet_or_piece * 12

        per_sheet_or_piece_total_cost = (self.purchase_price + self.additional_cost) / self.total_sheet_or_piece if self.total_sheet_or_piece > 0 else 0

        stock, _ = Stock.objects.get_or_create(product=self.product)
        stock.update_stock(
            self.rim, self.dozen, self.only_sheet_or_piece, 
            self.per_sheet_or_piece_price, per_sheet_or_piece_total_cost
        )
        stock.last_per_rim_or_dozen_price = self.per_rim_price
        stock.last_per_sheet_or_piece_price = self.per_sheet_or_piece_price
        stock.save()

        super().save(*args, **kwargs)

        self.purchase.invoice_challan_amount = self.purchase.items.aggregate(
            total=models.Sum('purchase_price')
        )['total'] or 0  
        self.purchase.save()

    def __str__(self):
        return f"{self.product.product_code} - {self.product.product_name}"


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rim = models.IntegerField(default=0) 
    dozen = models.IntegerField(default=0)
    sheet_or_piece = models.IntegerField(default=0) 
    last_per_rim_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_rim_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)   

    last_per_dozen_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_dozen_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  

    last_per_sheet_or_piece_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_sheet_or_piece_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  


    def update_stock(self, purchased_rim, purchased_dozen, only_sheet_or_piece,per_sheet_or_piece_price,
     per_sheet_or_piece_total_cost):
        self.rim += purchased_rim
        self.dozen += purchased_dozen
        self.sheet_or_piece += only_sheet_or_piece
        self.last_per_sheet_or_piece_price=per_sheet_or_piece_price
        self.per_sheet_or_piece_total_cost=per_sheet_or_piece_total_cost

        if purchased_rim>0:
            self.last_per_rim_price=per_sheet_or_piece_price*500
            self.per_rim_total_cost=per_sheet_or_piece_total_cost*500

        if purchased_dozen>0:
            self.last_per_dozen_price=per_sheet_or_piece_price*12
            self.per_dozen_total_cost=per_sheet_or_piece_total_cost*12
        
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
        return f"{self.product.product_code} - {self.product.product_name} (Stock: {self.rim} rims, {self.dozen} dozens, {self.sheet_or_piece} sheets/pieces)"

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
        self.previous_due = self.customer.due_amount

        total_due = self.invoice_total_amount - self.today_paid_amount
        self.balance_amount = total_due + self.customer.due_amount

        self.customer.due_amount = self.balance_amount
        self.customer.save()

        super().save(*args, **kwargs)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Stock, on_delete=models.CASCADE) 
    rim_sold = models.IntegerField(default=0)
    dozen_sold = models.IntegerField(default=0)
    sheet_or_piece_sold = models.IntegerField(default=0)
    per_rim_sell_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_dozen_sell_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    per_sheet_or_piece_sell_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def save(self, *args, **kwargs):
        try:
            stock = Stock.objects.get(product=self.product.product)
        except Stock.DoesNotExist:
            raise ValueError(f"Cannot sell product '{self.product.product_code}' - Not in stock!")

        if self.rim_sold > stock.rim:
            raise ValueError(f"Not enough rims in stock! Available: {stock.rim}, Tried to sell: {self.rim_sold}")

        if self.dozen_sold > stock.dozen:
            raise ValueError(f"Not enough dozens in stock! Available: {stock.dozen}, Tried to sell: {self.dozen_sold}")

        if self.sheet_or_piece_sold > stock.sheet_or_piece:
            raise ValueError(f"Not enough sheets/pieces in stock! Available: {stock.sheet_or_piece}, Tried to sell: {self.sheet_or_piece_sold}")

        if self.pk: 
            old_item = SaleItem.objects.get(pk=self.pk)
            stock.rim += old_item.rim_sold
            stock.dozen += old_item.dozen_sold
            stock.sheet_or_piece += old_item.sheet_or_piece_sold
            stock.save()

        stock.rim -= self.rim_sold
        stock.dozen -= self.dozen_sold
        stock.sheet_or_piece -= self.sheet_or_piece_sold
        stock.save()

 
        if self.per_rim_sell_price and self.per_sheet_or_piece_sell_price:
            self.total_price = (self.rim_sold * self.per_rim_sell_price)+ (self.sheet_or_piece_sold * self.per_sheet_or_piece_sell_price)

        if self.per_dozen_sell_price and self.per_sheet_or_piece_sell_price:
            self.total_price = (self.dozen_sold * self.per_dozen_sell_price)+ (self.sheet_or_piece_sold * self.per_sheet_or_piece_sell_price)
        
        if self.per_rim_sell_price:
            self.per_sheet_or_piece_sell_price=self.per_rim_sell_price/500
            self.total_price = (self.rim_sold * self.per_rim_sell_price)+ (self.sheet_or_piece_sold * self.per_sheet_or_piece_sell_price)
        
        if self.per_dozen_sell_price:
            self.per_sheet_or_piece_sell_price=self.per_rim_sell_price/12
            self.total_price = (self.dozen_sold * self.per_dozen_sell_price)+ (self.sheet_or_piece_sold * self.per_sheet_or_piece_sell_price)
        

        if self.per_sheet_or_piece_sell_price:
            self.per_rim_sell_price=self.per_sheet_or_piece_sell_price*500
            self.per_dozen_sell_price=self.per_sheet_or_piece_sell_price*12
            self.total_price = (self.rim_sold * self.per_rim_sell_price)+(self.dozen_sold * self.per_dozen_sell_price)+ (self.sheet_or_piece_sold * self.per_sheet_or_piece_sell_price)

        super().save(*args, **kwargs)

        self.sale.invoice_total_amount = self.sale.items.aggregate(
            total=models.Sum('total_price')
        )['total'] or 0 

        self.sale.balance_amount = self.sale.invoice_total_amount - self.sale.today_paid_amount
        self.sale.customer.due_amount = self.sale.balance_amount 
        self.sale.customer.save()
        self.sale.save()

    def delete(self, *args, **kwargs):
        stock, created = Stock.objects.get_or_create(product=self.product)

        stock.rim += self.rim_sold
        stock.dozen += self.dozen_sold
        stock.sheet_or_piece += self.sheet_or_piece_sold
        stock.save()

        super().delete(*args, **kwargs)

        self.sale.invoice_total_amount = self.sale.items.aggregate(
            total=models.Sum('total_price')
        )['total'] or 0  

        self.sale.balance_amount = self.sale.invoice_total_amount - self.sale.today_paid_amount
        self.sale.customer.due_amount = self.sale.balance_amount
        self.sale.customer.save()
        self.sale.save()

    def __str__(self):
        return f"Sale Item {self.product.product.product_code} - {self.product.product.product_name}"
