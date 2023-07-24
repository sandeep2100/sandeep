import random
from django.http import JsonResponse
from django.shortcuts import render,redirect
import googlemaps
import math
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import UserSerializer
import requests
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout





def calculate_distance(source, destination):
    # Initialize Google Maps API client
    gmaps = googlemaps.Client(key='AIzaSyAX0OjsvGZFaLvdaYyOvaWvRmSpnEqVNIo')

    # Make API request to calculate distance
    response = gmaps.distance_matrix(source, destination, mode='driving')

    # Extract distance value from response
    distance = response['rows'][0]['elements'][0]['distance']['value']

    # Convert distance from meters to kilometers
    distance_km = distance / 1000

    return distance_km


def INDEX(request):
    obj = clock.objects.all()
    context = {
        'obj': obj,
    }

    return render(request, 'index.html', context)



#def REGISTER(request):

    #if request.method == 'POST':
     #   username = request.POST.get('username')
     #   mobile = request.POST.get('mobile')
     #   email = request.POST.get('email')
     #   password = request.POST.get('password')



      #  if User.objects.filter(mobile=mobile).exists():
       #     messages.error(request, 'mobile is already exists')
       #     return redirect('login')

       # if User.objects.filter(email=email).exists():
      #      messages.error(request, 'email id is already exists')
       #     return redirect('login')

      #  user = User(
      #      mobile=mobile,
      #      email=email,
       #     username=username,
       # )
       # user.set_password(password)
       # user.save()
       # return redirect('login')
    #return render(request, 'register.html')



def LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email or Password are Invalid !')
            return redirect('login')

    return render(request, 'login.html')




def calculate_fare(request):
    places = ['Mumbai, Maharashtra, India',
                   'Silvassa, Dadra and Nagar Haveli and Daman and Diu, India',
                   'Vapi, Gujarat, India', 'Valsad, Gujarat, India',
                   'Navsari, Gujarat, India',
                   'Surat, Gujarat, India',
                   'Bharuch, Gujarat, India',
                   'Ankleshwar, Gujarat, India',
                   'Vadodara, Gujarat, India',
                   'Udaipur, Rajasthan, India']

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        source = request.POST.getlist('source')  # Get the source as a string, not a list
        destination = request.POST.getlist('destination')  # Get the destination as a string, not a list
        date = request.POST.getlist('date')
        time = request.POST.getlist('time')
        re_date = request.POST.getlist('re_date')
        re_time = request.POST.getlist('re_time')


        distance = calculate_distance(source, destination)
        toll_tax = distance



        per_km_price1 = 10

        per_km_price2 = 12

        per_km_price3 = 14

        per_km_price4 = 15

        base_fare1 = distance * per_km_price1 + toll_tax
        base_fare2 = distance * per_km_price2 + toll_tax
        base_fare3 = distance * per_km_price3 + toll_tax
        base_fare4 = distance * per_km_price4 + toll_tax

        if any(place in source for place in places) and any(place in destination for place in places):
            base_fare1 = base_fare1
            base_fare2 = base_fare2
            base_fare3 = base_fare3
            base_fare4 = base_fare4 # Base fare when both source and destination are in the array
        elif any(place in source for place in places) or any(place in destination for place in places):
            base_fare1 += 1500
            base_fare2 += 1500
            base_fare3 += 1500
            base_fare4 += 1500 # Base fare + additional fare when either source or destination is in the array
        else:
            base_fare1 += 3000
            base_fare2 += 3000
            base_fare3 += 3000
            base_fare4 += 3000  # Base fare + additional fare when neither source nor destination is in the array

        gst1 = base_fare1 * 0.05  # Add 5% GST amount
        gst2 = base_fare2 * 0.05
        gst3 = base_fare3 * 0.05
        gst4 = base_fare4 * 0.05

        total_fare1 = base_fare1 + gst1
        total_fare2 = base_fare2 + gst2
        total_fare3 = base_fare3 + gst3
        total_fare4 = base_fare4 + gst4 # Add 5% GST amount

        fare1 = total_fare1 * 0.15
        fare2 = total_fare2 * 0.15
        fare3 = total_fare3 * 0.15
        fare4 = total_fare4 * 0.15

        dis_fare1 = fare1 + total_fare1
        dis_fare2 = fare2 + total_fare2
        dis_fare3 = fare3 + total_fare3
        dis_fare4 = fare4 + total_fare4

        distance = round(distance)

        total_fare1 = math.ceil(total_fare1)
        total_fare2 = math.ceil(total_fare2)
        total_fare3 = math.ceil(total_fare3)
        total_fare4 = math.ceil(total_fare4)

        gst1 = math.ceil(gst1)
        gst2 = math.ceil(gst2)
        gst3 = math.ceil(gst3)
        gst4 = math.ceil(gst4)

        base_fare1 = math.ceil(base_fare1)
        base_fare2 = math.ceil(base_fare2)
        base_fare3 = math.ceil(base_fare3)
        base_fare4 = math.ceil(base_fare4)

        dis_fare1 = math.ceil(dis_fare1)
        dis_fare2 = math.ceil(dis_fare2)
        dis_fare3 = math.ceil(dis_fare3)
        dis_fare4 = math.ceil(dis_fare4)



        context = {
            'form_type': form_type,
            'source': source,
            'destination': destination,
            'distance': distance,
            'total_fare1': total_fare1,
            'total_fare2': total_fare2,
            'total_fare3': total_fare3,
            'total_fare4': total_fare4,
            'date': date,
            'time': time,
            're_date': re_date,
            're_time': re_time,

            'gst1': gst1,
            'gst2': gst2,
            'gst3': gst3,
            'gst4': gst4,
            'base_fare1': base_fare1,
            'base_fare2': base_fare2,
            'base_fare3': base_fare3,
            'base_fare4': base_fare4,
            'dis_fare1': dis_fare1,
            'dis_fare2': dis_fare2,
            'dis_fare3': dis_fare3,
            'dis_fare4': dis_fare4,

        }
        request.session['source'] = source
        request.session['destination'] = destination
        request.session['distance'] = distance
        request.session['total_fare1'] = total_fare1
        request.session['total_fare2'] = total_fare2
        request.session['total_fare3'] = total_fare3
        request.session['total_fare4'] = total_fare4

        request.session['date'] = date
        request.session['time'] = time
        request.session['re_time'] = re_time
        request.session['re_date'] = re_date

        request.session['gst1'] = gst1
        request.session['gst2'] = gst2
        request.session['gst3'] = gst3
        request.session['gst4'] = gst4

        request.session['base_fare1'] = base_fare1
        request.session['base_fare2'] = base_fare2
        request.session['base_fare3'] = base_fare3
        request.session['base_fare4'] = base_fare4

        request.session['dis_fare1'] = dis_fare1
        request.session['dis_fare2'] = dis_fare2
        request.session['dis_fare3'] = dis_fare3
        request.session['dis_fare4'] = dis_fare4



        return redirect('cab_list')

    return redirect('index')


