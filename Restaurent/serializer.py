from rest_framework import serializers
from Restaurent.models import *

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
        fields =["Restname"]
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # Assuming you want to serialize the username


class RestaurentSerializer(serializers.ModelSerializer):
    
    # Admin=UserSerializer(read_only=True)
    class Meta:
        model=Restaurent
        fields=["Restname"]

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
    restname = RestaurantSerializer(read_only=True)  # Nested serializer for Restaurant

    class Meta:
        model = Review
        fields = ['id', 'user', 'restname', 'review', 'rating']

    def create(self, validated_data):
        # Create Review instance with validated data
        restname_data = validated_data.pop('restname')
        restaurant_instance = Restaurent.objects.create(**restname_data)
        review_instance = Review.objects.create(restname=restaurant_instance, **validated_data)
        return review_instance
        # depth=1
        
class ReviewNestedSerializer(serializers.ModelSerializer):
    restname = RestaurantSerializer()

    class Meta:
        model = Review
        fields = [ 'user', 'restname', 'review', 'rating']

    def create(self, validated_data):
        restname_data = validated_data.pop('restname')
        restname = Restaurent.objects.get_or_create(**restname_data)[0]
        review = Review.objects.create(restname=restname, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['restname'] = RestaurentSerializer(instance.restname).data
        return representation
        
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
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"
        
        
class marksSerializer(serializers.ModelSerializer):
    # student=StudentSerializer(read_only=True)
    class Meta:
        model=marks
        fields="__all__"