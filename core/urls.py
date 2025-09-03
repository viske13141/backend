from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from .views import (
    AdminViewSet, create_admin,
    ContactViewSet, EventViewSet, LeadershipMemberViewSet,
    MinistryItemViewSet, VideoViewSet,BookingViewSet,TicketViewSet,ShopViewSet,PaymentCreateView
)

router = DefaultRouter()


# ✅ New endpoints
router.register(r'events', EventViewSet)
router.register(r'leadership', LeadershipMemberViewSet)
router.register(r'ministries', MinistryItemViewSet)
router.register(r'shop', ShopViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'admin', AdminViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'tickets', TicketViewSet, basename='ticket') 
router.register(r'payments', PaymentCreateView, basename='payment-create') 




urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/', create_admin),
]
