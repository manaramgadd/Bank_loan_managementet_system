from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone

class User(AbstractUser, PermissionsMixin):
    class UserRole(models.IntegerChoices):
        LENDER = 1, 'Provider'
        BORROWER = 2, 'Customer'
        STAFF = 3, 'Employee'

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.IntegerField(choices=UserRole.choices, default=UserRole.LENDER)
    username = models.CharField(max_length=50, unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Changed related_name to avoid conflict
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='custom_user'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Changed related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.username

class LoanApplication(models.Model):
    application_id = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(User,  on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    terms_conditions = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"LoanApplication {self.application_id} by {self.borrower}"

class LoanAgreement(models.Model):
    agreement_id = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, primary_key=True)
    lender = models.ForeignKey(User, on_delete=models.CASCADE)
    approval_date = models.DateField(auto_now_add=True)
    repayment_deadline = models.DateField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    payment_due_date = models.DateField(null=True)
    fully_paid = models.BooleanField(default=False)
    min_payment = models.DecimalField(max_digits=12, decimal_places=2)
    max_payment = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"LoanAgreement {self.agreement_id}"

class LoanPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(LoanAgreement, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} for Loan {self.loan.agreement_id}"

class FundingAccount(models.Model):
    lender = models.OneToOneField(User, related_name='funding_account', on_delete=models.CASCADE, primary_key=True)
    total_funds = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"FundingAccount for {self.lender.username}"
