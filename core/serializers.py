from rest_framework.serializers import Serializer, ValidationError
from rest_framework import fields, serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from .utils import send_mail_users


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:

        model = CustomUser
        fields = ('last_name', 'first_name', 'email', 'password', 'confirm_password')


    def validate(self, data):

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
                raise serializers.ValidationError({'email':" L'email ou le password est incorrect. "})
        else:
            raise serializers.ValidationError({'email':" L'email ou le password est incorrect. "})
        
        return data


class RefreshTokenSerializer(serializers.Serializer):

    token = serializers.CharField()

    def validate(self, data):

        token = data.get('token')

        if not token:
            raise serializers.ValidationError({'token':" Ancien token non renseigné "})

        return data


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


    def validate(self, data):

        user = self.context['request'].user # recuperer le user connecté
        print(user)

        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password':'Ancien mot de passe pas correct'})
        return data

    
    def save(self):

        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        return user


class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.CharField(required=True)

    def validate(self, data):

        user = self.context['request'].user # recuperer le user connecté
        print(CustomUser.objects.filter(email = data.get('email')).first())

        if not CustomUser.objects.filter(email = data.get('email')).first() :
            raise serializers.ValidationError({'email':"Cette adresse n'appartient à aucun utilisateur actif"})
        return data

    
    def save(self):

        user = self.context['request'].user
        
        # send mail
        if user.last_name or user.first_name :
            name = user.last_name + ' ' + user.first_name
        else : 
            name = user.email

        template = "core/template_mail.html"
        subject = 'Réinitialisation du mot de passe'
        context_mail = {"name": name}
        email = [user.email,]
        has_send = send_mail_users(template = template, subject = subject, receivers = email, context = context_mail)
        
        return user


class ProfileChangeSerializer(serializers.Serializer):

    profile_picture = serializers.ImageField(allow_empty_file=True, required = False)

    class Meta:

        model = CustomUser
        fields = ('profile_picture')

        
    def validate(self, data):

        user = self.context['request'].user # recuperer le user connecté
        print(data.get('profile_picture'))

        if not data.get('profile_picture'):
            print(data.get('profile_picture'))
            raise serializers.ValidationError({'profile_picture':'Photo de profil non renseignée'})
        return data

    
    def save(self):

        user = self.context['request'].user
        user.profile_picture = self.validated_data['profile_picture']
        user.save()
        
        return user.profile_picture.url


class SearchLieuSerializer(serializers.Serializer):

    initial = serializers.CharField(required=True)

    def save(self):
        print(self.context['request'].user)
        result = []
        lieux = ["", "nsam", "Bastos", "Centre commercial", "Elig-Edzoa", "Djoungolo", "Emana", "Etoa-Meki", 
        "Mballa  ", "Mfandena ", "Ngoulemakong", "Ngousso", "Njon-essi", "Nkolmesseng", "Messassi", "Nkolondom", 
        "Nlongkak ", "Nylon ", "Okolo", "Olembe ", "Tongolo", "Manguier", "Tsinga", "Briqueterie", "Madagascar", 
        "Nkomkana", "Ntougou ", "Mokolo quartier", "Mokolo marché", "Ekoudou", "Febe", "Oliga", "Messa-Carrière", 
        "Azegue Messa Mezala", "Messa Plateau", "Angono", "Doumassi", "Ekoazon", "Cité Verte", "Etetack Abobo",
         "Grand Messa", "Messa Administratif", "Ahala", "Afanoya ", "Centre administratif", "quartier du lac", 
         "Dakar", "Efoulan", "Etoa", "Etoug-Ebe", "Mbaligi", "Méyo", "Mekoumbou", "Melen ", "Messong", "Mvan", 
         "Mvolyé", "Ngoa Ekélé", "Nyomo", "Nkol-Mbenda", "Nkolmesseng", "Nkolfon", "Nsimeyong", "Ntouessong",
          "Obili", "Obobogo", "Olezoa", "Simbock", "Mimboman ", "Mvog Mbi", "Nkomo I", "Nkomo", "Ngoa Ekelé", 
          "Biteng", "Awae ", "Ewonkan", "Nkolo", "Odza ", "Mbog Abang", "Ekoumdoum", "Kondengui", "Ekounou", "Ekie", 
          "Ndamvout", "Mvan", "Nkolndongo ", "Mimboman ", "Nkolndongo", "Mfoundassi", "Messamme", "Ndongo",
           "Toutouli", "Meyo", "Abome", "Minkan", "Mvog-Ada", "Ngousso", "Essos", "Mfandana", "Nkolmesseng",
            "Nkoul Mekong", "Quartier Fouda", "Eleveur", "Ngousso-Ntem", "Biyem-Assi", "Mendong ", "Nkolbikok ", 
            "Etoug-Ebe", "Melen", "Mvog-Betsi", "Etoug-Ebe ", "Melen", "Nkolbikok", "Etetak", "Nnom-Nnam",
             "Oyom Abang ", "Ngoulemakong", "Oyom Abang", "Ndamvouth", "Oyom Abang", "Nkomassi", "Oyom Abang ",
              "Nkolbisson", "Nkol-So", "Mbog-Doum", "Abobo", "Ebot-Mefou"]
              
        initial = self.validated_data['initial']
        # parcourir la liste et vérifier si la sous-chaîne est contenue dans chaque élément
        for chaine in lieux:
            if initial in chaine:
                result.append(chaine)
            if not initial in chaine:
                if initial in chaine.lower():
                    result.append(chaine)

        return result        
    