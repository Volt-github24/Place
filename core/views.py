from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from core.admin import CustomUserAdmin
from .serializers import (ProfileSerializer, LoginSerializer, PasswordChangeSerializer, ResetPasswordSerializer,
					ProfileChangeSerializer, SearchLieuSerializer, ForgotPasswordSerializer, ChangeInfosSerializer)
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser


# inscription, prends les informations de l'utilisateur et les enregistre dans la base de donnees
class ProfileCreateView(generics.CreateAPIView):

	
	queryset = CustomUser.objects.all()
	serializer_class = ProfileSerializer

	@swagger_auto_schema(
		request_body=ProfileSerializer,
		operation_description="End point d'inscription, prends les informations de l'utilisateur, celles visibles plus bas et les enregistre dans la base de donnees",
		)
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)
       
		if serializer.is_valid():
         
			self.perform_create(serializer)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
        
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# End point de modification des informations du profile (username, email, last_name, first_name), tous facultatifs, prends ces informations, et les update dans la base de donnees
class ChangeInfosView(generics.CreateAPIView):

	serializer_class = ChangeInfosSerializer

	permission_classes = [IsAuthenticated,]
	authentication_classes = (TokenAuthentication,) 

	@swagger_auto_schema(
		request_body=ChangeInfosSerializer,
		operation_description="End point de modification des informations du profile (username, email, last_name, first_name), tous facultatifs, prends ces informations, et les update dans la base de donnees",
		)
	def put(self, request):

		obj = CustomUser.objects.get(pk=request.user.id)
		serializer = ChangeInfosSerializer(obj, data=request.data)

		if serializer.is_valid():
			serializer.update(serializer)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# connexion d'un utilisateur avec l'email, le password puis retourne l'ensemble des informations de l'utilisateur et le token
class LoginView(generics.GenericAPIView):

	serializer_class = LoginSerializer

	@swagger_auto_schema(
		request_body=LoginSerializer,
		operation_description="End point de connexion, prends l'email, le password puis retourne l'ensemble des informations de l'utilisateur ainsi que le token",
		)
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)
       
		if serializer.is_valid():

			user = serializer.validated_data['user']
			print(user.username)
			login(request, user)
			profile = ProfileSerializer(user)
			token, created = Token.objects.get_or_create(user=user)
			profile_data = profile.data
			profile_data.update({'token': token.key})
			profile_data.update({'username':user.username})
			profile_data.update({'date_joined':str(user.date_joined)[:19]})
			profile_data.update({'last_login':str(user.last_login)[:19]})
			profile_data.update({'admin':user.is_staff})

			if user.profile_picture:
				profile_data.update({'profile_picture': user.profile_picture.url})
			return Response(profile_data, status=status.HTTP_200_OK)
        
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# pour changer le mot de passe, prends l'ancien et le nouveau mot de passe entrés puis met a jour le mot de passe de l'utilisateur connecté si l'ancien mot de passe correspond à un utilisateur dans la base de données
class PasswordChangeView(generics.GenericAPIView):

	serializer_class = PasswordChangeSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = (TokenAuthentication,) 

	@swagger_auto_schema(
		request_body=PasswordChangeSerializer,
		operation_description="End point permettant de changer le password, prends l'ancien et le nouveau mot de passe entrés puis met a jour le mot de passe de l'utilisateur connecté si l'ancien mot de passe correspond à un utilisateur dans la base de données.",
		)
	def post(self, request):

		serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
        
		return Response({'detail': 'Mot de passe changé avec succes'})


# pour changer le mot de passe, prends le mot de passe et la confirmation de mot de passe , puis met a jour le mot de passe si l'utilisateur a recu un mail, sinon il devra d'abord cliquer sur forgot password, recevoir l'email et suivre la procedure
class ResetPasswordView(generics.GenericAPIView):

	serializer_class = ResetPasswordSerializer

	@swagger_auto_schema(
		request_body=ResetPasswordSerializer,
		operation_description="End point pour changer le mot de passe, prends le mot de passe et la confirmation de mot de passe , puis met a jour le mot de passe si l'utilisateur a recu un mail, sinon il devra d'abord cliquer sur forgot password, recevoir l'email et suivre la procedure.",
		)
	def post(self, request):

		serializer = ResetPasswordSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
        
		return Response({'detail': 'Mot de passe changé avec succes'})


# changer la photo de profil, prend la photo passee dans le formulaire par l'utilisateur puis met son champs photo de profil a jour
class ProfileChangeView(generics.GenericAPIView):

	serializer_class = ProfileChangeSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = (TokenAuthentication,) 


	@swagger_auto_schema(
		request_body=ProfileChangeSerializer,
		operation_description="End point permettant de changer la photo de profil, prend la photo passee dans le formulaire par l'utilisateur puis met son champs photo de profil a jour",
		)
	def post(self, request):

		serializer = ProfileChangeSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		url = serializer.save()
		
		profile = {'url':url}
        
		return Response(profile, status=status.HTTP_200_OK)


# lien pour notifier l'utilisateur dont dont le mot de passe a été oublié, prend l'email de l'utilisateur et lui envoit un mail pour la suite de la procedure de modification de mot de passe
class ForgotPasswordView(generics.GenericAPIView):

	serializer_class = ForgotPasswordSerializer

	@swagger_auto_schema(
		request_body=ForgotPasswordSerializer,
		operation_description="End point permettant de notifier l'utilisateur dont dont le mot de passe a été oublié, prend l'email de l'utilisateur et lui envoit un mail pour la suite de la procedure de modification de mot de passe.",
		)
	def post(self, request):

		serializer = ForgotPasswordSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
        
		return Response({'email':'Nous vous avons envoyé un email pour vous communiquer la procédure à suivre.'})


# fonction permettant de retourner les suggestions en fonction de l'entree de l'utilisateur, ceci est utiisé dans la barre de recherche du frontend
class SearchLieuView(generics.GenericAPIView):

	serializer_class = SearchLieuSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = (TokenAuthentication,) 

	@swagger_auto_schema(
		request_body=SearchLieuSerializer,
		operation_description="End point de suggestions, permettant de retourner les suggestions en fonction de l'entree de l'utilisateur, ceci est utiisé dans la barre de recherche du frontend.",
		)
	def post(self, request):

		serializer = SearchLieuSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		result = serializer.save()
        
		return Response({'result': result})