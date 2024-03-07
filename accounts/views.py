from rest_framework.response import Response
from rest_framework.decorators import APIView
from .serializer import RegisterSerializer,LoginSerializer
from rest_framework import status
# Create your views here.


class Register(APIView):
    def post(Self,request):
        try:
            data=request.data
            ser=RegisterSerializer(data=data)
            
            if not ser.is_valid():
                return Response({
                    'data':ser.errors,
                    'msg':"something went wrong"
                },status=status.HTTP_400_BAD_REQUEST)
                
                
            ser.save()
            return Response({
                'data':ser.data,
                'msg':"account created successfully"
            },status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'msg':"wrong"
            }
            )
            
class Login(APIView):
    def post(self,request):
        try:
            data=request.data
            ser=LoginSerializer(data=data)
            if not ser.is_valid():
                return Response({
                    'data':ser.errors,
                    'msg':'not authenticated'
                })
            print(ser.data)
            token=ser.get_token(ser.data)
            return Response({
                "data":token,
                'msg':"logged in"
            })
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'msg':"wrong"
            })