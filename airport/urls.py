from rest_framework.routers import DefaultRouter

from airport.views import CrewPositionViewSet, CrewViewSet, AirportViewSet, RouteViewSet, AirplaneViewSet

router = DefaultRouter()
router.register("crew_position", CrewPositionViewSet)
router.register("crew", CrewViewSet)
router.register("", AirportViewSet)
router.register("route", RouteViewSet)
router.register("airplane_type", RouteViewSet)
router.register("airplane", AirplaneViewSet)



urlpatterns = router.urls


app_name = "airport"