from email.policy import default

from django.db import models

# Create your models here.
class BillDetails(models.Model):
    bill_no = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    amount_paid = models.IntegerField(null=True, default=0)
    balance_amount = models.IntegerField(null=True)

    def __str__(self):
        return f'Bill {self.bill_no}'