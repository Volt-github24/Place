from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from core.admin import CustomUserAdmin
from .serializers import ProfileSerializer, LoginSerializer, RefreshTokenSerializer, PasswordChangeSerializer, SearchLieuSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser


# inscription
class ProfileCreateAPIView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer


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
       
        if serializer.is_valid():

            user = serializer.validated_data['user']
            login(request, user)
            profile = ProfileSerializer(user)
            token, created = Token.objects.get_or_create(user=user)
            profile_data = profile.data
            profile_data.update({'token': token.key}) 
            return Response(profile_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# redemande du token (a revoir)
class RefreshTokenView(generics.GenericAPIView):

	serializer_class = RefreshTokenSerializer
	permission_classes = [IsAuthenticated,]


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


class PasswordChangeView(generics.GenericAPIView):

	serializer_class = PasswordChangeSerializer
	permission_classes = [IsAuthenticated,]

	def post(self, request):

		serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
        
		return Response({'detail': 'Mot de passe changé avec succes'})


class SearchLieuView(generics.GenericAPIView):

	serializer_class = SearchLieuSerializer
	permission_classes = [IsAuthenticated,]

	def post(self, request):

		serializer = SearchLieuSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		result = serializer.save()
        
		return Response({'detail': result})