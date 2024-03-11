from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import BasicAuthentication
from Restaurent.models import *
from Restaurent.serializer import *
from django.contrib.auth import authenticate
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
# Create your views here.


#this view is for the user where they can we all the restaurant in the webiste or app given by the server or the admin
class UserRest(APIView):
    def get(self,request):
        data=Restaurent.objects.all()
        
        if request.GET.get('search'):
            search=request.GET.get('search')
            data=Restaurent.objects.filter(Q(Restname__icontains=search) | Q(totaltabel__icontains=search))
        ser=RestaurentSerializer(data,many=True)    
        return Response({
            "data":ser.data,
            "msg":"all Restaurent"
        })

#this view is for the reatuarent owner right now i am putting admin as owner of the restaurent and they can view their restaurent and they can view there bookings and the person coming to there restuarant
class AdminRestaurent(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAdminUser]
    def get(self,request):
        print(request.user.id)
        print(request.user)
        # this is to check who is the user
        # checking with the user with the help of request.user  
        AllRestaurent=Restaurent.objects.filter(Admin=request.user.id)
        userdata=User.objects.filter(username__icontains=Persons.name)
        foods=Food.objects.filter(restname__restname=AllRestaurent.restname)
        
        
        userser=UserSerializer(userdata,many=True)
        # pr=AllRestaurent.values_list("id")
        # print(pr[0])
        # restaure_booking=Bookings.objects.get(restaurent__id=AllRestaurent.id)
        # print(restaure_booking)
        if request.GET.get('search'):
            search=request.GET.get('search')
            AllRestaurent=Restaurent.objects.filter(Q(Restname__icontains=search) | Q(totaltabel__icontains=search))
        ser=RestaurentSerializer(AllRestaurent,many=True)
        return Response({
            "data":ser.data,
            "user":userser.data,
            "msg":"here is all restaurent"
        })
        
        
#this view is for testing purpose and this view is to view all the restaurant from the database  
class AllUser(APIView):
    def get(self,request):
        All=Restaurent.objects.all()
        ser=RestaurentSerializer(All,many=True)
        return Response({
            "data":ser.data,
            "msg":"fetched"
        })
        
        
# this view is for only the admin who can add there restaurant and add what is the name and ,how many tabel is there in restaurant we can even add more feature as i am doing for paractice i have created limited attributes
class AddRestaurent(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAdminUser]
    def post(self,request):
        try:
            data=dict(request.data)
            data['Admin']=request.user.id
            if Restaurent.objects.filter(Admin=data['Admin'],Restname=data['Restname']).exists():
                return Response({
                    "data":"restaurent with the same name by the user  exists"
                })
            ser=RestaurentSerializer(data=data)
        
            # restbookingdata=Bookings.objects.filter()
            if not ser.is_valid():
                return Response({
                    'data':ser.errors,
                    "msg":"something went wrong"
                })
            ser.save()
            return  Response({
                "data":ser.data,
                "msg":"Restaurent added"
        
            })
        except Exception as e:
            print(e)
            return Response({
                "error":str(e)
            })
    
# this view  is for the admin user but with the help of custom user that i have tried when i sharted this  prac project 

class RestView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # if AdminUser.objects.get(username=username).DoesNotExist:
        #     return Response({
        #         "data":"there is no restaurent owned by him"
        #     })
        
        user = AdminUser.objects.get(username=username,password=password)
        rest=Restaurent.objects.filter(Admin__username=username)
        infotabel=BookTabel.objects.filter(restaurent__Admin=user)
        tabelser=BookTabelSerializer(infotabel,many=True)
        persons=person.objects.filter(restaurent__Admin=user)
        personser=PersonSerializer(persons,many=True)
        ser=RestaurentSerializer(rest,many=True)
        if user is not None:
            return Response({"restaurent": ser.data,
                             "tabelinfo":tabelser.data,
                             "person":personser.data
                             })
            
            
        else:
            return Response({"data":"Invalid credentials"})
        
        
