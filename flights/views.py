from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger


# Create your views here.
def index(request):
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, 'flights/index.html', context)


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight Does not Exist")
    context = {
        "flight": flight,
        "passengers": flight.flight_passengers.all(),
        "non_passenger": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, 'flights/flight.html', context)


def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        flightname = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=passenger_id)
    except KeyError:
        return render(request, "flights/error.html", {'message': "KeyError"})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {'message': "flight Does not exist"})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {'message': "Passenger Does not exist"})

    passenger.flights.add(flightname)
    return HttpResponseRedirect(reverse("book", args=(flight_id,)))
