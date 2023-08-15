from rest_framework.routers import DefaultRouter

from airport.views import (
    CrewPositionViewSet,
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    AirplaneViewSet,
    FlightViewSet,
    AirplaneTypeViewSet,
    TicketViewSet,
    OrderViewSet,
)

router = DefaultRouter()
router.register("crew_position", CrewPositionViewSet)
router.register("crew", CrewViewSet)
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)
router.register("airplane_type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("flight", FlightViewSet)
router.register("tickets", TicketViewSet)
router.register("order", OrderViewSet)


urlpatterns = router.urls


app_name = "airport"
