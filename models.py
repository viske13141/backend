from django.db import models
import random
import string

class AdminUser(models.Model):
    name = models.CharField(max_length=255, default="Anonymous")

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.URLField(max_length=500)
    max_attendees = models.PositiveIntegerField()
    registered_attendees = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class LeadershipMember(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.URLField(max_length=500)    
    contact_email = models.EmailField()
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class MinistryItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(max_length=500)    
    leader = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    who_is_this_for = models.CharField(max_length=255)
    attachment = models.FileField(upload_to='contact_attachments/', blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    number_of_tickets = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)
    booking_id = models.CharField(max_length=15, unique=True, null=True, blank=True)
    # paid = models.BooleanField(default=False)  # ⬅️ Moved here from Ticket
    paid = models.CharField(
        max_length=20,
        choices=[("stripe", "Stripe"), ("paypal", "PayPal"), ("false", "Not Paid")],
        default="false"
    )

    def _generate_booking_id(self):
        """Generate a random 10-digit booking ID with 'bid' prefix."""
        return 'bid' + ''.join(random.choices(string.digits, k=10))

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = self._generate_booking_id()
            while Booking.objects.filter(booking_id=self.booking_id).exists():
                self.booking_id = self._generate_booking_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.event.title} on {self.booked_at.strftime('%Y-%m-%d')}, ID: {self.booking_id}"


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="tickets")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Ticket for {self.name} ({'Paid' if self.booking.paid else 'Unpaid'})"  # ⬅️ Status based on booking
    
class Payment(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    item_name = models.CharField(max_length=255,default="item1")
    payer_name = models.CharField(max_length=255)
    payer_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.payer_email}"

class Shop(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(max_length=500)    

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
    
   