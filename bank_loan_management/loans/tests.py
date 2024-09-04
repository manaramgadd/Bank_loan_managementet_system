from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import FundingAccount, LoanApplication, LoanAgreement, LoanPayment
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Sum

User = get_user_model()

class LoanManagementTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a lender user
        self.lender = User.objects.create_user(
            username='lender_user', password='password123', role=1
        )
        
        # Create a borrower user
        self.borrower = User.objects.create_user(
            username='borrower_user', password='password123', role=2
        )
        
        # Create an employee user
        self.employee = User.objects.create_user(
            username='employee_user', password='password123', role=3
        )

        # Set up tokens for the users
        self.lender_token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'lender_user',
            'password': 'password123'
        }).data['access']

        self.borrower_token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'borrower_user',
            'password': 'password123'
        }).data['access']

        self.employee_token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'employee_user',
            'password': 'password123'
        }).data['access']

        # Create a FundingAccount for the lender
        FundingAccount.objects.create(lender=self.lender, total_funds=Decimal('10000.00'))

        # Create a LoanApplication and LoanAgreement
        self.loan_application = LoanApplication.objects.create(
            borrower=self.borrower, loan_amount=5000, terms_conditions='6 months', approved=True
        )
        self.loan_agreement = LoanAgreement.objects.create(
            agreement_id=self.loan_application,
            lender=self.lender,
            repayment_deadline=make_aware(datetime.now() + timedelta(days=180)).date(),
            interest_rate=0.05,
            min_payment=Decimal('100.00'),
            max_payment=Decimal('1000.00')
        )


   
    def test_post_payment_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.post(reverse('loan-payments'), {
            'payment_amount': '500.00',
            'loan': self.loan_agreement.agreement_id_id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['payment_amount']), 500.00)

    def test_post_payment_invalid_amount(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.post(reverse('loan-payments'), {
            'payment_amount': '-100.00',
            'loan': self.loan_agreement.agreement_id_id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Payment amount must be positive')

    def test_post_payment_exceeds_due(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.post(reverse('loan-payments'), {
            'payment_amount': '10000.00',
            'loan': self.loan_agreement.agreement_id_id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       

    def test_post_payment_unauthorized_access(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.lender_token)
        response = self.client.post(reverse('loan-payments'), {
            'payment_amount': '500.00',
            'loan': self.loan_agreement.agreement_id_id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'Unauthorized loan access')

    def test_post_payment_invalid_loan(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.post(reverse('loan-payments'), {
            'payment_amount': '500.00',
            'loan': 99999  # Assuming this loan ID doesn't exist
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Loan not found')
    
    def test_get_payments_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.get(reverse('loan-payments'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_post_funds_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.lender_token)
        response = self.client.post(reverse('funds'), {'total_funds': '1000.00'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_funds_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.post(reverse('funds'), {'total_funds': '1000.00'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_funds_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.lender_token)
        response = self.client.get(reverse('funds'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_funds_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.get(reverse('funds'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_request_loans_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.post(reverse('loan-requests'), {
            'loan_amount': '5000',
            'terms_conditions': '6 months'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['loan_amount']), 5000.00)
    def test_request_loans_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.lender_token)
        response = self.client.post(reverse('loan-requests'), {
            'loan_amount': '5000.00',
            'terms_conditions': '6 months'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_loan_request(self):
        # Create a loan request to delete
        loan_request = LoanApplication.objects.create(
            borrower=self.borrower, loan_amount=5000, terms_conditions='6 months', approved=False
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.borrower_token)
        response = self.client.delete(reverse('loan-requests'), {'loanRequestId': loan_request.application_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Request deleted successfully')


  
