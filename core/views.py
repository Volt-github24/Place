from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer, LoginSerializer, RefreshTokenSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated


# inscription
class UserCreateAPIView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# connexion
class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer


    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# redemande du token
class RefreshTokenView(generics.GenericAPIView):

	#authentication_classes = [TokenAuthentication]
	#permission_classes = [IsAuthenticated]

	serializer_class = RefreshTokenSerializer


	def post(self, request):

		try:

			# verifier si le token est bien renseigné
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)

			# Récupérer le jeton expiré
			token = Token.objects.get(key=request.data['token'])

			# Récupérer l'utilisateur associé au jeton
			user = token.user

            # Créer un nouveau jeton pour l'utilisateur
			new_token, created = Token.objects.get_or_create(user=user)

            # Supprimer l'ancien jeton
			token.delete()

			return Response({'token': new_token.key}, status=status.HTTP_200_OK)

		except Token.DoesNotExist:

			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
