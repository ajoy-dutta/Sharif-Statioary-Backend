from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import*
from .serializers import*
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User=get_user_model()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class UserRegistrationView(ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()  # Replace `User` with your model name
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Log received data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Registration successful"},
            status=status.HTTP_201_CREATED
        )



class StaffListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = StaffApproveSerializer

class StaffApproveView(generics.RetrieveUpdateDestroyAPIView):  # GET, PUT, DELETE
    permission_classes = [IsAdmin]

    queryset = User.objects.all()
    serializer_class = StaffApproveSerializer
    # lookup_field = "id"  # Users will be accessed using their ID

    def update(self, request, *args, **kwargs):
        """Update user's approval status"""
        user = self.get_object()

        # Convert "true"/"false" strings to actual boolean values
        is_approved = request.data.get("is_approved")
        if isinstance(is_approved, str):
            is_approved = is_approved.lower() == "true"

        try:
            user.is_approved = is_approved
            user.save()
            return Response(
                {"message": f"User {user.username} approval status updated successfully."},
                status=status.HTTP_200_OK,
            )
        except IntegrityError:
            return Response(
                {"error": "Database integrity error. Check related data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        """Delete the user"""
        user = self.get_object()
        user.delete()
        return Response(
            {"message": f"User {user.username} deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({"error": "User not authenticated"}, status=401)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def post(self, request):
        # Create the serializer with data and context
        print(request.data)
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication is required."}, status=401)  # Unauthorized

        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        # Check if the data is valid
        if serializer.is_valid():
            serializer.save()  # Save the new password
            return Response({"detail": "Password updated successfully."})

        # If the serializer is invalid, print the errors for debugging
        print("Validation errors:", serializer.errors)

        return Response(serializer.errors, status=400)  # Return 400 with error