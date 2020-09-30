from django.shortcuts import render
import datetime
import json


# Create your views here.

from rest_framework import viewsets
from rest_framework.decorators import api_view

from .serializers import theatreSerializer
from .serializers import playSerializer
from .serializers import sectionSerializer
from .models import *
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .scripts.email_interface import *


class theatreView(viewsets.ViewSet):
    queryset = Theatre.objects.distinct('location')
    serializer = theatreSerializer
    def list(self, request, *args, **kwargs):
        json_dict=[]
        listset = list(Theatre.objects.distinct('location').values('location'))
        for each in listset:
            theatres_at_location = list(Theatre.objects.filter(location=each["location"]).distinct('name').values_list('name'))
            count = 0
            for theatre in theatres_at_location:
                plays = list(Play.objects.filter(theatre_name=theatre))
                count+=len(plays)

            if count:
                json_dict.append(each["location"])
        return Response(json_dict)

class playView(viewsets.ViewSet):
    queryset = Play.objects.distinct('name')
    serializer = playSerializer


    def list(self, request, *args, **kwargs):
        json_dict=[]
        locations = list(Theatre.objects.distinct('location').values('location'))

        play_location_dict={}
        play_list = []
        for each in list(Play.objects.distinct('name').values('name')):
            play_list.append(each['name'])
        play_location_dict['All'] = play_list

        for location in locations:
            place= location['location']
            temp_list=[]
            play_list=[]


            theatreList = list(Theatre.objects.filter(location=place).values('name'))
            for theatre in theatreList:
                theatre = theatre['name']
                temp_list+=list(Play.objects.filter(theatre_name=theatre).distinct('name').values('name'))

            if len(temp_list)>0:
                for each in temp_list:
                    play_list.append(each["name"])

                play_location_dict[place] = play_list
            else:
                play_location_dict[place]=[]

        json_dict.append(play_location_dict)

        return Response(json_dict)

class sectionView(viewsets.ViewSet):
    queryset = Theatre.objects.distinct('location')
    serializer = sectionSerializer
    def list(self, request, *args, **kwargs):
        json_dict=[]
        locations = list(Theatre.objects.distinct('location').values('location'))

        play_location_section_dict={}
        play_list = []
        for each in list(Play.objects.distinct('name').values('name')):
            play_list.append(each['name'])

        for location in locations:
            place= location['location']
            play_dict={}
            temp_play_list=[]
            play_list=[]


            theatreList = list(Theatre.objects.filter(location=place).values('name'))
            for theatre in theatreList:
                theatre = theatre['name']
                temp_play_list+=list(Play.objects.filter(theatre_name=theatre).distinct('name').values_list('name','sections'))

            if len(temp_play_list)>0:
                play_section_dict={}
                for play in temp_play_list:
                    if play[1]!= None:
                        section_list=play[1].split(',')
                    else:
                        section_list=['Stalls']
                    play_section_dict[play[0]]=list(dict.fromkeys(section_list))
                play_location_section_dict[place]=play_section_dict

                            



            else:
                play_location_section_dict[place]={}

        json_dict.append(play_location_section_dict)
        return Response(json_dict)


