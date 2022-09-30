import pytest
from datetime import datetime

from airline.models import FareClass, ComfortsPrice, Airplane, Airport, Flight, Booking, Ticket, Discount
from account.models import StaffProfile


@pytest.fixture
def testpassenger(db, django_user_model):
    email = 'test_passenger@test.com'
    password = 'strong-test-pass1!'
    first_name = 'test_first_name'
    last_name = 'test_last_name'
    passenger = django_user_model.objects.create_user(email=email, password=password, first_name=first_name,
                                                      last_name=last_name, is_airline_staff=False)
    passenger.is_active = True
    return passenger


@pytest.fixture
def teststaffuser(db, django_user_model):
    email = 'test_staff_member@test.com'
    password = 'strong-test-pass1!'
    first_name = 'staff_first_name'
    last_name = 'staff_last_name'
    staffuser = django_user_model.objects.create_user(email=email, password=password, first_name=first_name,
                                                      last_name=last_name, is_airline_staff=True)
    return staffuser


@pytest.fixture
def testsupervisorprofile(db, django_user_model, teststaffuser, airport):
    supervisor = StaffProfile.objects.create_user(user=teststaffuser, airport=airport, role='supervisor')
    return supervisor


@pytest.fixture
def airplane(db):
    airplane = Airplane.objects.create(name="Airbus A340-600", first_class_seats=8, business_class_seats=44,
                                       economy_class_seats=245)
    return airplane


@pytest.fixture
def airport_LGA(db):
    airport = Airport.objects.create(iata="LGA", name="LaGuardia", city="New York", country_code='US')
    return airport


@pytest.fixture
def airport_ORY(db):
    airport = Airport.objects.create(iata="ORY", name="Orly", city="Paris", country_code='FR')
    return airport


@pytest.fixture
def flight(db, airport_LGA, airport_ORY, airplane, testsupervisorprofile):
    flight = Flight.objects.create(departure_time=datetime.strptime("2022-10-04 14:00:00+03", '%Y-%m-%d %H:%M:%S+%z'),
                                   duration="10:35:00", origin=airport_LGA, destination=airport_ORY,
                                   airplane=airplane, first_class_seats_occupied=0, business_class_seats_occupied=0,
                                   economy_class_seats_occupied=0, first_class_price=1000.00,
                                   economy_class_price=500.00,
                                   business_class_price=700.00, supervisor=testsupervisorprofile, is_cancelled=False)
    return flight


@pytest.fixture
def booking(db, testpassenger, flight):
    booking = Booking.objects.create(flight=flight, purchaser=testpassenger)
    return booking


@pytest.fixture
def discount(db, flight):
    discount = Discount.objects.create(flight=flight, first_class_discount=3.00, business_class_discount=5.00,
                                       economy_class_discount=10.00)
    return discount


@pytest.fixture
def economy_class(db, flight):
    economy_class = FareClass.objects.create(name='Economy')
    return economy_class


@pytest.fixture
def business_class(db, flight):
    business_class = FareClass.objects.create(name='Business')
    return business_class


@pytest.fixture
def first_class(db, flight):
    first_class = FareClass.objects.create(name='First')
    return first_class


@pytest.fixture
def economy_class_ticket(db, booking, flight, testpassenger, economy_class):
    ticket = Ticket.objects.create(booking=booking, passenger_first_name=testpassenger.first_name,
                                   passenger_last_name=testpassenger.last_name, fare_class=economy_class,
                                   n_bags=2, baggage_price=70.00, lunch=True, total_price=530.00,
                                   boarding_registered=False, checked_in=False)
    return ticket


@pytest.fixture
def business_class_ticket(db, booking, flight, testpassenger, business_class):
    ticket = Ticket.objects.create(booking=booking, passenger_first_name=testpassenger.first_name,
                                   passenger_last_name=testpassenger.last_name, fare_class=business_class,
                                   n_bags=2, baggage_price=0.00, lunch=True, total_price=695.00,
                                   boarding_registered=False, checked_in=False)
    return ticket


@pytest.fixture
def first_class_ticket(db, booking, flight, testpassenger, first_class):
    ticket = Ticket.objects.create(booking=booking, passenger_first_name=testpassenger.first_name,
                                   passenger_last_name=testpassenger.last_name, fare_class=first_class,
                                   n_bags=2, baggage_price=0.00, lunch=True, total_price=1020.00,
                                   boarding_registered=False, checked_in=False)
    return ticket
