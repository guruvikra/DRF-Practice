from django.contrib import admin
# from .models import *
from Restaurent.models import *
# Register your models here.
admin.site.register(AdminUser)
admin.site.register(Restaurent)
admin.site.register(BookTabel)
admin.site.register(TabelInfo)
admin.site.register(person)
admin.site.register(Persons)
admin.site.register(Bookings)
admin.site.register(Transactions)
admin.site.register(Favorite)
admin.site.register(Review)
admin.site.register(MoneyWallet)
admin.site.register(BookingTable)
# admin.site.register(ExampleRestaurant)
admin.site.register(Food) 
# admin.site.register(Practiceone) 
# admin.site.register(BaseModel) 
# admin.site.register(OnlineFoodOrder)
admin.site.register(Student)
admin.site.register(marks)