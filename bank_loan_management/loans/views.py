from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.utils.timezone import make_aware,now
from datetime import datetime
from .models import *
from . import serializers

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer

from decimal import Decimal

class Get_and_Post_Funds(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role != 1 :
            return Response({'error': 'You are not authorized to add funds.'}, status=403)

        data = request.data
        try:
            # Convert 'total_funds' to Decimal instead of float
            loan_budget = Decimal(data.get('total_funds', '0'))
            
            if loan_budget <= Decimal('0.0'):
                return Response({'error': 'Fund amount must be positive.'}, status=400)
        except (ValueError, TypeError, Decimal.InvalidOperation):
            return Response({"error": "Invalid budget format"}, status=400)

        fund, created = FundingAccount.objects.get_or_create(lender=user)
        fund.total_funds += loan_budget
        fund.save()
        serializer = serializers.FundSerializer(fund)
        return Response(serializer.data)

    def get(self, request):
        user = request.user

        if  user.role==2:
            return Response({'error': 'You are not authorized to view this information.'}, status=403)
        if user.role == 1:
            loans = LoanAgreement.objects.filter(lender_id=user)
            fund = FundingAccount.objects.get(lender=user)
            fund_serializer = serializers.FundSerializer(fund)
            loan_serializer = serializers.LoanSerializer(loans, many=True)
            return Response({'fund': fund_serializer.data, 'loans': loan_serializer.data}, status=200)
        if user.role ==3:
            loans = LoanAgreement.objects
            fund = FundingAccount.objects.get()
            fund_serializer = serializers.FundSerializer(fund)
            loan_serializer = serializers.LoanSerializer(loans, many=True)
            return Response({'fund': fund_serializer.data, 'loans': loan_serializer.data}, status=200)

class Get_and_Delete_Users(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 3:  # Assuming 3 is the role for Employees
            return Response({'error': 'Only employees can get all users'}, status=403)
        users = User.objects.all()
        serializer = serializers.BankUserSerializer(users, many=True)
        return Response(serializer.data, status=200)

    def delete(self, request):
        if request.user.role != 3:  # Assuming 3 is the role for Employees
            return Response({'error': 'Only employees can delete users'}, status=403)

        user_id = request.data.get('id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            if user.is_superuser:
                return Response({'error': 'Cannot delete admin users'}, status=400)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    

class Request_Loans(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        if request.user.role == 2:  
            loan_requests = LoanApplication.objects.filter(borrower_id=user , approved=False)
            loans = LoanAgreement.objects.filter(agreement_id__borrower_id=user)
        
        loan_requests = LoanApplication.objects
        loans = LoanAgreement.objects
        loan_request_serializer = serializers.LoanRequestSerializer(loan_requests, many=True)
        loan_serializer = serializers.LoanSerializer(loans, many=True)
        return Response({'loanRequests': loan_request_serializer.data, 'loans': loan_serializer.data}, status=200)

    def post(self, request):
        if request.user.role != 2:  
         return Response({'error': 'Only customers can request loans'}, status=403)
        user = request.user
        data = request.data
        try:
            loan_amount = float(data['loan_amount'])
            terms_conditions = data['terms_conditions']
            if loan_amount <= 0:
                return Response({'error': 'Amount must be positive'}, status=400)
        except (KeyError, ValueError):
            return Response({'error': 'Invalid data'}, status=400)

        loan_request = LoanApplication.objects.create(borrower=user, loan_amount=loan_amount, terms_conditions=terms_conditions)
        serializer = serializers.LoanRequestSerializer(loan_request)
        return Response(serializer.data, status=200)

    def delete(self, request):
        loan_request_id = request.data.get('loanRequestId')
        if not loan_request_id:
            return Response({'error': 'Loan request ID is required'}, status=400)

        try:
            loan_request = LoanApplication.objects.get(application_id=loan_request_id)
            if loan_request.approved:
                return Response({'error': 'Request was already approved'}, status=400)
            loan_request.delete()
            return Response({'message': 'Request deleted successfully'}, status=200)
        except LoanApplication.DoesNotExist:
            return Response({'error': 'Loan request not found'}, status=404)

class Get_and_approve_loans(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 3:  # Assuming 3 is the role for Employees
            return Response({'error': 'Only employees can approve loans'}, status=403)
        loan_requests = LoanApplication.objects.filter(approved=False)
        serializer = serializers.LoanRequestSerializer(loan_requests, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        if request.user.role != 3:  # Assuming 3 is the role for Employees
            return Response({'error': 'Only employees can approve loans'}, status=403)

        data = request.data
        try:
            agreement_id = data['agreement_id']
            interest_rate = float(data['interest_rate'])
            if not 0 < interest_rate < 1:
                return Response({'error': 'Interest rate must be between 0 and 1'}, status=400)

            repayment_deadline_str = data['repayment_deadline']
            repayment_deadline = datetime.strptime(repayment_deadline_str, '%Y-%m-%d')
            repayment_deadline = make_aware(repayment_deadline)

            if repayment_deadline < now():
                return Response({'error': 'Deadline cannot be in the past'}, status=400)

            lender_id = data['lender']
            min_payment = float(data['min_payment'])
            max_payment = float(data['max_payment'])

        except (KeyError, ValueError):
            return Response({'error': 'Invalid data format or missing data'}, status=400)

        try:
            loan_request = LoanApplication.objects.get(application_id=agreement_id)
            lender = User.objects.get(id=lender_id, role=1)  # Assuming role 1 is for Lender
            funding_account = FundingAccount.objects.get(lender=lender)

            if min_payment <= 0 or max_payment > loan_request.loan_amount:
                return Response({'error': 'Invalid minimum or maximum payment'}, status=400)
            if max_payment <= min_payment or max_payment > loan_request.loan_amount:
                return Response({'error': 'Invalid maximum payment'}, status=400)
            if funding_account.total_funds < loan_request.loan_amount:
                return Response({'error': 'Insufficient budget'}, status=400)

        except (LoanApplication.DoesNotExist, User.DoesNotExist, FundingAccount.DoesNotExist):
            return Response({'error': 'Data not found'}, status=404)



        # Approve the loan request and update the funding account
        loan_request.approved = True
        loan_request.save()
        funding_account.total_funds -= loan_request.loan_amount
        funding_account.save()

        # Create the Loan Agreement
        loan_agreement = LoanAgreement.objects.create(
            agreement_id=loan_request,
            lender=lender,
            repayment_deadline=repayment_deadline.date(),
            interest_rate=interest_rate,
            min_payment=min_payment,
            max_payment=max_payment
        )

        serializer = serializers.LoanSerializer(loan_agreement)
        return Response(serializer.data, status=201)
class Get_and_Post_Payments(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = request.user
        loans = LoanAgreement.objects.filter(agreement_id__borrower_id=user)
        payments = LoanPayment.objects.filter(loan__in=loans)
        serializer = serializers.PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        user = request.user
        data = request.data
        try:
            payment_amount = Decimal(request.data.get('payment_amount', 0))  # Convert to Decimal

            loan_id = data['loan']
            if payment_amount <= 0:
                return Response({'error': 'Payment amount must be positive'}, status=400)
        except (KeyError, ValueError):
            return Response({'error': 'Invalid data format or missing data'}, status=400)

        try:
            loan = LoanAgreement.objects.get(agreement_id_id=loan_id)
            if loan.agreement_id.borrower != user:
                return Response({'error': 'Unauthorized loan access'}, status=403)
        except LoanAgreement.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=404)

    

        if not (loan.min_payment <= payment_amount <= loan.max_payment):
            return Response({'error': 'Payment must be within the allowed range'}, status=400)

        total_payments = LoanPayment.objects.filter(loan=loan).aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
        total_due = loan.agreement_id.loan_amount * (1 + loan.interest_rate)
        new_total = (total_payments) + (payment_amount)

        if new_total > total_due:
            return Response({'error': 'Payment exceeds the due amount'}, status=400)
        elif new_total == total_due:

            loan.save()

        payment = LoanPayment.objects.create(loan=loan, payment_amount=payment_amount)
        serializer = serializers.PaymentSerializer(payment)
        return Response(serializer.data, status=200)
