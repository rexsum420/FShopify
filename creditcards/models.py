from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CreditCardQuerySet(models.QuerySet):
    def annotate_expiration_month_year(self):
        return self.annotate(
            expiration_month_year=models.functions.Concat(
                models.functions.ExtractMonth('expiration_date'),
                models.Value('/'),
                models.functions.ExtractYear('expiration_date'),
                output_field=models.CharField()
            )
        )

    def with_expiration_month_year(self):
        return self.annotate(
            expiration_month_year=models.functions.Cast(
                models.functions.Concat(
                    models.functions.ExtractMonth('expiration_date'),
                    models.Value('/'),
                    models.functions.ExtractYear('expiration_date')
                ),
                models.CharField()
            )
        )

class CreditCardManager(models.Manager):
    def get_queryset(self):
        return CreditCardQuerySet(self.model, using=self._db).with_expiration_month_year()

class CreditCard(models.Model):
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)
    card_holder = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = CreditCardManager()

    def __str__(self):
        return f"{self.card_holder} - {self.masked_card_number}"

    @property
    def masked_card_number(self):
        # Mask the card number except for the last 4 digits
        return f"**** **** **** {self.card_number[-4:]}" if self.card_number else "No Card Number"

class BillingAddress(models.Model):
    credit_card = models.OneToOneField(CreditCard, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state}, {self.postal_code}, {self.country}"
