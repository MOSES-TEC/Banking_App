from decimal import Decimal
from django.db import models
from userauths.models import User
from account.models import Account
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

TRANSACTION_TYPE = (
    ("transfer", "Transfer"),
    ("recieved", "Received"),
    ("withdrawal", "Withdrawal"),
    ("refund", "Refund"),
    ("request", "Payment Request"),
    ("deposit", "Deposit"),
    ("none", "None"),
)

TRANSACTION_STATUS = (      
    ('completed', 'Completed'),       
    ('failed', 'Failed'),   
    ('pending', 'Pending'),
    ("processing", "Processing"),
    ("request_sent", "Request Sent"),
    ("request_settled", "Request Settled"),
    ("request_processing", "Request Processing"),      
    ('cancelled', 'Cancelled'),   
    ('refunded', 'Refunded'),     
    ('suspended', 'Suspended'),
)


CARD_TYPE = (
    ('visa', 'Visa'),
    ('mastercard', 'MasterCard'),
    ('amex', 'American Express'),
    ('verve', 'verve'),
)

class Transaction(models.Model):
    transaction_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix="TXN")

    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.CharField(max_length=2000, null=True, blank=True)

    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")

    receiver_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="receiver_account")
    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sender_account")

    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=100, default="none")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        try:
            return f"{self.user}"
        except:
            return f"Transaction"



class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_id = ShortUUIDField(unique=True, length=5, max_length=20, prefix="CARD", alphabet="1234567890")
    
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    cvv = models.IntegerField()
    

    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    card_type = models.CharField(choices=CARD_TYPE, max_length=20, default="mastercard")
    card_status = models.BooleanField(default=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"





