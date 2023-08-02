from datetime import timezone

import razorpay
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.response import Response

from CarRental.AWS import S3
from .models import *
from django.contrib.auth import authenticate, login, logout
import uuid
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework import status

from .ser import GpsTracker


def index(request):
    cars = Car.objects.all()
    return render(request, "index.html", {'cars': cars})


def signup_notification():
    print("Welcome To Car Booking System!!You are successfully logged in..")


def order_notification():
    print("You're Vehicle Order is Confirmed")


def customer_signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        city = request.POST['city']

        if password1 != password2:
            return redirect("/customer_signup")

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                        password=password1)
        user.save()
        try:
            location = Location.objects.get(city=city.lower())
        except:
            location = None
        if location is not None:
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        else:
            location = Location(city=city.lower())
            location.save()
            location = Location.objects.get(city=city.lower())
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        customer.save()
        signup_notification()
        alert = True
        return render(request, "customer_signup.html", {'alert': alert})
    return render(request, "customer_signup.html", {"location": Location.city_list()})


def customer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    user1 = Customer.objects.get(user=user)
                    if user1.type == "Customer":
                        login(request, user)
                        return redirect("/customer_homepage")
                    elif user1.type == "Car Dealer":
                        alert = True
                        return render(request, "customer_login.html", {'alert': alert})
                except ObjectDoesNotExist:
                    alert = True
                    return render(request, "customer_login.html", {'alert': alert})

            alert = True
            return render(request, "customer_login.html", {'alert': alert})

    return render(request, "customer_login.html", {"location": Location.city_list()})


def car_dealer_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        city = request.POST['city']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return redirect('/car_dealer_signup')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                        password=password1)
        user.save()
        try:
            location = Location.objects.get(city=city.lower())
        except:
            location = None
        if location is not None:
            car_dealer = CarDealer(car_dealer=user, phone=phone, location=location, type="Car Dealer")
        else:
            location = Location(city=city.lower())
            location.save()
            location = Location.objects.get(city=city.lower())
            car_dealer = CarDealer(car_dealer=user, phone=phone, location=location, type="Car Dealer")
        car_dealer.save()
        signup_notification()
        alert = True

        return render(request, "car_dealer_signup.html", {"alert": alert})
    return render(request, "car_dealer_signup.html", {"location": Location.city_list()})


def car_dealer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    user1 = CarDealer.objects.get(car_dealer=user)
                    if user1.type == "Car Dealer":
                        login(request, user)
                        return redirect("/all_cars")
                    elif user1.type == "Customer":
                        alert = True
                        return render(request, "car_dealer_login.html", {"alert": alert})
                except ObjectDoesNotExist:
                    alert = True
                    return render(request, "car_dealer_login.html", {"alert": alert})

            alert = True
            return render(request, "car_dealer_login.html", {"alert": alert})
        return render(request, "car_dealer_login.html", {"location": Location.city_list()})


def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'logout.html')


def add_car(request):
    if request.method == "POST":
        car_name = request.POST['car_name']
        vehicle_number = request.POST['vehicle_number']
        city = request.POST['city']
        image = request.FILES['image']
        obj = S3()(directory='car', file=image)
        print(obj)
        print(S3().media_storage.url(obj))
        capacity = request.POST['capacity']
        rent = request.POST['rent']
        tracking = request.POST['tracking']
        car_dealer = CarDealer.objects.get(car_dealer=request.user)
        try:
            location = Location.objects.get(city=city)
        except:
            location = None
        if location is not None:
            car = Car(name=car_name, vehicle_number=vehicle_number, car_dealer=car_dealer, location=location,
                      capacity=capacity, image=obj,
                      rent=rent, tracking=tracking)
        else:
            location = Location(city=city)
            car = Car(name=car_name, vehicle_number=vehicle_number, car_dealer=car_dealer, location=location,
                      capacity=capacity, image=obj,
                      rent=rent, tracking=tracking)
        car.save()
        alert = True
        return render(request, "add_car.html", {'alert': alert})
    return render(request, "add_car.html", {"location": Location.city_list()})


def all_cars(request):
    dealer = CarDealer.objects.filter(car_dealer=request.user).first()
    cars = Car.objects.filter(car_dealer=dealer)
    return render(request, "all_cars.html", {'cars': cars})


