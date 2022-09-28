from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from account.models import StaffProfile
from airline.models import FareClass, ComfortsPrice, Airplane, Airport, Flight, Booking, Ticket, Discount
from .forms import TicketCodeForm


def is_gate_manager(user):
    return user.staff_profile.role == 'gate_manager'


def is_check_in_manager(user):
    return user.staff_profile.role == 'checkin_manager'


def is_supervisor(user):
    return user.staff_profile.role == 'supervisor'


@login_required
@user_passes_test(lambda u: u.is_airline_staff)
def staff_profile_redirect(request):
    if is_gate_manager(request.user):
        return redirect(reverse('gate-manager-profile'))
    if is_check_in_manager(request.user):
        return redirect(reverse('checkin-manager-profile'))
    if is_supervisor(request.user):
        return redirect(reverse('supervisor-profile'))


@login_required
@user_passes_test(is_gate_manager)
def gate_manager_profile(request):
    return render(request, 'staff_interface/gate_manager_profile.html')


@login_required
@user_passes_test(lambda u: is_gate_manager(u) or is_supervisor(u))
def register_boarding(request):
    confirmed = request.GET.get('confirmed')
    ticket_code = request.GET.get('ticket_code')
    if confirmed:
        ticket = Ticket.objects.get(ticket_code=ticket_code)
        ticket.boarding_registered = True
        ticket.save()
        result = "Registered!"
        success = True
        return render(request, 'staff_interface/checkin_passenger.html',
                      {'result': result, 'success': success, })

    if request.method == 'POST':
        form = TicketCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            success = False
            try:
                ticket = Ticket.objects.get(ticket_code=cd['ticket_code'])
            except Ticket.DoesNotExist:
                ticket = None
                result = "Ticket does not exist!"
            if ticket:
                if ticket.boarding_registered:
                    result = "Ticket is already registered!"
                    return render(request, 'staff_interface/register_boarding.html',
                                  {'form': form, 'success': success, 'result': result, })
                else:
                    flight = ticket.booking.flight
                    success = True
                    return render(request, 'staff_interface/register_boarding.html',
                                  {'form': form, 'success': success,
                                   'ticket': ticket, 'flight': flight, })

            return render(request, 'staff_interface/register_boarding.html',
                          {'form': form, 'result': result, 'success': success, })
        else:
            return render(request, 'staff_interface/register_boarding.html', {'form': form, })

    else:
        form = TicketCodeForm()
        return render(request, 'staff_interface/register_boarding.html', {'form': form, })


@login_required
@user_passes_test(is_check_in_manager)
def checkin_manager_profile(request):
    return render(request, 'staff_interface/checkin_manager_profile.html')


@login_required
@user_passes_test(lambda u: is_check_in_manager(u) or is_supervisor(u))
def checkin_passenger(request):
    confirmed = request.GET.get('confirmed')
    ticket_code = request.GET.get('ticket_code')
    if confirmed:
        ticket = Ticket.objects.get(ticket_code=ticket_code)
        ticket.checked_in = True
        ticket.save()
        result = "Checked in!"
        success = True
        return render(request, 'staff_interface/checkin_passenger.html',
                      {'result': result, 'success': success, })

    if request.method == 'POST':
        form = TicketCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            success = False
            try:
                ticket = Ticket.objects.get(ticket_code=cd['ticket_code'])
            except Ticket.DoesNotExist:
                ticket = None
                result = "Ticket does not exist!"
            if ticket:
                if ticket.checked_in:
                    result = "This passenger is already checked in!"
                else:
                    flight = ticket.booking.flight
                    success = True
                    return render(request, 'staff_interface/checkin_passenger.html',
                                  {'form': form, 'success': success,
                                   'ticket': ticket, 'flight': flight, })

            return render(request, 'staff_interface/checkin_passenger.html',
                          {'form': form, 'result': result, 'success': success, })
    else:
        form = TicketCodeForm()
        return render(request, 'staff_interface/checkin_passenger.html', {'form': form, })


@login_required
@user_passes_test(lambda u: is_check_in_manager(u) or is_supervisor(u))
def checkin_add_options(request):
    pass

@login_required
@user_passes_test(is_supervisor)
def supervisor_profile(request):
    return render(request, 'staff_interface/supervisor_profile.html')
