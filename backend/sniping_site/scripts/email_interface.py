import requests
from ..models import *
def send_alerts():
    
    users = Customer.objects.all()
    print(users)
    for user in users.iterator():
        theatres = []
        playtimes = []

        startDate = datetime.datetime.strptime(getattr(user, "lower_date"), '%Y-%m-%dT%H:%M:%S.%fZ')
        endDate = datetime.datetime.strptime(getattr(user, "higher_date"), '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=11, minutes=59)


        for each in list(Theatre.objects.filter(location=getattr(user, "location")).values('name')):
            theatres.append(each["name"])
        
        for each in list(Play.objects.filter(theatre_name__in=theatres, name=getattr(user, "play_name"),
                         date_time__range=(startDate, endDate)).values('date_time')):
            playtimes.append(each["date_time"])

        prices = Price.objects.filter(theatre_name__in=theatres, play_date_time__in=playtimes,
                                      value__lte=getattr(user, max_price).order_by('-value'))[:10]
        
        print(prices.count() + " prices found for user with email : " + getattr(user, "email"))

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

    return

                                                                        


        

