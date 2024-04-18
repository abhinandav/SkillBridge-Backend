from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework import serializers
from User.models import User,TeacherDetails
from TeacherApp.models import *
from StudentApp.models import *
from TeacherApp.serializers import *
from StudentApp.serializers import *




# class VideosSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Videos
#         fields= '__all__'



class OrderListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    course_name = serializers.ReadOnlyField(source='course.course_name')
    author = serializers.ReadOnlyField(source='course.added_by.username')

    class Meta:
        model = Orders
        fields = ['username','author', 'course_name', 'price', 'date_purchased']














# class AdminUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username',  'email','password','date_joined','is_active','is_superuser','is_staff', 'is_email_verified']
#         extra_kwargs = {
#             'password':{ 'write_only':True},
#             'username': {'error_messages': {'required': 'Please provide the username.'}},
#             'email': {'error_messages': {'required': 'Please provide the email address.'}},         
#         }
       
#     def create(self, validated_data):
#         password = validated_data.pop('password',None)
#         user_instance = self.Meta.model(**validated_data)
#         if password is not None:
#             user_instance.set_password(password)
#             user_instance.is_active=True
#             user_instance.save()
#         return user_instance
    

    













# class AdminUserSerializer(serializers.ModelSerializer):
#     teacher_details = TeacherDetailsSerializer(many=False, read_only=True)  # Update this line

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password', 'teacher_details', 'date_joined', 'is_active', 'is_superuser', 'is_staff', 'is_email_verified']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'username': {'error_messages': {'required': 'Please provide the username.'}},
#             'email': {'error_messages': {'required': 'Please provide the email address.'}},
#         }

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         teacher_details_data = validated_data.pop('teacher_details', None)

#         user_instance = self.Meta.model(**validated_data)

#         if password is not None:
#             user_instance.set_password(password)
#             user_instance.is_active = True
#             user_instance.save()

#         if teacher_details_data is not None:
#             TeacherDetails.objects.create(user=user_instance, **teacher_details_data)

#         return user_instance