from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from api.models import MutualFund, UserFunds


class SignupViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("create_account")
        self.valid_payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirmation": "testpass123",
        }

    def test_create_valid_user(self):
        response = self.client.post(self.signup_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            get_user_model().objects.filter(username="test@example.com").exists()
        )

    def test_create_invalid_user_no_username(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload.pop("email")
        response = self.client.post(self.signup_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_user(self):
        self.client.post(self.signup_url, self.valid_payload, format="json")
        response = self.client.post(self.signup_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.user = get_user_model().objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        self.valid_payload = {"username": "test@example.com", "password": "testpass123"}

    def test_successful_login(self):
        response = self.client.post(self.login_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], self.user.username)

    def test_login_invalid_credentials(self):
        invalid_payload = {"username": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid credentials")

    def test_login_missing_username(self):
        invalid_payload = {"password": "testpass123"}
        response = self.client.post(self.login_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_password(self):
        invalid_payload = {"username": "test@example.com"}
        response = self.client.post(self.login_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_empty_credentials(self):
        invalid_payload = {"username": "", "password": ""}
        response = self.client.post(self.login_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexist_user(self):
        invalid_payload = {
            "username": "nonexistent@example.com",
            "password": "testpass123",
        }
        response = self.client.post(self.login_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse("logout")
        self.user = get_user_model().objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        Token.objects.create(user=self.user)
        self.headers = {"Authorization": f"Token {self.user.auth_token}"}

    def test_successful_logout(self):
        response = self.client.post(self.logout_url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_with_get_method(self):
        response = self.client.get(self.logout_url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ListMutualFundsViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.list_funds_url = reverse("list_mutual_funds")
        self.user = get_user_model().objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        Token.objects.create(user=self.user)
        self.headers = {"Authorization": f"Token {self.user.auth_token}"}
        self.test_data = [
            {
                "Scheme_Code": 120437,
                "ISIN_Div_Payout_ISIN_Growth": "-",
                "ISIN_Div_Reinvestment": "INF846K01CU0",
                "Scheme_Name": "Axis Banking & PSU Debt Fund - Direct Plan - Daily IDCW",
                "Net_Asset_Value": 1038.5219,
                "Date": "28-Feb-2025",
                "Scheme_Type": "Open Ended Schemes",
                "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
                "Mutual_Fund_Family": "Axis Mutual Fund",
            },
            {
                "Scheme_Code": 120438,
                "ISIN_Div_Payout_ISIN_Growth": "INF846K01CR6",
                "ISIN_Div_Reinvestment": "-",
                "Scheme_Name": "Axis Banking & PSU Debt Fund - Direct Plan - Growth Option",
                "Net_Asset_Value": 2624.3258,
                "Date": "28-Feb-2025",
                "Scheme_Type": "Open Ended Schemes",
                "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
                "Mutual_Fund_Family": "Axis Mutual Fund",
            },
        ]

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_funds_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_http_method(self):
        response = self.client.post(self.list_funds_url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_successful_mutual_funds_fetch(self):
        with patch("api.views.get_mutual_funds_data") as mock_get_data:
            mock_get_data.return_value = self.test_data
            response = self.client.get(self.list_funds_url, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)
            self.assertEqual(response.data[0]["Scheme_Code"], 120437)

    def test_failed_mutual_funds_fetch(self):
        with patch("api.views.get_mutual_funds_data") as mock_get_data:
            mock_get_data.return_value = None
            response = self.client.get(self.list_funds_url, headers=self.headers)
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(response.data["error"], "Failed to fetch mutual fund data")


class ListPortFolioViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.list_portfolio_url = reverse("portfolio")
        self.user = get_user_model().objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )
        Token.objects.create(user=self.user)
        mf = MutualFund.objects.create(name="Test Fund 1", scheme_Code=123456, nav=10)
        uf = UserFunds.objects.create(user=self.user, mutual_fund=mf, quantity=100)
        self.headers = {"Authorization": f"Token {self.user.auth_token}"}

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_portfolio_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_http_method(self):
        response = self.client.post(self.list_portfolio_url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_successful_portfolio_fetch(self):
        response = self.client.get(self.list_portfolio_url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["mf_name"], "Test Fund 1")
        self.assertEqual(response.data[0]["current_value"], 1000.0)
"Test Fund 1"
