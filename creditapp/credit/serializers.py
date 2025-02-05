from rest_framework import serializers
from .models import BillDetails

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetails
        fields = ['bill_no', 'amount', 'created_at', 'amount_paid', 'balance_amount']

        read_only_fields = ['bill_no', 'created_at']