from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserWriteSerializer, AuthenticationSerializer, logger


class UserCreateAPIView(APIView):
	serializer_class = UserWriteSerializer

	def post(self, request):
		try:
			data = request.data
			serializer = self.serializer_class(data=data)
			serializer.is_valid(raise_exception=True)
			user = serializer.save()
			return Response({
				'message': 'Account created successfully',
				'user_id': user.id,
			}, status=status.HTTP_201_CREATED)
		except Exception as e:
			logger.error(str(e))
			return Response({
				'message': str(e),
			}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
	serializer_class = AuthenticationSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

