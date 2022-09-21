from django.db import models

from account.models import StaffProfile, PassengerProfile


class FareClass(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} class"


class BaggagePrices(models.Model):
    fare_class = models.ForeignKey(FareClass, on_delete=models.CASCADE, related_name="baggage_prices")
    first_bag_price = models.DecimalField(max_digits=5, decimal_places=2)
    second_bag_price = models.DecimalField(max_digits=5, decimal_places=2)
    three_or_more_bags_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.fare_class} baggage prices"


class Airplane(models.Model):
    name = models.CharField(max_length=150)
    first_class_seats = models.IntegerField()
    business_class_seats = models.IntegerField()
    economy_class_seats = models.IntegerField()

    def __str__(self):
        return self.name


class Airport(models.Model):
    iata = models.CharField(max_length=3)
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}, {self.city}, {self.iata}"


class Flight(models.Model):
    departure_time = models.DateTimeField()
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    first_class_seats_occupied = models.IntegerField()
    business_class_seats_occupied = models.IntegerField()
    economy_class_seats_occupied = models.IntegerField()
    first_class_price = models.DecimalField(max_digits=6, decimal_places=2)
    business_class_price = models.DecimalField(max_digits=6, decimal_places=2)
    economy_class_price = models.DecimalField(max_digits=6, decimal_places=2)
    supervisor = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="flights")

    def __str__(self):
        return f"{self.origin} -> {self.destination}, {self.departure_time}"


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    purchaser = models.ForeignKey(PassengerProfile, on_delete=models.CASCADE, related_name="bookings")
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.flight}, {self.purchaser}, {self.total_price}"


class Ticket(models.Model):
    ticket_code = models.BigAutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="tickets")
    passenger_first_name = models.CharField(max_length=150)
    passenger_last_name = models.CharField(max_length=150)
    fare_class = models.ForeignKey(FareClass, on_delete=models.CASCADE, related_name="tickets")
    baggage_cost = models.DecimalField(max_digits=6, decimal_places=2)
    lunch = models.BooleanField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    boarding_registered = models.BooleanField()
    checked_in = models.BooleanField()

    def __str__(self):
        return f"{self.passenger_first_name} {self.passenger_last_name}"


class Discount(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="discounts")
    first_class_discount = models.DecimalField(max_digits=4, decimal_places=2)
    business_class_discount = models.DecimalField(max_digits=4, decimal_places=2)
    economy_class_discount = models.DecimalField(max_digits=4, decimal_places=2)
