from rest_framework.routers import DefaultRouter

from airport.views import CrewPositionViewSet, CrewViewSet

router = DefaultRouter()
router.register("crew_position", CrewPositionViewSet)
router.register("crew", CrewViewSet)



urlpatterns = router.urls


app_name = "airport"