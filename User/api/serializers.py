from rest_framework import serializers
from User.models import User,TeacherDetails
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from User.models import *
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        # ...
        return token
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)



class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({"password": "Password is required."})



class TeacherRegisterSerializer(UserRegisterSerializer):
    class Meta(UserRegisterSerializer.Meta):
        fields = UserRegisterSerializer.Meta.fields

    def create(self, validated_data):
        user_instance = super().create(validated_data)
        user_instance.is_staff = True
        user_instance.save()
        return user_instance


class TeacherDetailsSerializer(serializers.ModelSerializer):
    # user_profile = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = TeacherDetails
        fields='__all__'
        


class TeacherDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherDocument
        fields='__all__'
        # fields = ['id_proof', 'photo_proof','tenth_proof', 'plustwo_proof', 'graduation_proof', 'experience_proof' ]

    def create(self, validated_data):
        return TeacherDocument.objects.create(**validated_data)
    









