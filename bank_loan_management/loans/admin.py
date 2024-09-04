from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import User, FundingAccount, LoanAgreement, LoanPayment, LoanApplication

admin.site.register(User)
admin.site.register(FundingAccount)
admin.site.register(LoanAgreement)
admin.site.register(LoanPayment)
admin.site.register(LoanApplication)