def edit_car(request, iid):
    car = Car.objects.get(id=iid)
    if request.method == "POST":
        car_name = request.POST['car_name']
        vehicle_number = request.POST['vehicle_number']
        city = request.POST['city']
        capacity = request.POST['capacity']
        rent = request.POST['rent']
        device_id = request.POST['device_id']

        car.name = car_name
        car.vehicle_number = vehicle_number
        car.city = city
        car.capacity = capacity
        car.rent = rent
        car.tracking = device_id
        car.save()

        try:
            image = request.FILES['image']
            obj = S3()(directory='car', file=image)
            car.image = obj
            car.save()
        except:
            pass
        alert = True
        return render(request, "edit_car.html", {'alert': alert})
    return render(request, "edit_car.html", {'car': car})


def delete_car(request, myid):
    if not request.user.is_authenticated:
        return redirect("/car_dealer_login")
    car = Car.objects.filter(id=myid)
    car.delete()
    return redirect("/all_cars")


def customer_homepage(request):
    return render(request, "customer_homepage.html", {"location": Location.city_list()})


def search_results(request):
    city = request.POST['city']
    city = city.lower()
    vehicles_list = []
    location = Location.objects.filter(city=city)
    for a in location:
        cars = Car.objects.filter(location=a)
        for car in cars:
            if car.is_available:
                vehicle_dictionary = {'name': car.name, 'id': car.id, 'image': car.url, 'city': car.location.city,
                                      'capacity': car.capacity}
                vehicles_list.append(vehicle_dictionary)
    request.session['vehicles_list'] = vehicles_list
    return render(request, "search_results.html")


def car_rent(request):
    id = request.POST['id']
    car = Car.objects.get(id=id)
    cost_per_day = int(car.rent)
    return render(request, 'car_rent.html', {'car': car, 'cost_per_day': cost_per_day})


def order_details(request):
    car_id = request.POST['id']
    username = request.user
    user = User.objects.get(username=username)
    days = request.POST['days']
    car = Car.objects.get(id=car_id)
    if car.is_available:
        car_dealer = car.car_dealer
        rent = (int(car.rent)) * (int(days))
        car_dealer.earnings += rent
        car_dealer.save()
        start_time = int(datetime.datetime.now(tz=timezone.utc).timestamp())
        try:
            order = Order(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days, start_time=start_time)
            order.save()
        except:
            order = Order.objects.get(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days,
                                      start_time=start_time)
        car.is_available = False
        car.save()
        order_notification()
        return render(request, "order_details.html", {'order': order})
    return render(request, "order_details.html")


def past_orders(request):
    all_orders = []
    user = User.objects.get(username=request.user)
    try:
        orders = Order.objects.filter(user=user)
    except:
        orders = None
    if orders is not None:
        for order in orders:
            if not order.is_complete:
                order_dictionary = {'id': order.id, 'rent': order.rent, 'car': order.car, 'days': order.days,
                                    'car_dealer': order.car_dealer}
                all_orders.append(order_dictionary)
    return render(request, "past_orders.html", {'all_orders': all_orders})


def delete_order(request, myid):
    order = Order.objects.filter(id=myid)
    order.delete()
    return redirect("/past_orders")


def all_orders(request):
    all_orders = Order.all_orders(request.user.id)
    print(request.user.id)
    return render(request, "all_orders.html", {'all_orders': all_orders})


def complete_order(request):
    order_id = request.POST['id']
    order = Order.objects.get(id=order_id)
    car = order.car
    order.end_time = int(datetime.datetime.now(tz=timezone.utc).timestamp())
    order.is_complete = True
    order.save()
    car.is_available = True
    car.save()
    return HttpResponseRedirect('/all_orders/')


def earnings(request):
    username = request.user
    user = User.objects.get(username=username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    all_orders = []
    for order in orders:
        all_orders.append(order)
    return render(request, "earnings.html", {'amount': car_dealer.earnings, 'all_orders': all_orders})


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


def terms_and_privacy(request):
    return render(request, 'terms_and_privacy.html')


def about_us(request):
    return render(request, "About_Us.html")


class GpsView(APIView):
    def post(self, request):
        gps_data = request.query_params.dict()
        gps_data.update({"device_id": gps_data['id']})
        gps_data.pop('id', None)
        gps_ser = GpsTracker(data=gps_data)
        gps_ser.is_valid(raise_exception=True)
        gps_ser.save()
        return Response({"status": "OK"}, status=status.HTTP_200_OK)


class CurrentLocationView(APIView):
    def get(self, request, device_id):
        # vehicle = Car.objects.get(vehicle_number='KA34BN7755')
        return render(request=request, template_name='live_location.html',
                      context={"data": Tracking.last_location(device_id=device_id)})


class RoutPathView(APIView):
    def get(self, request, order_id):
        return render(request=request, template_name='root_path.html',
                      context={"data": Order.objects.get(id=order_id).rout_path})


def create_link(order_id):
    return Response(context={"data": Order.objects.get(id=order_id).make_payment})
