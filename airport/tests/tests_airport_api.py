from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from airport.models import (
    CrewPosition,
    Crew,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Order,
    Ticket,
)
from airport.serializers import (
    CrewPositionSerializer,
    CrewSerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    FlightSerializer,
)

CREW_POSITION_URL = reverse("airport:crewposition-list")
CREW_URL = reverse("airport:crew-list")
AIRPORT_URL = reverse("airport:airport-list")
ROUTE_URL = reverse("airport:route-list")
FLIGHT_URL = reverse("airport:flight-list")
AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")
AIRPLANE_URL = reverse("airport:airplane-list")
ORDER_URL = reverse("airport:order-list")
TICKETS_URL = reverse("airport:ticket-list")
CREW_POSITION_DETAIL = "airport:crewposition-detail"
AIRPORT_DETAIL = "airport:airport-detail"
ROUTE_DETAIL = "airport:route-detail"
FLIGHT_DETAIL = "airport:flight-detail"
AIRPLANE_TYPE_DETAIL = "airport:airplanetype-detail"
AIRPLANE_DETAIL = "airport:airplane-detail"
ORDER_DETAIL = "airport:order-detail"
TICKETS_DETAIL = "airport:tickets-detail"


def sample_crew_position(**params):
    defaults = {
        "position": "TestPosition",
    }
    defaults.update(params)

    return CrewPosition.objects.create(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "Joe",
        "last_name": "Doe",
        "position": sample_crew_position(),
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_airport(**params):
    defaults = {
        "name": "TestAirportName",
        "code": "AAA",
        "closest_big_city": "TestCityName",
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(**params):
    defaults = {
        "source": sample_airport(name="Airport1", code="BBB", closest_big_city="City1"),
        "destination": sample_airport(
            name="Airport2", code="CCC", closest_big_city="City2"
        ),
        "distance": 100.0,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {
        "brand": "TestBrand",
        "model": "TestModel",
        "default_row": 10,
        "default_seats_in_row": 6,
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    defaults = {
        "name": "TestName",
        "row": 10,
        "seats_in_row": 6,
        "airplane_type": sample_airplane_type(),
    }
    defaults.update(params)
    airplane = Airplane.objects.create(**defaults)

    if "crew" in defaults:
        for crew_instance in defaults["crew"]:
            airplane.crew.add(crew_instance)

    return airplane


def sample_flight(**params):
    defaults = {
        "route": sample_route(),
        "airplane": sample_airplane(),
        "departure_time": datetime.now(),
        "arrival_time": datetime.now() + timedelta(hours=5),
    }
    defaults.update(params)
    return Flight.objects.create(**defaults)


def sample_order(**params):
    user = get_user_model().objects.create_user(
        username="testusername", email="test1@example.com", password="testpass1"
    )
    defaults = {"created_at": datetime.now(), "user": user, "order_number": "ABC12345"}
    defaults.update(params)
    return Order.objects.create(**defaults)


def sample_ticket(**params):
    defaults = {
        "row": 1,
        "seat": 1,
        "flight": sample_flight(),
        "order": sample_order(),
    }
    defaults.update(params)
    return Ticket.objects.create(**defaults)


def airport_create(name, code, closest_big_city):
    return Airport.objects.create(
        name=name, code=code, closest_big_city=closest_big_city
    )


def route_create(source, destination, distance):
    return Route.objects.create(
        source=source, destination=destination, distance=distance
    )


def detail_crew_position_url(crew_position):
    return reverse(CREW_POSITION_DETAIL, args=[crew_position.id])


def detail_airport_url(airport):
    return reverse(AIRPORT_DETAIL, args=[airport.id])


def detail_route_url(route):
    return reverse(ROUTE_DETAIL, args=[route.id])


def detail_flight_url(flight):
    return reverse(FLIGHT_DETAIL, args=[flight.id])


def detail_airplane_type_url(airplane_type):
    return reverse(AIRPLANE_TYPE_DETAIL, args=[airplane_type.id])


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_crew_position_auth_required(self):
        res = self.client.get(CREW_POSITION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_auth_requires(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_auth_requires(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_route_auth_requires(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_type_auth_requires(self):
        res = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_auth_requires(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_auth_requires(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_auth_requires(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tickets_auth_requires(self):
        res = self.client.get(TICKETS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_crew_position_list(self):
        sample_crew_position()

        res = self.client.get(CREW_POSITION_URL)
        crew_positions = CrewPosition.objects.order_by("id")
        serializer = CrewPositionSerializer(crew_positions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_crew_position_create_forbidden(self):
        res = self.client.post(CREW_POSITION_URL, {"position": "TestPosition"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_list(self):
        sample_crew()

        res = self.client.get(CREW_URL)
        crew = Crew.objects.order_by("first_name")
        serializer = CrewSerializer(crew, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_crew_create_forbidden(self):
        playload = {
            "first_name": "Joe",
            "last_name": "Doe",
            "position": sample_crew_position(),
        }
        res = self.client.post(CREW_URL, playload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_airport_list(self):
        sample_airport()

        res = self.client.get(AIRPORT_URL)
        airports = Airport.objects.order_by("name")
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_airport_create_forbidden(self):
        playload = {"name": "Singapore", "code": "AAA", "closest_big_city": "Singapore"}
        res = self.client.post(AIRPORT_URL, playload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_list(self):
        route = sample_route()

        res = self.client.get(ROUTE_URL)
        route = Route.objects.order_by("source")
        serializer = RouteSerializer(route, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_route_create_forbidden(self):
        playload = {
            "source": sample_airport(
                name="Airport1", code="BBB", closest_big_city="City1"
            ),
            "destination": sample_airport(
                name="Airport2", code="CCC", closest_big_city="City2"
            ),
            "distance": 200.0,
        }

        res = self.client.post(ROUTE_URL, playload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_route_by_source(self):
        airport1 = airport_create("TestAirport1", "ZZZ", "City1")
        airport2 = airport_create("TestAirport2", "YYY", "City2")
        airport3 = airport_create("TestAirport3", "XXX", "City3")
        airport4 = airport_create("TestAirport4", "WWW", "City4")

        route1 = route_create(airport1, airport2, 200.0)
        route2 = route_create(airport3, airport4, 200.0)

        res = self.client.get(ROUTE_URL, {"source": "TestAirport"})

        serializer1 = RouteSerializer(route1)
        serializer2 = RouteSerializer(route2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_filter_route_by_destination(self):
        airport1 = airport_create("TestAirport1", "ZZZ", "City1")
        airport2 = airport_create("TestAirport2", "YYY", "City2")
        airport3 = airport_create("TestAirport3", "XXX", "City3")
        airport4 = airport_create("TestAirport4", "WWW", "City4")

        route1 = route_create(airport1, airport2, 200.0)
        route2 = route_create(airport3, airport4, 200.0)

        res = self.client.get(ROUTE_URL, {"destination": "TestAirport"})

        serializer1 = RouteSerializer(route1)
        serializer2 = RouteSerializer(route2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_filter_route_by_distance(self):
        airport1 = airport_create("TestAirport1", "ZZZ", "City1")
        airport2 = airport_create("TestAirport2", "YYY", "City2")
        airport3 = airport_create("TestAirport3", "XXX", "City3")
        airport4 = airport_create("TestAirport4", "WWW", "City4")

        route1 = route_create(airport1, airport2, 200.0)
        route2 = route_create(airport3, airport4, 100.0)

        res = self.client.get(ROUTE_URL, {"distance": 150})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_airplane_type_list(self):
        sample_airplane_type()

        airplane_types = AirplaneType.objects.order_by("brand")
        serializer = AirplaneTypeSerializer(airplane_types, many=True)

        res = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_airplane_type_filter_by_brand(self):
        airplane_type1 = sample_airplane_type()
        airplane_type2 = sample_airplane_type(
            brand="TestBrand2",
            model="TestModel2",
            default_row=10,
            default_seats_in_row=6,
        )

        serializer1 = AirplaneTypeSerializer(airplane_type1)
        serializer2 = AirplaneTypeSerializer(airplane_type2)

        res = self.client.get(AIRPLANE_TYPE_URL, {"brand": "Brand"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_airplane_type_str(self):
        airplane_type1 = sample_airplane_type()
        expected_str = "TestBrand TestModel"

        self.assertEqual(airplane_type1.__str__(), expected_str)

    def test_airplane_type_create_forbidden(self):
        playload = {
            "brand": "TestBrand",
            "model": "TestModel",
            "default_rows": 10,
            "default_seat_in_rows": 6,
        }

        res = self.client.post(AIRPLANE_TYPE_URL, playload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_list(self):
        airplane1 = sample_airplane()
        crew1 = sample_crew()
        airplane1.crew.add(crew1)

        airplanes = Airplane.objects.order_by("name")
        serializer = AirplaneSerializer(airplanes, many=True)

        res = self.client.get(AIRPLANE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_airplane_create_forbidden(self):
        playload = {
            "name": "TestName",
            "row": 6,
            "seats_in_row": 6,
            "airplane_type": sample_airplane_type(),
            "crew": [],
        }
        res = self.client.post(AIRPLANE_URL, playload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_airplane_str(self):
        airplane = sample_airplane()
        expected_str = "TestName"

        self.assertEqual(airplane.__str__(), expected_str)

    def test_airplane_property(self):
        airplane_type = sample_airplane_type()
        airplane = sample_airplane()

        expected_capacity = airplane.row * airplane.seats_in_row

        serializer = AirplaneSerializer(airplane)

        self.assertEqual(serializer.data["capacity"], expected_capacity)

    def test_flight_list(self):
        sample_flight()

        flights = Flight.objects.order_by("id")
        serializer = FlightSerializer(flights, many=True)

        res = self.client.get(FLIGHT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_flight_create_forbidden(self):
        playload = {
            "route": sample_route().id,
            "airplane": sample_airplane().id,
            "departure_time": datetime.now(),
            "arrival_time": datetime.now() + timedelta(hours=5),
        }

        res = self.client.post(FLIGHT_URL, playload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_flight_property_with_empty_airplane(self):
        flight = sample_flight()
        expected_available_tickets = flight.airplane.capacity
        self.assertEqual(flight.available_tickets, expected_available_tickets)

    def test_flight_property_with_booked_tickets(self):
        flight = sample_flight()
        ticket = Ticket.objects.create(
            row=1, seat=1, flight=flight, order=sample_order()
        )

        booked_tickets_count = Ticket.objects.filter(flight=flight).count()
        expected_available_tickets = flight.airplane.capacity - booked_tickets_count
        self.assertEqual(flight.available_tickets, expected_available_tickets)


class AuthenticatedIsAdminAirportTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_crew_position_create(self):
        res = self.client.post(CREW_POSITION_URL, {"position": "TestPosition"})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_crew_position_detail(self):
        crew_position = sample_crew_position()

        url = reverse(CREW_POSITION_DETAIL, args=[crew_position.id])
        res = self.client.get(url)

        serializer = CrewPositionSerializer(crew_position)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_crew_position_update(self):
        crew_position = sample_crew_position()

        url = detail_crew_position_url(crew_position)
        res = self.client.put(url, {"position": "UpdatedTestPosition"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_crew_position_delete(self):
        crew_position = sample_crew_position()

        url = detail_crew_position_url(crew_position)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_airport_create(self):
        airport = {"name": "TestAirport", "code": "AAA", "closest_big_city": "TestCity"}

        res = self.client.post(AIRPORT_URL, airport)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_airport_partial_update(self):
        airport = sample_airport()

        url = detail_airport_url(airport)
        res = self.client.patch(url, {"name": "NewName"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_route_create(self):
        airport1 = airport_create("Airport1", "BBB", "City1")
        airport2 = airport_create("Airport2", "CCC", "City2")

        route = {"source": airport1.id, "destination": airport2.id, "distance": 200.0}

        res = self.client.post(ROUTE_URL, route)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_route_partial_update(self):
        airport1 = airport_create("Airport1", "BBB", "City1")
        airport2 = airport_create("Airport2", "CCC", "City2")
        airport3 = airport_create("Airport3", "DDD", "City3")

        route = route_create(airport1, airport2, 200)

        url = detail_route_url(route)
        res = self.client.patch(url, {"source": airport3.id, "distance": 2000})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_route_delete(self):
        airport1 = airport_create("Airport1", "BBB", "City1")
        airport2 = airport_create("Airport2", "CCC", "City2")

        route = route_create(airport1, airport2, 200)

        url = detail_route_url(route)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_airplane_type_create(self):
        playload = {
            "brand": "TestBrand",
            "model": "TestModel",
            "default_row": 10,
            "default_seats_in_row": 6,
        }

        res = self.client.post(AIRPLANE_TYPE_URL, playload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_airplane_type_update(self):
        airplane_type = sample_airplane_type()
        playload = {
            "brand": "TestBrand",
            "model": "TestModel",
            "default_row": 10,
            "default_seats_in_row": 6,
        }
        url = detail_airplane_type_url(airplane_type)
        res = self.client.put(url, playload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_airplane_create(self):
        airplane_type = sample_airplane_type()

        crew1 = sample_crew(
            first_name="TestName1",
            last_name="TestLastName1",
            position=sample_crew_position(position="NewTestPosition"),
        )

        playload = {
            "name": "TestName",
            "airplane_type": airplane_type.id,
            "crew": [crew1.id],
        }

        serializer = AirplaneSerializer(data=playload)
        self.assertTrue(serializer.is_valid())
        airplane = serializer.save()

        self.assertEqual(airplane.name, playload["name"])
        self.assertEqual(airplane.airplane_type, airplane_type)
        self.assertEqual(airplane.row, airplane_type.default_row)
        self.assertEqual(airplane.seats_in_row, airplane_type.default_seats_in_row)
        self.assertIn(crew1, airplane.crew.all())

    def test_flight_create(self):
        playload = {
            "route": sample_route().id,
            "airplane": sample_airplane().id,
            "departure_time": datetime.now(),
            "arrival_time": datetime.now() + timedelta(hours=5),
        }

        res = self.client.post(FLIGHT_URL, playload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
