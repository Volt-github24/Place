from rest_framework.serializers import Serializer, ValidationError
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)


    class Meta:

        model = User
        fields = ['email', 'last_name', 'first_name', 'password', 'confirm_password']

    def validate(self, data):

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Les mots de passe ne correspondent pas.'})
        if User.objects.filter(email = data.get('email')).exists():
            raise serializers.ValidationError({'email': 'Adresse email deja existante.'})
        return data

    def create(self, validated_data):

        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data, username = validated_data['email'])
        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(" Utilisateur non actif. ")
                data['user'] = user
            else:
                raise serializers.ValidationError(" L'email ou le password n'est pas correct. ")
        else:
            raise serializers.ValidationError(" L'email ou le password n'est pas correct. ")

        return data


class RefreshTokenSerializer(serializers.Serializer):

    token = serializers.CharField()

    def validate(self, data):

        token = data.get('token')

        if not token:
            raise serializers.ValidationError(" Ancien token non renseigné ")

        return data
