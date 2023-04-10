from rest_framework.serializers import Serializer, ValidationError
from rest_framework import fields, serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    profile_picture = serializers.ImageField(required=True)

    class Meta:

        model = CustomUser
        fields = ('last_name', 'first_name', 'email', 'password', 'confirm_password', 'profile_picture')


    def validate(self, data):

        profile_picture = data.get('profile_picture')

        if not profile_picture:
            data['profile_picture'] = 'default_picture.jpg'

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Les mots de passe ne correspondent pas.'})
        
        if CustomUser.objects.filter(email = data.get('email')).exists():
            raise serializers.ValidationError({'email': 'Adresse email deja existante.'})
        
        return data



    def create(self, validated_data):

        validated_data.pop('confirm_password')
        print(validated_data)
        user = CustomUser.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

   
    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data["user"] = user
            else:
                raise serializers.ValidationError(" L'email ou le password est incorrect. ")
        else:
            raise serializers.ValidationError(" L'email ou le password est incorrect. ")
        print(data, "j'affiche les datas")
        return data


class RefreshTokenSerializer(serializers.Serializer):

    token = serializers.CharField()

    def validate(self, data):

        token = data.get('token')

        if not token:
            raise serializers.ValidationError(" Ancien token non renseigné ")

        return data


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


    def validate(self, data):

        user = self.context['request'].user # recuperer le user connecté
        print(user)

        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError('Ancien mot de passe pas correct')
        return data

    def save(self):

        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        return user


class SearchLieuSerializer(serializers.Serializer):

    initial = serializers.CharField(required=True)

    def save(self):

        result = []
        lieux = ["", "nsam", "Bastos", "Centre commercial", "Elig-Edzoa", "Djoungolo", "Emana", "Etoa-Meki", "Mballa  ", "Mfandena ", "Ngoulemakong", "Ngousso", "Njon-essi", "Nkolmesseng", "Messassi", "Nkolondom", "Nlongkak ", "Nylon ", "Okolo", "Olembe ", "Tongolo", "Manguier", "Tsinga", "Briqueterie", "Madagascar", "Nkomkana", "Ntougou ", "Mokolo quartier", "Mokolo marché", "Ekoudou", "Febe", "Oliga", "Messa-Carrière", "Azegue Messa Mezala", "Messa Plateau", "Angono", "Doumassi", "Ekoazon", "Cité Verte", "Etetack Abobo", "Grand Messa", "Messa Administratif", "Ahala", "Afanoya ", "Centre administratif", "quartier du lac", "Dakar", "Efoulan", "Etoa", "Etoug-Ebe", "Mbaligi", "Méyo", "Mekoumbou", "Melen ", "Messong", "Mvan", "Mvolyé", "Ngoa Ekélé", "Nyomo", "Nkol-Mbenda", "Nkolmesseng", "Nkolfon", "Nsimeyong", "Ntouessong", "Obili", "Obobogo", "Olezoa", "Simbock", "Mimboman ", "Mvog Mbi", "Nkomo I", "Nkomo", "Ngoa Ekelé", "Biteng", "Awae ", "Ewonkan", "Nkolo", "Odza ", "Mbog Abang", "Ekoumdoum", "Kondengui", "Ekounou", "Ekie", "Ndamvout", "Mvan", "Nkolndongo ", "Mimboman ", "Nkolndongo", "Mfoundassi", "Messamme", "Ndongo", "Toutouli", "Meyo", "Abome", "Minkan", "Mvog-Ada", "Ngousso", "Essos", "Mfandana", "Nkolmesseng", "Nkoul Mekong", "Quartier Fouda", "Eleveur", "Ngousso-Ntem", "Biyem-Assi", "Mendong ", "Nkolbikok ", "Etoug-Ebe", "Melen", "Mvog-Betsi", "Etoug-Ebe ", "Melen", "Nkolbikok", "Etetak", "Nnom-Nnam", "Oyom Abang ", "Ngoulemakong", "Oyom Abang", "Ndamvouth", "Oyom Abang", "Nkomassi", "Oyom Abang ", "Nkolbisson", "Nkol-So", "Mbog-Doum", "Abobo", "Ebot-Mefou"]
        initial = self.validated_data['initial']
        # parcourir la liste et vérifier si la sous-chaîne est contenue dans chaque élément
        for chaine in lieux:
            if initial in chaine:
                result.append(chaine)
            if not initial in chaine:
                if initial in chaine.lower():
                    result.append(chaine)

        return result        
    