from django.urls import path
from api.views import (
    SignupView,
    LoginView,
    LogoutView,
    ListMutualFundsView,
    AddFundsView,
    ListPortfolioView,
)

urlpatterns = [
    path("create_account/", SignupView.as_view(), name="create_account"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("list_mfs/", ListMutualFundsView.as_view(), name="mutual_funds"),
    path("add_fund/", AddFundsView.as_view(), name="add_mf"),
    path("list_portfolio/", ListPortfolioView.as_view(), name="portfolio"),
]
