import datetime
import uuid

import razorpay
from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User

from CarRental.AWS import S3


class Location(models.Model):
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.city

    @classmethod
    def city_list(cls):
        return cls.objects.all().order_by('city').values_list("city", flat=True)


class CarDealer(models.Model):
    car_dealer = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(10)], max_length=10)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    earnings = models.IntegerField(default=0)
    type = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.car_dealer)


class Car(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=200, null=True, blank=True)
    vehicle_number = models.CharField(max_length=15, blank=False, default=True)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    capacity = models.CharField(max_length=2)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    rent = models.CharField(max_length=10, blank=True)
    tracking = models.CharField(max_length=10, null=True)

    # @classmethod
    # def last_location(cls, tracking_id):
    #     return cls.objects.filter(tracking_id=tracking_id).only('vehicle_number', 'name', 'tracking'). \
    #         values('vehicle_number', 'name', 'tracking').last()

    def __str__(self):
        return self.name

    @property
    def url(self):
        if self.image:
            return S3().media_storage.url(self.image)
        return None


class Tracking(models.Model):
    device_id = models.IntegerField(default=0)
    timestamp = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    bearing = models.FloatField(default=0.0)
    altitude = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    batt = models.FloatField(default=0.0)
    charge = models.FloatField(default=True)

    @classmethod
    def last_location(cls, device_id):
        return cls.objects.filter(device_id=device_id).only('lat', 'lon', 'timestamp', 'accuracy', 'device_id'). \
            values('lat', 'lon', 'timestamp', 'accuracy', 'device_id').last()

    @classmethod
    def root_path(cls, device_id):
        return list(cls.objects.filter(device_id=device_id).only('lat', 'lon', 'timestamp', 'accuracy'). \
                    values('lat', 'lon', 'timestamp', 'accuracy'))


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(10)], max_length=10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rent = models.CharField(max_length=10)
    days = models.CharField(max_length=3)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=30, default='Pending')

    @property
    def rout_path(self):
        if not self.is_complete:
            return list(
                Tracking.objects.filter(device_id=self.car.tracking, timestamp__gte=self.start_time).order_by(
                    'id').only('lat', 'lon',
                               'timestamp',
                               'accuracy', ).values('lat', 'lon', 'timestamp', 'accuracy'))

        return list(Tracking.objects.filter(device_id=self.car.tracking,
                                            timestamp__range=[self.start_time, self.end_time]).order_by('id').only(
            'lat', 'lon',
            'timestamp',
            'accuracy'). \
                    values('lat', 'lon', 'timestamp', 'accuracy'))

    @classmethod
    def all_orders(cls, user):
        return cls.objects.filter(car_dealer__car_dealer=user).order_by('is_complete', '-id').select_related(
            'car_dealer', 'user', 'car')

    # @classmethod
    # def past_orders(cls, user):
    #     return cls.objects.filter(car_dealer__user=user).order_by('is_complete', '-id').select_related(
    #         'car_dealer', 'user', 'car')

    @classmethod
    def make_payment(cls, order_id):
        client = razorpay.Client(auth=("rzp_test_pcJUI2h54atKS2", "zcn5CaE2muoStTh5Q6QBmqM0"))
        order = cls.objects.get(id=order_id)
        customer = Customer.objects.get(user=order.user)
        ref_id = uuid.uuid4().__str__()
        payment = client.payment_link.create(
            {'amount': int(order.rent) * 100, 'currency': 'INR', "accept_partial": "true",
             "first_min_partial_amount": 0, "description": "For Testing",
             "customer": {"name": customer.user.first_name,
                          "email": customer.user.email,
                          "contact": customer.phone
                          },
             "notify":
                 {
                     "sms": True,
                     "email": True
                 },
             "reminder_enable": True,
             "notes": {
                 "policy_name": "HireCar"
             },

             "reference_id": ref_id,
             "callback_url": "http://127.0.0.1:8000/Payment_Success/",
             "callback_method": "get"
             },
        )

        order.payment_id = ref_id
        order.status = payment['status']
        order.save()
        print(payment)
        return payment['short_url']


class Tracking(models.Model):
    device_id = models.IntegerField(default=0)
    timestamp = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    bearing = models.FloatField(default=0.0)
    altitude = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    batt = models.FloatField(default=0.0)
    charge = models.FloatField(default=True)

    @classmethod
    def last_location(cls, device_id):
        return cls.objects.filter(device_id=device_id).only('lat', 'lon', 'timestamp', 'accuracy'). \
            values('lat', 'lon', 'timestamp', 'accuracy').last()
