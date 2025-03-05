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
        if self.pk is None:  # Only update when creating a new invoice
            self.company.previous_due += self.balance_amount
            self.company.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_challan_no} - {self.company.company_name}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    product_code = models.CharField(max_length=100)
    product_description = models.CharField(max_length=255)
    rim = models.IntegerField(default=0)
    dozen=models.IntegerField(default=0)
    sheet_or_piece = models.IntegerField(default=0)
    only_sheet_piece = models.IntegerField(default=0)
    total_sheet_piece = models.IntegerField(default=0)
    rim_or_dozen_per_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sheet_or_piece_per_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    labour_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    road_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_extra_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    total_per_rim_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_per_sheet_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    rim_or_dozen_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sheet_or_piece_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    rim_or_dozen_per_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    rim_or_dozen_per_sell_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sheet_or_piece_per_sell_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product_code} - {self.product_description}"
