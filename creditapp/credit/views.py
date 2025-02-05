from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import BillDetails
from .serializers import BillSerializer

# Create your views here.
class BillView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        balance = amount
        bill = BillDetails(amount=amount, balance_amount=balance)
        bill.save()
        serializer = BillSerializer(bill)
        return Response(serializer.data, status=status.HTTP_200_OK)



class BillPayment(APIView):

    def get(self, request):
        unpaid_bills = BillDetails.objects.filter(balance_amount__gt=0).order_by('bill_no')
        if unpaid_bills:
            total_balance = sum(bill.balance_amount for bill in unpaid_bills)
            return Response({'message': 'Fetched total balance', 'data': {total_balance}}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No dues', 'data': {}}, status=status.HTTP_200_OK)

    def post(self, request):
        amnt = int(request.data.get('amount_paid'))
        unpaid_bills = BillDetails.objects.filter(balance_amount__gt=0).order_by('bill_no')
        total_balance = sum(bill.balance_amount for bill in unpaid_bills)

        excess_amount = 0
        if amnt > total_balance:
            excess_amount = amnt - total_balance
            amnt = total_balance  # Only distribute the valid amount
        if unpaid_bills:
            for bill in unpaid_bills:
                if amnt <= 0:
                    break

                if amnt == bill.balance_amount:
                    bill.amount_paid = bill.balance_amount
                    bill.balance_amount = 0
                    amnt=0
                elif amnt < bill.balance_amount:
                    bill.amount_paid += amnt
                    bill.balance_amount = bill.amount - bill.amount_paid
                    amnt = 0

                else:
                    bill.amount_paid += bill.balance_amount
                    amnt = amnt - bill.balance_amount
                    bill.balance_amount = bill.amount - bill.amount_paid

                bill.save()
            response_data = {"message": "Payment successful", 'data': {total_balance}}
            if excess_amount > 0:
                response_data["excess_amount"] = excess_amount

            return Response(response_data, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'There are no dues', 'data': {}}, status=status.HTTP_200_OK)
