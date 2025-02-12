# Authentication/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class SignUpView(APIView):
    def post(self, request):
        # Validate and deserialize the request data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new user to the database
            serializer.save()
            return Response({"success": True, "message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
