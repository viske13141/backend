from rest_framework import viewsets,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import (
    AdminUser, Contact,
    Event, LeadershipMember, MinistryItem, Video,Booking,Ticket,Shop,Payment
)

from .serializers import (
    
    AdminSerializer, ContactSerializer, 
     EventSerializer, LeadershipMemberSerializer,
    MinistryItemSerializer, VideoSerializer,BookingSerializer,TicketSerializer,ShopSerializer,PaymentSerializer
)

@api_view(['POST'])
def create_admin(request):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all().order_by('-date_posted')
    serializer_class = AdminSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer

class LeadershipMemberViewSet(viewsets.ModelViewSet):
    queryset = LeadershipMember.objects.all()
    serializer_class = LeadershipMemberSerializer

class MinistryItemViewSet(viewsets.ModelViewSet):
    queryset = MinistryItem.objects.all()
    serializer_class = MinistryItemSerializer
    
class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-booked_at')
    serializer_class = BookingSerializer
    lookup_field = 'booking_id'  # 👈 use booking_id instead of pk (id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class PaymentCreateView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer