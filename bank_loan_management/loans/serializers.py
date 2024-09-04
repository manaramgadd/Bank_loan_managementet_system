from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    DateField,
    FloatField,
    BooleanField,
    CharField,
    RelatedField
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model  # Import the correct user model

from .models import *

# Get the user model
User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        if hasattr(user, 'role'):  # Check if the user model has 'role'
            token['role'] = user.role
        token['is_admin'] = user.is_superuser
        return token

class FundSerializer(ModelSerializer):
    class Meta:
        model = FundingAccount
        fields = '__all__'

class BankUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','role']

class LoanSerializer(ModelSerializer):

    approval_date = DateField(read_only=True)
    repayment_deadline = DateField()
    interest_rate = FloatField()
    fully_paid = BooleanField()
    min_payment = FloatField()
    max_payment = FloatField()

    class Meta:
        model = LoanAgreement
        fields = (
            'agreement_id',  
            'approval_date',
            'repayment_deadline',
            'interest_rate',
            'fully_paid',
            'min_payment',
            'max_payment',
        )

class LoanRequestSerializer(ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = (
            'application_id',
            'borrower',
            'application_date',
            'loan_amount',
            'terms_conditions',
            'approved'
        )

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = '__all__'
