from rest_framework import serializers
from .models import *

# class AdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=["username"]
        

        
        
        
class BookTabelSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookTabel
        fields='__all__'
        
        
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model=person
        fields='__all__'
        
        
            
class PersonsSerializer(serializers.ModelSerializer):
    # phone_number = serializers.CharField(max_length=10, required=False)
    class Meta:
        model = Persons
        fields = ['name', 'address', 'Phone_number']
        

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurent
        fields = ["restname"]
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # Assuming you want to serialize the username


class RestaurentSerializer(serializers.ModelSerializer):
    
    # Admin=UserSerializer(read_only=True)
    class Meta:
        model=Restaurent
        fields="__all__"

class BookingsSerializer(serializers.ModelSerializer):
    
    persons = PersonsSerializer(many=True, read_only=True)
    # restname=RestaurentSerializer(read_only=True)

    class Meta:
        model = Bookings
        fields = ['id', 'user', 'noofpersons', 'persons']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transactions
        fields="__all__"
        
# class FavoriteSerializer(serializers.ModelSerializer):
#     # user = serializers.CharField(source='user.username', read_only=True)
#     rest=RestaurentSerializer(many=False,read_only=True)
#     # restaurant = serializers.CharField(source='restaurant.name', read_only=True)


#     class Meta:
#         model=Favorite
#         fields='__all__'
        




class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'restaurant']


class ReviewSerializer(serializers.ModelSerializer):

    # user = serializers.StringRelatedField(read_only=True)
    # restname = RestaurentSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        # depth=1
        

        
class WalletSerializer(serializers.ModelSerializer):
    # user=UserSerializer(read_only=True)
    class Meta:
        model=MoneyWallet
        fields="__all__"
        


class BookingTableSerializer(serializers.ModelSerializer):
    persons = PersonsSerializer(many=True,read_only=True)

    class Meta:
        model = BookingTable
        fields = "__all__"
        
# class PersonsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Persons
#         fields = ['name', 'address', 'Phone_number', 'tabelno']

class CreateAdminSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    
    def validate(self, attrs):
        if User.objects.filter(username=attrs['username'],email=attrs['email']).exists():
            raise serializers.ValidationError("this admin is already there")
        
        return attrs
    
    def create(self, validated_data):
        user=User.objects.create_superuser(username=validated_data['username'],
                                           email=validated_data['email'],
                                           )
        user.set_password(validated_data['password'])
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return validated_data