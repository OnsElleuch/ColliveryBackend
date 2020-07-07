from django.http import JsonResponse, Http404, HttpResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from backend.models import Delivery, Trip
from backend.serializers import DeliverySerializer, TripSerializer, RegistrationSerializer


class DeliveriesView(GenericAPIView):
    def get(self, request, **kwargs):
        deliveries = Delivery.objects.all()
        deliveries_dict = [delivery.to_dict() for delivery in deliveries]
        return JsonResponse(deliveries_dict, safe=False)

    def post(self, request, **kwargs):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.create(serializer.validated_data)
            return JsonResponse(obj.to_dict())
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryView(GenericAPIView):
    def get_object(self, pk):
        try:
            return Delivery.objects.get(pk=pk)
        except Delivery.DoesNotExist:
            raise Http404

    def get(self, request, pk, **kwargs):
        delivery = self.get_object(pk)
        serializer = DeliverySerializer(delivery)
        return JsonResponse(serializer.data)

    def put(self, request, pk, **kwargs):
        delivery = self.get_object(pk)
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.update(delivery, serializer.validated_data)
            return JsonResponse(obj.to_dict())
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, **kwargs):
        delivery = self.get_object(pk=pk)
        delivery.delete()
        return HttpResponse(status=status.HTTP_200_OK)


class TripsView(GenericAPIView):
    def get(self, request, **kwargs):
        trips = Trip.objects.all()
        trips_dict = [trip.to_dict() for trip in trips]
        return JsonResponse(trips_dict, safe=False)

    def post(self, request, **kwargs):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.create(serializer.validated_data)
            return JsonResponse(obj.to_dict())
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripView(GenericAPIView):
    def get_object(self, pk):
        try:
            return Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            raise Http404

    def get(self, request, pk, **kwargs):
        trip = self.get_object(pk)
        serializer = TripSerializer(trip)
        return JsonResponse(serializer.data)

    def put(self, request, pk, **kwargs):
        trip = self.get_object(pk)
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.update(trip, serializer.validated_data)
            return JsonResponse(obj.to_dict())
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, **kwargs):
        trip = self.get_object(pk=pk)
        trip.delete()
        return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