def CAB(request):
    source = request.session.get('source')
    destination = request.session.get('destination')
    distance = request.session.get('distance')
    total_fare1 = request.session.get('total_fare1')
    total_fare2 = request.session.get('total_fare2')
    total_fare3 = request.session.get('total_fare3')
    total_fare4 = request.session.get('total_fare4')
    date = request.session.get('date')
    time = request.session.get('time')
    date_h = request.session.get('date_h')
    time_h = request.session.get('time_h')
    re_time = request.session.get('re_time')
    re_date = request.session.get('re_time')

    localcity = request.session.get('localcity')
    date_l = request.session.get('date_l')
    time_l = request.session.get('time_l')


    gst1 = request.session.get('gst1')
    gst2 = request.session.get('gst2')
    gst3 = request.session.get('gst3')
    gst4 = request.session.get('gst4')

    base_fare1 = request.session.get('base_fare1')
    base_fare2 = request.session.get('base_fare2')
    base_fare3 = request.session.get('base_fare3')
    base_fare4 = request.session.get('base_fare4')

    dis_fare1 = request.session.get('dis_fare1')
    dis_fare2 = request.session.get('dis_fare2')
    dis_fare3 = request.session.get('dis_fare3')
    dis_fare4 = request.session.get('dis_fare4')

    context = {
        'source': source,
        'destination': destination,
        'distance': distance,
        'total_fare1': total_fare1,
        'total_fare2': total_fare2,
        'total_fare3': total_fare3,
        'total_fare4': total_fare4,
        'date': date,
        'time': time,
        're_date': re_date,
        're_time': re_time,

        'localcity': localcity,
        'date_l': date_l,
        'time_l': time_l,

        'gst1': gst1,
        'gst2': gst2,
        'gst3': gst3,
        'gst4': gst4,
        'date_h': date_h,
        'time_h': time_h,
        'base_fare1': base_fare1,
        'base_fare2': base_fare2,
        'base_fare3': base_fare3,
        'base_fare4': base_fare4,

        'dis_fare1': dis_fare1,
        'dis_fare2': dis_fare2,
        'dis_fare3': dis_fare3,
        'dis_fare4': dis_fare4,

    }
    print(localcity)

    return render(request, 'cab-list.html', context)