# this view is for booking the tabel from the restaurent but this not thw view i have used in the app or webapp     
class BookTabelview(APIView):
    def post(self,request):
        data=request.data
        ser=BookTabelSerializer(data=data)
        if ser.is_valid():
            name=request.data['restaurent']
            intime=request.data['intime']
            outime=request.data['outtime']
            tabelno=request.data['tabelno']
            noofpersons=request.data['noofperson']
            # user=request.data['user']
            # print(user)
            if intime==outime:
                return Response({
                    'msg':"intime is same as outtime"
                })

            
            s=Restaurent.objects.get(id=name)
            print(s.totaltabel)
            if int(tabelno)>s.totaltabel:
                return Response({
                    'msg':"invalid tabel no"
                })    
            if BookTabel.objects.filter(tabelno=tabelno).exists():
                pass
            start_time = datetime.strptime(intime, "%H:%M:%S").time()
            end_time = datetime.strptime(outime, "%H:%M:%S").time()
            if BookTabel.objects.filter(Q(intime__lt=end_time, outtime__gt=start_time) |
            Q(intime__lt=start_time, outtime__gt=start_time) |
            Q(intime__lt=end_time, outtime__gt=end_time),restaurent=name,tabelno=tabelno).exists():
                # print(Bookings.remainingcount.default)
                # count=s.tabel_count
                
                # print(BookTabel.objects.count())
                return Response({
                    'msg':"tabel is already booked at that time please go for another tabel",
                    'remaining tabel':s.totaltabel-int(tabelno)
                    })
            ser.save()
            

# Print the result

            
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
# this view is to add person who are coimg to restuarant and the view is used to show the persons and book the table for abhove book tabel view
# by this we can add the person to the tabel by one by one only
# we have to add a person  single at a time
class AddpersonView(APIView):
    def get(self,request):
        if request.GET.get('search'):
            search=request.GET.get('search')
            persons=person.objects.filter(tabelno=search)           
            ser=PersonSerializer(persons,many=True)
            return Response({
                "data":ser.data,
                'tabel no':search
            })
            
        return Response({
            'data':"search the tabel no"
        })
    def post(self,request):
        try:
            data=request.data
            name=request.data["name"]
            phn_number=request.data["phone_number"]
            tabelno=request.data["tabelno"]
            
            if person.objects.filter(name=name,phone_number=phn_number,tabelno=tabelno).count()>=1:
                return Response({
                    "data":"user is already added"
                })

            
            ser=PersonSerializer(data=data)
            tabelno=request.data['tabelno']
            restaurent=request.data['restaurent']
            tabelcount=person.objects.filter(restaurent=restaurent,tabelno=tabelno)
            restname=BookTabel.objects.get(restaurent=restaurent,tabelno=tabelno)
            if restname.noofperson<tabelcount.count()+1:
                return Response({
                    "data":"the tabel is full"
                },status=status.HTTP_204_NO_CONTENT)
            print(tabelcount.count())
            # print(restid.restaurent.Restname)
            if not ser.is_valid():
                return Response({
                    'data':ser.errors,
                    "msg":"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)
            ser.save()
            return Response({
                "data":ser.data,
                "msg":"person added"
            },status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                'data':{str(e)},
                'msg':"wrong"
            },status=status.HTTP_400_BAD_REQUEST)
            
            
# this view is to book a table and we can add all the persons coming to table at once in list that too can do by the user who is booking the tabel 
class CreateBookingsView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]    
    def get(self,request):
        user=request.user.id
        bookings=Bookings.objects.filter(user=user)
        if not bookings.exists:
            return Response({
                "data":"there no single booking booked by you",
                "msg":"you can book a table then it will show your records of booking"
            })
        ser=BookingsSerializer(bookings,many=True)
        return Response({
            "data":ser.data,
            "msg":"fetched"
        })
    def post(self, request):
        tabelperperson=500
        data=request.data
        data['user']=request.user.id
        booking_serializer = BookingsSerializer(data=data)
        

        if booking_serializer.is_valid():
            booking_instance = booking_serializer.save()
            print(booking_instance.noofpersons)
            persons_data = request.data.get('persons', [])
            person_ids = []
            for person_data in persons_data:
                person_serializer = PersonsSerializer(data=person_data)
                if person_serializer.is_valid():
                    print(len(person_ids))
                    if len(person_ids)+1>request.data['noofpersons']:#to check weather the user is not entering more persons than the no of users in to the input field
                        return Response(
                            {"data":f"you can add only {request.data['noofpersons']}"})
                    person_instance = person_serializer.save()
                    person_ids.append(person_instance.id)
                else:
                    return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            booking_instance.persons.add(*person_ids)
            totalcost=tabelperperson*booking_instance.noofpersons

            return Response({"data":booking_serializer.data,"total cost of the tabel is":totalcost} ,status=status.HTTP_201_CREATED)
        return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  #this view is for booking tabel in reataurant  
