from rest_framework import serializers
from backend.models import Trip, Delivery, Account


class TripSerializer(serializers.Serializer):
    starting_address = serializers.CharField(max_length=200)
    arrival_address = serializers.CharField(max_length=200)
    date = serializers.DateTimeField()
    user_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        trip = Trip(**validated_data)
        trip.save()
        return trip

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class DeliverySerializer(serializers.Serializer):
    starting_address = serializers.CharField(max_length=200)
    arrival_address = serializers.CharField(max_length=200)
    user_id = serializers.IntegerField(required=True)
    weight = serializers.DecimalField(max_digits=5, decimal_places=3)
    trip_id = serializers.IntegerField(required=True)
    info = serializers.CharField(max_length=500)

    def create(self, validated_data):
        delivery = Delivery(**validated_data)
        delivery.save()
        return delivery

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account
