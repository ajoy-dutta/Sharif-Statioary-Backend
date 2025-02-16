from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  # Add this import
from .models import User
from .serializers import UserSerializer
User = get_user_model()
# Sign Up View
class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Sign In View
class SignInView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Find the user by email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"success": False, "message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate using the email field (which should be mapped to username in your User model)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Generate tokens for authentication
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Login successful!",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response({"success": False, "message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