# class TabelBooking(APIView):
#     permission_classes=[IsAdminUser]
#     authentication_classes=[BasicAuthentication]
#     def get(self,request):
#         data=request.data
#         data['user']=request.user.id
#         query=BookingTable.objects.filter(user=data['user'])
#         ser=BookingsSerializer(query,many=True)
#         return Response({
#             "data":ser.data,
#             "msg":"fetched"
#         })
#     def post(self, request):
#         tabelperperson=500
#         data=request.data
#         data['user']=request.user.id
#         booking_serializer = BookingsSerializer(data=data)
        

#         if booking_serializer.is_valid():
#             booking_instance = booking_serializer.save()
#             print(booking_instance.noofpersons)
#             persons_data = request.data.get('persons', [])
#             person_ids = []
#             for person_data in persons_data:
#                 person_serializer = PersonsSerializer(data=person_data)
#                 if person_serializer.is_valid():
#                     print(len(person_ids))
#                     if len(person_ids)+1>request.data['noofpersons']:#to check weather the user is not entering more persons than the no of users in to the input field
#                         return Response(
#                             {"data":f"you can add only {request.data['noofpersons']}"})
#                     person_instance = person_serializer.save()
#                     person_ids.append(person_instance.id)
#                 else:
#                     return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             booking_instance.persons.add(*person_ids)
#             totalcost=tabelperperson*booking_instance.noofpersons

