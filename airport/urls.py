from rest_framework.routers import DefaultRouter

from airport.views import CrewPositionViewSet, CrewViewSet, AirportViewSet

router = DefaultRouter()
router.register("crew_position", CrewPositionViewSet)
router.register("crew", CrewViewSet)
router.register("", AirportViewSet)



urlpatterns = router.urls


app_name = "airport"