from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from api.models import UserFunds


class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "password_confirmation"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate(self, data):
        if User.objects.filter(email=data["email"], username=data["email"]).exists():
            raise serializers.ValidationError(f"User {data['email']} already exists.")
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        validated_data["password"] = make_password(validated_data["password"])
        user = User.objects.create(**validated_data)
        user.username = user.email
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserFundsSerializer(serializers.Serializer):

    scheme_Code = serializers.CharField()
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value


class PortfolioSerializer(serializers.ModelSerializer):

    mf_name = serializers.ReadOnlyField(source="mutual_fund.name")
    nav = serializers.ReadOnlyField(source="mutual_fund.nav")
    current_value = serializers.SerializerMethodField()

    class Meta:
        model = UserFunds
        fields = ["id", "mf_name", "nav", "quantity", "current_value"]

    def get_current_value(self, obj):
        return obj.quantity * obj.mutual_fund.nav
