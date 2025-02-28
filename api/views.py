from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.throttling import AnonRateThrottle


from api.serializers import UserSerializer, LoginSerializer
from api.utils import get_mutual_funds_data, get_single_fund_details
from api.models import MutualFund, UserFunds
from api.serializers import UserFundsSerializer, PortfolioSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request) -> Response:
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.id, "username": user.username}
        )


class LogoutView(APIView):
    def post(self, request) -> Response:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListMutualFundsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        mutual_fund_data = get_mutual_funds_data()
        if not mutual_fund_data:
            return Response(
                {"error": "Failed to fetch mutual fund data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(mutual_fund_data)


class AddFundsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request) -> Response:
        user = request.user
        serializer = UserFundsSerializer(data=request.data)
        if serializer.is_valid():
            scheme_code = serializer.validated_data["scheme_Code"]
            quantity = serializer.validated_data["quantity"]
            fund = MutualFund.objects.filter(scheme_Code=scheme_code).first()
            if not fund:
                fund_details = get_single_fund_details(scheme_code=scheme_code)
                if not fund_details:
                    return Response(
                        {"error": "Failed to fetch fund details"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                try:
                    scheme_name = fund_details["Scheme_Name"]
                    nav = fund_details["Net_Asset_Value"]
                    fund = MutualFund.objects.create(
                        scheme_Code=scheme_code,
                        name=scheme_name,
                        nav=nav,
                    )
                except KeyError:
                    return Response(
                        {"error": "Invalid fund details"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            user_funds, created = UserFunds.objects.get_or_create(
                user=user, mutual_fund=fund
            )
            user_funds.quantity += quantity
            user_funds.save()
            return Response(
                {"message": "Funds added successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPortfolioView(generics.ListAPIView):

    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserFunds.objects.filter(user=self.request.user).all()
