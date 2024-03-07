from django.db import models
from .manager import RegularUserManager
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,User,BaseUserManager
from django.db.models import Avg
import uuid
# import datetime
# Create your models here.


class AdminUser(AbstractBaseUser):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    objects=RegularUserManager()
    USERNAME_FIELD='username'
    def __str__(self) -> str:
        return self.username

class Restaurent(models.Model):
    Admin=models.ForeignKey(User,on_delete=models.CASCADE)
    Restname=models.CharField(max_length=50)
    totaltabel=models.IntegerField(default=10)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=0)
    
    def __str__(self) -> str:
        return f"{self.Restname} owner name is {self.Admin.id}" 
    
    
    
    
    
class BookTabel(models.Model):
    restaurent=models.ForeignKey(Restaurent,on_delete=models.CASCADE)
    tabelno=models.IntegerField()

    noofperson=models.IntegerField()
    intime=models.TimeField()
    outtime=models.TimeField()
    
    def __str__(self) -> str:
        return f"Tabel no {self.tabelno} is booked "

class person(models.Model):
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=10)
    address=models.TextField()
    restaurent=models.ForeignKey(Restaurent,on_delete=models.CASCADE,default=1)
    tabelno=models.IntegerField()
    
class TabelInfo(models.Model):
    tabel=models.ForeignKey(BookTabel,on_delete=models.CASCADE)
    persons=models.ManyToManyField(person)


class Persons(models.Model):
    name=models.CharField(max_length=50)
    address=models.TextField()
    Phone_number=models.CharField(max_length=10)
    # tabelno=models.IntegerField(default=0)
    
class Bookings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    tabelno=models.IntegerField(null=True,default=0)
    noofpersons=models.IntegerField()
    persons=models.ManyToManyField(Persons)
    # restname=models.ForeignKey(Restaurent,on_delete=models.CASCADE,null=True)
    # we should add the total money too so that the after booking we can forwarrd the payment to the front end
    class Meta:
        ordering=['-id']


class Transactions(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # bookingid=models.ForeignKey(Bookings,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=100)
    # amount=models.IntegerField()
    
    def __str__(self):
        return f"{self.user.username}'s order id {self.order_id}"
    
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'restaurant']  # Ensures a user cannot favorite a restaurant multiple times

    def __str__(self):
        return f"{self.user.username} favorites {self.restaurant.Restname}"
    
    
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    restname=models.ForeignKey(Restaurent,on_delete=models.CASCADE)
    review=models.TextField()
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=0)
    
    
    def __str__(self) -> str:
        return f"{self.review} given by user {self.user}" 
    
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        avg_rating=Review.objects.filter(restname=self.restname).aggregate(average=Avg('rating'))['average']
        self.restname.rating=avg_rating
        self.restname.save()
        
class MoneyWallet(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Totalmoney=models.IntegerField()
    
    def __str__(self) -> str:
        return f"user {self.user.username} has {self.Totalmoney} in  wallet"
    
    
    
# class Restaurenttwo(models.Model):
#     owner=models.ForeignKey(User,on_delete=models.CASCADE)
#     restname=models.CharField(max_length1=100)
#     totaa



class BookingTable(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    restname=models.ForeignKey(Restaurent,on_delete=models.CASCADE)
    tabelno=models.IntegerField(default=1)
    noofpersons=models.IntegerField(validators=[MinValueValidator(1)])
    persons=models.ManyToManyField(Persons)
    
    class Meta:
        ordering=['-id']
        
# class Online

class Food(models.Model):
    FOOD_TYPE_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
    ]
    foodname=models.CharField(max_length=100)
    description=models.TextField()
    price=models.IntegerField()
    type=models.CharField(max_length=10,choices=FOOD_TYPE_CHOICES)
    image=models.ImageField(upload_to='food/food-img')
    restname=models.ForeignKey(Restaurent,on_delete=models.CASCADE,related_name="restaurent")
    
    def __str__(self):
        return f"{self.foodname} in {self.restname.Restname}" 
# class ExampleRestaurant(models.Model):
#     owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="admin")
#     restname=models.CharField(max_length=100)
#     food_item=models.ForeignKey(Food,)



# class OnlineFoodOrder(models.Model):
#     uuid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     foods=models.ManyToManyField(Food)
#     address=models.TextField()
#     phone_number=models.CharField(max_length=10)
#     created_at=models.DateField(auto_now=True)