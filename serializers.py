from rest_framework import serializers
from django.db import transaction
from .models import (
     Event, LeadershipMember, MinistryItem, Video,Contact,AdminUser,Ticket,Booking,Shop,Payment
)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['registered_attendees']

class LeadershipMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipMember
        fields = '__all__'

class MinistryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinistryItem
        fields = '__all__'
        
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
        
class TicketSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='booking.event.title', read_only=True)
    paid = serializers.BooleanField(source='booking.paid', read_only=True)  # 🔄 Get paid status from Booking

    class Meta:
        model = Ticket
        fields = ['id', 'name', 'email', 'phone_number', 'paid', 'event_name']
        
class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, required=False)
    event_name = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        # Skip full validation if this is a PATCH (partial update)
        if self.instance and self.partial:
            return data

        event = data.get('event')
        requested_tickets = data.get('number_of_tickets')
        tickets_data = data.get('tickets')

        if not event or requested_tickets is None or tickets_data is None:
            raise serializers.ValidationError("Missing required booking data.")

        if event.registered_attendees >= event.max_attendees:
            raise serializers.ValidationError("This event is fully booked.")

        available_tickets = event.max_attendees - event.registered_attendees
        if requested_tickets > available_tickets:
            raise serializers.ValidationError(f"Only {available_tickets} tickets available.")

        if requested_tickets != len(tickets_data):
            raise serializers.ValidationError("Ticket details must match the number of tickets requested.")

        return data

    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        event = validated_data['event']

        with transaction.atomic():
            booking = Booking.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(booking=booking, **ticket_data)

            event.registered_attendees += booking.number_of_tickets
            event.save()

        return booking

    def update(self, instance, validated_data):
        # Only update the fields present in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    
    

        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"