def CAB_DETAIL(request):
    if request.method == 'POST':

        form_identifier = request.POST.get('form_identifier')

        if form_identifier == 'form1':
            car = request.POST.get('car1')
            car_type = request.POST.get('car_type1')
            seat = request.POST.get('seat1')
            base_fare = request.POST.get('base1')
            gst = request.POST.get('gst1')
            total_fare = request.POST.get('total1')
        elif form_identifier == 'form2':
            car = request.POST.get('car2')
            car_type = request.POST.get('car_type2')
            seat = request.POST.get('seat2')
            base_fare = request.POST.get('base2')
            gst = request.POST.get('gst2')
            total_fare = request.POST.get('total2')
        elif form_identifier == 'form3':
            car = request.POST.get('car3')
            car_type = request.POST.get('car_type3')
            seat = request.POST.get('seat3')
            base_fare = request.POST.get('base3')
            gst = request.POST.get('gst3')
            total_fare = request.POST.get('total3')
        elif form_identifier == 'form4':
            car = request.POST.get('car4')
            car_type = request.POST.get('car_type4')
            seat = request.POST.get('seat4')
            base_fare = request.POST.get('base4')
            gst = request.POST.get('gst4')
            total_fare = request.POST.get('total4')



    source = request.session.get('source')
    destination = request.session.get('destination')
    distance = request.session.get('distance')

    date = request.session.get('date')
    time = request.session.get('time')
    re_date = request.session.get('re_date')
    re_time = request.session.get('re_time')


    #base_fare = request.session.get('base_fare')



    context = {
        'source': source,
        'destination': destination,
        'distance': distance,
        'total_fare': total_fare,
        'date': date,
        'time': time,
        're_date': re_date,
        're_time': re_time,
        'gst': gst,
        'base_fare': base_fare,
        'car': car,
        'car_type': car_type,
        'seat': seat,


    }

    return render(request, 'cab-detail.html', context)





def CAB_BOOKING(request):
    if request.method == "POST":
        pickup_address = request.POST.get('pickup_address')
        drop_address = request.POST.get('drop_address')
        total = request.POST.get('total')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_b = request.POST.get('mobile_b')
        pickup_city = request.POST.get('pickup_city')
        drop_city = request.POST.get('drop_city')
        booking_id = request.POST.get('booking_id')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        time = request.POST.get('time')






        en = booking(

            name=name,
            email=email,
            mobile_b=mobile_b,  # Assuming mobile_number is the field in the User model
            pickup_city=pickup_city,
            drop_city=drop_city,
            pickup_address=pickup_address,
            drop_address=drop_address,
            booking_id=booking_id,
            amount=amount,
            date=date,
            time=time,


        )
        en.save()
        booking_id = en.booking_id

        total_payment = total
        payment_amount = 0


    source = request.session.get('source')
    destination = request.session.get('destination')
    distance = request.session.get('distance')
    #total_fare = request.session.get('total_fare')
    date = request.session.get('date')
    time = request.session.get('time')
    re_date = request.session.get('re_date')
    re_time = request.session.get('re_time')
    oneway_trip = request.session.get('oneway_trip')
    roundway_trip = request.session.get('roundway_trip')


    context = {
        'source': source,
        'destination': destination,
        'distance': distance,
        'total': total,
        'date': date,
        'time': time,
        're_date': re_date,
        're_time': re_time,
        'oneway_trip': oneway_trip,
        'roundway_trip': roundway_trip,
        'name': name,
        'mobile_b': mobile_b,
        'email': email,
        'pickup_address': pickup_address,
        'drop_address': drop_address,
        'payment_amount': payment_amount,
        'booking_id': booking_id,
        'total': float(total),
        'amount': amount,
        'h_date' : date ,
        'h_time' : time ,




    }

    return render(request, 'cab-booking.html', context)





def CONFIRM(request):
   return render(request, 'confirm.html')


def PASSWORD(request):
   return render(request, 'forgot-password.html')


def PROFILE(request):
   return render(request, 'profile.html')


def PRIVACY(request):
   return render(request, 'privacy&policy.html')




def otp(request):
    return render(request, 'otp.html')

def logout_view(request):
    logout(request)
    return render(request, 'index.html')





class OTPView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password') # Specify the desired mobile number here
        otp = random.randint(100000, 999999)  # Generate OTP here or use a library like `pyotp`

        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Mobile number is already exists')
            return redirect('otp')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exists')
            return redirect('otp')




        user, _ = User.objects.get_or_create(mobile=mobile)
        user.otp = otp
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        # Send OTP via 2Factor.in API
        api_key = '2d1d5168-1bb8-11ee-addf-0200cd936042'  # Replace with your 2Factor.in API key
        url = f"https://2factor.in/API/V1/{api_key}/SMS/{mobile}/{otp}/OTP+is+{otp}"
        response = requests.get(url)


        if response.status_code == 200:
            return render(request, 'verify_otp.html', {'mobile': mobile})
        else:
            return render(request, 'register.html', {'error': 'Failed to send OTP'})


class OTPVerificationView(View):
    def post(self, request):
        mobile = request.POST.get('mobile')  # Specify the desired mobile number here
        otp = request.POST.get('otp')


        try:
            user = User.objects.get(mobile=mobile, otp=otp)
            # Perform further authentication or login logic here
            user.is_active = True  # Activate the user account
            user.save()

            user.otp = None
            user.save(update_fields=['is_active', 'otp'])
            return render(request, 'login.html')
        except User.DoesNotExist:
            return render(request, 'index.html', {'mobile': mobile, 'error': 'Invalid OTP'})

    def get(self, request):
        return render(request, 'index.html')







def localcab(request):
    if request.method == 'POST':
        localcity = request.POST.get('local')
        local_date = request.POST.get('local_date')
        local_time = request.POST.get('local_time')
        package = request.POST.get('package')



