from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from Restaurent.views import *

# router=DefaultRouter()
# router.register(r'bookview',Bookingview)
urlpatterns = [
    # path('',include(router.urls)),
    path('addrest',AddRestaurent.as_view()),
    path('userrest',UserRest.as_view()),
    path("all",AllUser.as_view()),
    path('restview',RestView.as_view()),
    path('Favlist',FavoriteList.as_view()),
    path('book',BookTabelview.as_view()),
    path('wallet',Wallet.as_view()),
    path('walletpayment',WalletPaymentAPIView.as_view()),
    path('wallet/addmoney',AddmoneytoWallet.as_view()),
    path('addperson',AddpersonView.as_view()),
    path('review',RestReview.as_view()),
    path("adminrestaurent",AdminRestaurent.as_view()),
    path("booking",CreateBookingsView.as_view()),
    path('payment',RazorpayOrderView.as_view()),
    path('practice',practice.as_view()),
    path('page',Pagee.as_view()),
    path('tabel',TabelBooking.as_view()),
    path('adminview',AdminRestaurant.as_view()),
    path('view/<int:id>',Viewww.as_view()),
    path('createadmin',CreatAdmin.as_view()),
    path('student',Students.as_view()),
    path('student/marks',Marks.as_view()),
    path('student/mark',AddMarksByNameAPIView.as_view())
    # path('pay',process_payment.as_view()),
]


