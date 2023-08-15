from django.contrib import admin

from airport.models import (
    CrewPosition,
    Crew,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Ticket,
    Order
)

admin.site.register(CrewPosition)
admin.site.register(Crew)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(Order)
