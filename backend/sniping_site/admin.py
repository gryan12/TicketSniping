from django.contrib import admin

# Register your models here.

from .models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display= ('email','play_name','lower_date', 'section', 'higher_date', 'max_price','location')

admin.site.register(Customer, CustomerAdmin)

class PlayAdmin(admin.ModelAdmin):
    list_display= ('date_time','theatre_name','name')

admin.site.register(Play, PlayAdmin)

class PriceAdmin(admin.ModelAdmin):
    list_display= ('value','seat_column','seat_row', 
                    'vendor', 'seat_section', 'play_date_time', 
                    'theatre_name', 'scraping_date_time')

admin.site.register(Price, PriceAdmin)

class SeatAdmin(admin.ModelAdmin):
    list_display= ('seat_column','seat_row', 
                    'play_name', 'section', 'play_date_time', 
                    'theatre_name')

admin.site.register(Seat, SeatAdmin)

class TheatreAdmin(admin.ModelAdmin):
    list_display= ('name','location','capacity')

admin.site.register(Theatre, TheatreAdmin)
