from datetime import datetime, timedelta

from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from airport.models import CrewPosition, Crew, Airport, Route, AirplaneType, Airplane, Flight, Ticket, Order
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import CrewPositionSerializer, CrewSerializer, AirportSerializer, RouteSerializer, \
    AirplaneTypeSerializer, AirplaneSerializer, FlightSerializer, FlightDetailSerializer, TicketSerializer, \
    OrderSerializer


class CrewPositionViewSet(viewsets.ModelViewSet):
    queryset = CrewPosition.objects.all()
    serializer_class = CrewPositionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()

        position = self.request.query_params.get("position")
        if position:
            queryset = queryset.filter(position__position__icontains=position)

        return queryset


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()

        name = self.request.query_params.get("name")
        code = self.request.query_params.get("code")
        closest_big_city = self.request.query_params.get("closest_big_city")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if code:
            queryset = queryset.filter(code__icontains=code)
        if closest_big_city:
            queryset = queryset.filter(closest_big_city__icontains=closest_big_city)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by airport name (ex. ?name=Boryspil)",
            ),
            OpenApiParameter(
                "code",
                type=OpenApiTypes.STR,
                description=(
                        "Filter by airport code "
                        "(ex. ?code=KBP)"
                ),
            ),
            OpenApiParameter(
                "closest_big_city",
                type=OpenApiTypes.STR,
                description=(
                        "Filter by closest big city"
                        "(ex. ?closest_big_city=Kyiv)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)




class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()

        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        distance = self.request.query_params.get("distance")

        if source:
            queryset = queryset.filter(source__name__icontains=source)
        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)
        if distance:
            try:
                distance = float(distance)
                queryset = queryset.filter(distance__gte=distance)
            except ValueError:
                pass

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filter by source airport(ex. ?source=Boryspil)",
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.STR,
                description=(
                        "Filter by destination airport"
                        "(ex. ?destination=Joahn)"
                ),
            ),
            OpenApiParameter(
                "distance",
                type=OpenApiTypes.INT,
                description=(
                        "Filter by route distance"
                        "(ex. ?distance=100)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)




class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        brand = self.request.query_params.get("brand")

        queryset = self.queryset

        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        return queryset.distinct()


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().select_related("airplane", "route").annotate(
        tickets_available=(
            F("airplane__row") * F("airplane__seats_in_row") - Count("tickets")
        )
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


    def get_serializer_class(self):
        if self.action == "list":
            return FlightSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

    def get_queryset(self):
        queryset = super().get_queryset()

        departure_time = self.request.query_params.get("departure_time")
        arrival_time = self.request.query_params.get("arrival_time")
        available_tickets = self.request.query_params.get("available_tickets")

        if available_tickets:
            queryset = queryset.filter(tickets_available__gte=available_tickets)

        if departure_time:
            start_date = datetime.strptime(departure_time, "%Y-%m-%d").date()
            end_date = start_date + timedelta(days=1)
            queryset = queryset.filter(departure_time__date__gte=start_date, departure_time__date__lt=end_date)

        if arrival_time:
            date = datetime.strptime(arrival_time, "%Y-%m-%d").date()
            queryset = queryset.filter(arrival_time__date__gte=date)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "departure_time",
                type=OpenApiTypes.DATE,
                description="Filter by departure date (ex. ?departure_time=2023-08-01)",
            ),
            OpenApiParameter(
                "arrival_time",
                type=OpenApiTypes.DATE,
                description="Filter by arrival date (ex. ?arrival_time=2023-08-02)",
            ),
            OpenApiParameter(
                "available_tickets",
                type=OpenApiTypes.INT,
                description="Filter by available tickets is greater or equal (ex. ?available_tickets=10)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(order__user=user)

    def perform_create(self, serializer):
        user = self.request.user

        ticket = serializer.save()
        ticket.order.user = user
        ticket.order.save()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
