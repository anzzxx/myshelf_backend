from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerilizer,CustomLoginSerializer,UserProfileSerializer,UserProfileEditSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

class SignupView(APIView):
    permission_classes=[]
    
    def post(self,request):
        serializer=SignupSerilizer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            
            return Response(
                {
                    "message":"user registerd succesfully", 
                    "user":{
                        "id":user.id,
                        "username":user.username,
                        "email":user.email
                    },
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
class LoginView(APIView):
    permission_classes=[]
        
    def post(self,request):
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED) 
    
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=400)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)            
        
        

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response({
            "message": "Profile details fetched successfully",
            "data": serializer.data
        }, status=200)
    

class UserProfileEditView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        user = request.user
        serializer = UserProfileEditSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)