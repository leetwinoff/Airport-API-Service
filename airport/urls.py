from rest_framework.routers import DefaultRouter

from airport.views import CrewPositionViewSet

router = DefaultRouter()
router.register("crew", CrewPositionViewSet)

urlpatterns = router.urls


app_name = "airport"