#             return Response({"data":booking_serializer.data,"total cost of the tabel is":totalcost} ,status=status.HTTP_201_CREATED)
#         return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#this view is for booking tabel in reataurant  
class TabelBooking(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        data=request.data
        data['user']=request.user.id
        query=BookingTable.objects.filter(user=data['user'])
        ser=BookingTableSerializer(query,many=True)
        return Response({
            "data":ser.data,
            "msg":"fetched"
        })
    def post(self,request):
        try:
            tabelperperson=500
            data=request.data
            data['user']=request.user.id
            booking_serializer = BookingTableSerializer(data=data)
            
            if BookingTable.objects.filter(user=data['user'],restname=data['restname'],tabelno=data['tabelno']).exists():
                return Response({
                    "data":"your booking already exists"
                })
            if booking_serializer.is_valid():
                booking_instance=booking_serializer.save()
                
                persons=request.data.get('persons',[])# here we aare passing empty list if we dont get persons then we get a empty list
                person_idx=[]# this empty list is for storing the id of the person as we have to add person to the tabel and person is mant to many field
                for p in persons:
                    ser=PersonSerializer(data=p)
                    
                    if not ser.is_valid():
                        return Response({
                            "data":ser.errors,
                        })
                        
                    if len(person_idx)+1>request.data["noofpersons"]:
                        return Response({
                            "data":f"you can add only {request.data['noofpersons']}"
                        })
                    person_instance=ser.save()
                    person_idx.append(person_instance.id)
                booking_instance.persons.add(*person_idx)
                totalcost=tabelperperson*booking_instance.noofpersons
                
                return Response({
                    "data":booking_serializer.data,
                    "cost":totalcost
                })
            else:
                return Response({
                    "data":booking_serializer.errors
                })
        except Exception as e:
            return Response({
                "data":str(e)
            })
            
            
            
            
            
            
            
            
            
# class Bookingview(ModelViewSet):
    # queryset=Bookings.objects.all()
    # serializer_class=BookingsSerializer
    # def create(self, request, *args, **kwargs):
    #     data=request.data
    #     ser=BookingsSerializer(data=data)
    #     if ser.is_valid():
    #         ser.save()
    #     perssondata=request.data.get('persons')
    #     for person in perssondata:
    #         pser=PersonsSerializer(data=person)
    #         if pser.is_valid():
    #             pser.save()
    #             Bookings.persons.add(pser.data)
    #         else:
    #                 # If person data is not valid, delete the booking and return error
    #                 Bookings.delete()
    #                 return Response(pser.errors, status=status.HTTP_400_BAD_REQUEST)
    #         return Response({
    
    #             "data":BookingsSerializer.data
    #         })
            


import razorpay

#payment intrface without the interface i.e without the front end 
class RazorpayOrderView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request):
        # id=request.data['bookingid']
        user=request.user.id
        priceperperson=500
        bookingid=Bookings.objects.filter(user=user).first()
        noofpersons=bookingid.noofpersons
        amount=noofpersons*priceperperson
        # print(type(noofpersons))
        client = razorpay.Client(auth=('rzp_test_MA9ofOgbWXUEmW', 'h0TPaVrngweM0sWzmZkAwc26'))
        # amount = request.data.get('amount')  # You should validate and sanitize user input/
        try:
            order_response = client.order.create(data={'amount': amount, 'currency': 'INR'})
            order_id = order_response['id']
            user=request.user
            transaction=Transactions.objects.create(order_id=order_id,user=user)
            transaction.save()
            return Response({'order_id': order_id,"amount":amount}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# def process_payment(request, order_id):
#     # Construct Razorpay checkout URL using the order ID
#     razorpay_checkout_url = f'https://checkout.razorpay.com/v1/payments/{order_id}/redirect'
#     return redirect(razorpay_checkout_url)


# class process_payment(APIView):
#     def post(self,request):
#         orderid=request.data['orderid']
#         razorpay_checkout_url = f'https://checkout.razorpay.com/v1/payments/{orderid}/redirect'
#         return Response({
#             'data':razorpay_checkout_url
        
#         })
        
        
        
#  this view is to add the the favorite of the person we can add multiple favorite and  if the restaurant is already is there then it will throw an error     
class FavoriteList(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        data=Favorite.objects.filter(user=request.user.id)
        ser=FavoriteSerializer(data,many=True)
        return Response({
            "data":ser.data
        })
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = FavoriteSerializer(data=data)

        if serializer.is_valid():
            user = request.user
            restaurant_id = serializer.validated_data['restaurant']
            
            if Favorite.objects.filter(user=user, restaurant=restaurant_id).exists():
                return Response({"message": "Favorite already exists"}, status=400)

            favorite = serializer.save(user=user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
       


# this view is to  write a review about the restaurant and with the rating inside the model review we are changing the rating of the restaurant using the inbuilt avg 
# we can write the review and rating of the restaurant  

class RestReview(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        data=Review.objects.filter(user=request.user.id)
        ser=ReviewNestedSerializer(data,many=True)
        return Response({
            "data":ser.data,
            "msg":"all review by you"
        })
    def post(self,request):
        data=request.data
        data['user']=request.user.id
        if Review.objects.filter(user=data['user'],restname=data['restname']).exists():
            return Response({
                "data":"already"
            })
            
        # rating=Review.objects.filter(restname=data['restname'])
        # print(rating.select_related(rating))
        
            
        ser=ReviewNestedSerializer(data=data)
        if not ser.is_valid():
            return Response({
                'data':ser.errors,
                'msg':"something went wrong"
            })
        ser.save()
        return Response({
            "data":ser.data,
            "msg":"Review saved"
        })
        
# class RestWithRating(APIView):
#     permission_classes=[IsAuthenticated]
#     authentication_classes=[JWTAuthentication]
#     def get(self,request):
#         average_rating = Review.objects.filter(restname=3).aggregate(average=Avg('rating'))['average']
        



# this review is for the user and user can only have one wallet and we can pay through the wallet which makes it more easier for the payment after booking of the table 
class Wallet(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        try:
            wallet=MoneyWallet.objects.get(user=request.user.id)
            if not wallet:
                return Response({
                    "data":"create a wallet first"
                })
            ser=WalletSerializer(wallet)
            return Response({
                "data":ser.data,
                "msg":"your wallet data"
            })
        except Exception as e:
            return Response({
                "msg": "create a wallet first "
            })
        
            
    def post(self,request):
        try:
            data=request.data
            data['user']=request.user.id
            # mutable_data = request.data.copy()
            # # Add user ID to the mutable data
            # mutable_data['user'] = request.user.id

            # Serialize the mutable data
            ser = WalletSerializer(data=data)
            if not ser.is_valid():
                return Response({
                    "data":ser.errors
                })
            
            ser.save()
            return Response({
                "data":ser.data,
                "msg":"wallet created"
            })
        except Exception as e:
            return Response({
                "data":str(e),
                "msg":"wrong"
            })
            
            
        
class WalletPaymentAPIView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'message': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = MoneyWallet.objects.get(user=request.user.id)
            if wallet.Totalmoney >= amount:
                wallet.Totalmoney-= amount
                wallet.save()
                return Response({'message': f'Payment successful. New balance: {wallet.Totalmoney}'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Wallet not found',
                             'error':str(e)
                             }, status=status.HTTP_404_NOT_FOUND)
# class AddmoneytoWallet(APIView):
#     permission_classes=[IsAuthenticated]
#     authentication_classes=[JWTAuthentication]
#     def post(self,request):
#         try:
#             data=request.data
#             userwallet=MoneyWallet.objects.get(user=request.user.id)
#             print(userwallet)
#             userwallet.Totalmoney+=data['addmoney']
#             userwallet.save()
#             return Response({
#                 "data":"money added to your wallet",
#                 "new balance":userwallet.Totalmoney
#             })
#         except Exception as e:
#             print(e)
            
            
class AddmoneytoWallet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            data = request.data
            userwallet = MoneyWallet.objects.get(user=request.user.id)
            userwallet.Totalmoney += data['addmoney']  # Add money to the existing balance
            #here we have to implment the razorpay to add real money 
            #as of now i have added the dummy money
            userwallet.save()
            return Response({
                "data": "Money added to your wallet",
                "new_balance": userwallet.Totalmoney
            }, status=status.HTTP_200_OK)
        except MoneyWallet.DoesNotExist:
            return Response({
                "error": "MoneyWallet object does not exist for this user"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
from rest_framework import mixins
from rest_framework import generics

class practice(mixins.ListModelMixin,# this mixin is to get data from database
               mixins.CreateModelMixin #this is to create 
               ,mixins.DestroyModelMixin,# this is to delete
               mixins.UpdateModelMixin # this is to update
               ,generics.GenericAPIView):
    
    
    queryset=Restaurent.objects.all()
    serializer_class=RestaurentSerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[BasicAuthentication]
    
    def perform_create(self, serializer):
        # Set the user field of the object being created to the current user
        serializer.save(Admin=self.request.user)
  

    def get(self,request,*args, **kwargs):
        return self.list(request,*args, **kwargs)
    
    def post(self,request,*args, **kwargs):
        return self.create(request,*args,**kwargs)
    
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
    
    
from rest_framework.pagination import PageNumberPagination


class MyCustomPagination(PageNumberPagination):
    page_size =2
    page_size_query_param = 'page_size'
    max_page_size = 100

class Pagee(APIView):
    pagination_class=MyCustomPagination
    
    def get(self,request):
        query_set=Restaurent.objects.all()
        paginator=self.pagination_class()
        paginated_queryset=paginator.paginate_queryset(query_set,request)
        serializers=RestaurentSerializer(paginated_queryset,many=True)
        
        return paginator.get_paginated_response(serializers.data)
    
    
# class Book(APIView):
#     def get(self,request):
#         query_set=Restaurent.objects.filter()

class AdminRestaurant(generics.ListAPIView):
    permission_classes=[IsAdminUser]
    authentication_classes=[BasicAuthentication]
    serializer_class=RestaurentSerializer
    
    def get_queryset(self):
        user=self.request.user
        return Restaurent.objects.filter(Admin=user)    
class Viewww(generics.ListAPIView):
    serializer_class=RestaurentSerializer
    def get_queryset(self):
        id=self.kwargs['id']
        return Restaurent.objects.filter(id=id)
    
class CreatAdmin(APIView):
    
    def post(self,request):
        try:
            data=request.data
            ser=CreateAdminSerializer(data=data)
            if not ser.is_valid():
                return Response({
                    "data":ser.errors,
                    "msg":"something went wrong"
                })
            ser.save()
            return Response({
                "data":ser.data,
                "msg":"super user created"
            })
        except Exception as e:
            return Response({
                "data":str(e)
            })
            
            
class orderfood(APIView):
    pass

class AddFoodAdmin(APIView):
    pass


class Students(APIView):
    def get(self,request):
        try:
            queryset=Student.objects.all()
            ser=StudentSerializer(queryset,many=True)
            return Response({
                "data":ser.data,
                "msg":"student list"
            })
            
        except Exception as e:
            return Response({
                "msg":"something went wrong",
                "data":str(e)
            })
    def post(self,request):
        try:
            data=request.data
            ser=StudentSerializer(data=data)
            if not ser.is_valid():
                return Response({
                    "data":ser.errors,
                    "msg":"something went wrong"
                })
            ser.save()
            return Response({
                "data":ser.data,
                "msg":"student created"
            })
        except Exception as e:
            return Response({
                "data":str(e),
                "msg":"something went error"
            })
            
            
class Marks(APIView):
    def get(self,request):
        stu=request.data['student']
        queryset=marks.objects.filter(student__student=stu)
        ser=marksSerializer(queryset,many=True)
        return Response({
            "data":ser.data,
            "msg":"this are the marks and grade"
        })
        
    def post(self,request):
        try:
            data=request.data
            ser=marksSerializer(data=data)
            
            if not ser.is_valid():
                return Response({
                    "data":ser.errors,
                    "msg":"data not valid"
                })
            ser.save()
            
            return Response({
                "data":ser.data,
                "msg":"added"
            })
        except Exception as e:
            return Response({
                "data":str(e),
                "msg":"Exception"
            })
            
            
class AddMarksByNameAPIView(APIView):
    def post(self, request):
        try:
            # Get student name and marks data from the request
            student = request.data.get('student')
            marks_data = request.data.get('marks')

            # Find the student by name
            student = Student.objects.get(student=student)
            e=marks.objects.filter(student__student=student)
            if e.exists():
                return Response({
                    "data":"marks already exists",
                    "msg":"add another student mark "
                })
            # Add the student ID to marks data
            marks_data['student'] = student.uuid

            # Serialize marks data
            marks_serializer = marksSerializer(data=marks_data)
            if not marks_serializer.is_valid():
                return Response(marks_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the marks instance
            marks_serializer.save()

            return Response({
                "data": marks_serializer.data,
                "msg": "Marks added for student"
            }, status=status.HTTP_201_CREATED)

        except Student.DoesNotExist:
            return Response({
                "msg": "Student does not exist",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "msg": "error",
                "data": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)