@csrf_exempt
@api_view(['POST'])
def formSearch(request):
    def prices_to_json(prices):
        prices_json=[]
        for price in prices.iterator():
            price_play_date_time = getattr(price, 'play_date_time')
            price_theatre_name = getattr(price, 'theatre_name')
            price_seat_row  = getattr(price, 'seat_row')
            price_seat_col  = getattr(price, 'seat_column')
            price_seat_section  = getattr(price, 'seat_section')
            play_url = getattr(Play.objects.get(name = loaded_data["play"], date_time=price_play_date_time, 
                               theatre_name=price_theatre_name),'url')

            price_history = Price.objects.filter(play_date_time=price_play_date_time,
                                                 theatre_name=price_theatre_name,
                                                 seat_row=price_seat_row,
                                                 seat_column=price_seat_col,
                                                 seat_section=price_seat_section)
            raw_history=[(getattr(oldprice, 'scraping_date_time'), getattr(oldprice, 'value')) 
                      for oldprice in price_history.iterator() ]
            new_raw_history=sorted(raw_history, key=lambda x:(x[0]), reverse=True)
            history = [x[1] for x in new_raw_history]
            print(history)


            price_json = {
                    'price': getattr(price, 'value'),
                    'play_name': loaded_data["play"],
                    'play_date_time': price_play_date_time,
                    'theatre_name': price_theatre_name,
                    'seat_row': price_seat_row,
                    'seat_col': price_seat_col,
                    'section': price_seat_section,
                    'vendor': getattr(price, 'vendor'),
                    'url':play_url,
                    'history':history
                    }
            prices_json.append(price_json)
        return prices_json
        
    def get_play_times(play, start, end, search=False):
        playtimes = []
        extra_days=1
        now = datetime.datetime.now().replace(hour=11, minute=59)
        print(now)
        if (search):
            while (extra_days < 365 and len(playtimes)<11):
                extra_days+=1
                newStart = startDate - datetime.timedelta(days=extra_days)
                if (newStart < now):
                    newStart = now
                newEnd= endDate + datetime.timedelta(days=extra_days)
                plays = list(Play.objects.filter(theatre_name__in=theatres, name=play,
                        date_time__range=(newStart, newEnd)).values('date_time'))
                if (len(plays)>0):
                    for each in plays:
                        playtimes.append(each["date_time"])
                
                

        else:
            for each in list(Play.objects.filter(theatre_name__in=theatres, name=play,
                                                 date_time__range=(start, end)).values('date_time')):
                playtimes.append(each["date_time"])
        return playtimes

            

    loaded_data = request.data

    print(request.data)
    theatres = []
    
    startDate = datetime.datetime.strptime(loaded_data["startDate"], '%Y-%m-%dT%H:%M:%S.%fZ')
    endDate = datetime.datetime.strptime(loaded_data["endDate"], '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=23, minutes=59)

    for each in list(Theatre.objects.filter(location=loaded_data["place"]).values('name')):
        theatres.append(each["name"])


    playtimes = get_play_times(loaded_data["play"], startDate, endDate)

    if loaded_data["eveOrMat"]=="Evening":
        new_times=[]
        for playtime in playtimes:
            if playtime.time() > datetime.time(17,00):
                new_times.append(playtime)
        playtimes = new_times      

    
    elif loaded_data["eveOrMat"]=="Matinee":
        new_times=[]
        for playtime in playtimes:
            if playtime.time() < datetime.time(17,00):
                new_times.append(playtime)
        playtimes = new_times      


    prices = Price.objects.filter(theatre_name__in=theatres, play_date_time__in=playtimes,
                                  value__lte=loaded_data["highPrice"], seat_section=loaded_data["section"]).order_by('-scraping_date_time')
    
    plays = list(prices.values_list('theatre_name', 'play_date_time').distinct())
    venue_prices={}
    for play in plays:
        play_prices= list(prices.filter(theatre_name=play[0],play_date_time=play[1]))
        venue_prices[play]=len(play_prices)
        

         

    print(prices.count())
    prices=prices[:25]
        

    res = []

    if (prices.count()>0):
            res+=prices_to_json(prices)
    else:
        res.append(0)
        diff_date_play_times = get_play_times(loaded_data["play"], startDate, endDate, search=True)
        other_prices = {}


        other_prices["diff_date_prices"] = prices_to_json(Price.objects.filter(theatre_name__in=theatres, play_date_time__in=diff_date_play_times,
                                      value__lte=loaded_data["highPrice"], seat_section=loaded_data["section"]).order_by('-value')[:5])
        res.append(other_prices)
        
        
        



    print(res)
    return JsonResponse(res, safe=False)


@csrf_exempt
@api_view(['POST'])
def emailAlert(request):

    print(request)
    #section=request.data["section"],
    alert = Customer(email=request.data["email"], play_name=request.data["play"], max_price=request.data["highPrice"],
                     lower_date=request.data["startDate"],higher_date=request.data["endDate"],
                     location=request.data["place"])

    print(alert)
    alert.save()
    print(alert)
                     

    res = []
    email_json = {
            'success':"email recieved = %s"%(request.data["email"])
            }
    res.append(email_json)
    return JsonResponse(res, safe=False)
     
@csrf_exempt
@api_view(['POST'])
def checkAlerts(request):
    print(request.data)

    users = Customer.objects.all()
    print(users)
    email_count=0

    for user in users.iterator():
        theatres = []
        playtimes = []

        #startDate = datetime.datetime.strptime(getattr(user, "lower_date"), '%Y-%m-%dT%H:%M:%S.%fZ')
        #endDate = datetime.datetime.strptime(getattr(user, "higher_date"), '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=11, minutes=59)
        startDate = getattr(user, "lower_date")
        endDate = getattr(user, "higher_date")



        for each in list(Theatre.objects.filter(location=getattr(user, "location")).values('name')):
            theatres.append(each["name"])
        
        for each in list(Play.objects.filter(theatre_name__in=theatres, name=getattr(user, "play_name"),
                         date_time__range=(startDate, endDate)).values('date_time')):
            playtimes.append(each["date_time"])

        prices = Price.objects.filter(theatre_name__in=theatres, play_date_time__in=playtimes,
                                      value__lte=getattr(user, "max_price")).order_by('-value')[:10]
        
        print(str(prices.count()) + " prices found for user with email : " + getattr(user, "email"))

        if prices.count() > 0:
            if prices.count() == 1:
                body = "We have found you 1 seat: \n"
            else:
                body = "We have found you %d seats: \n"%(prices.count)

            for price in prices.iterator():
                play = Play.objects.get(date_time = getattr(price, "play_date_time"), name = getattr(price, "play_name"), 
                                            theatre_name =getattr(price, "theatre_name"))
                body+="%s - %s - %s - Seat:- %s %s %s Price:- %s Link:- %s \n"%(getattr(user, "play_name"), getattr(price, "theatre_name"),
                                                                                getattr(price, "play_date_time"), getattr(price, "seat_row"),
                                                                                getattr(price, "seat_col"), getattr(price, "seat_row"),
                                                                                getattr(price, "seat_section"), getattr(price, "value"),
                                                                                getattr(play, "url"))
            requests.post(
                "https://api.mailgun.net/v3/mg.tik.ninja/messages",
                auth=("api", "0cf59a904a59ee4841963b7ebae67ea8-ed4dc7c4-2db0460f"),
                data={"from": "Tik.Ninja Seat Alerts <seat-alert-noreply@mg.tik.ninja>",
                    "to": [""%(getattr(user,"email"))],
                    "subject": "We Have Found You A Seat!",
                    "text": body})
            email_count +=1
    res = []
    success_json = {
        'AlertsChecked':"%d emails sent"%(email_count)
    }
    res.append(success_json)
    return JsonResponse(res, safe=False)
    
    
    







