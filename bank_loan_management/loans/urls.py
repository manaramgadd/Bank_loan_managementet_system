from django.urls import path
from . import views
from .views import MyTokenObtainPairView



urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('funds/',views.Get_and_Post_Funds.as_view(),name='funds'),
    path('users/', views.Get_and_Delete_Users.as_view()),
    path('loan-requests/', views.Request_Loans.as_view(),name='loan-requests'),
    path('loan-approves/', views.Get_and_approve_loans.as_view(),name='loan-approves'),
    path('loan-payments/', views.Get_and_Post_Payments.as_view(),name='loan-payments')
]

