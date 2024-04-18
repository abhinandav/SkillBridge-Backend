
from rest_framework import serializers
from .models import User
from StudentApp.models import *
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

class OrderWithUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='course.added_by', read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'user', 'date_purchased', 'price']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'



class ChatSenderSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['sender_username']


from rest_framework import serializers

# class OrderSerializer(serializers.ModelSerializer):
#     username = serializers.SerializerMethodField()

#     class Meta:
#         model = Orders
#         fields = ['id', 'user','username', 'course', 'price', 'date_purchased'] 

#     def get_username(self, obj):
#         print('username',obj.user.username)
#         return obj.user.username


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']

class OrderSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ['id', 'user', 'username', 'profile_pic', 'course', 'price', 'date_purchased'] 

    def get_username(self, obj):
        return obj.user.username

    def get_profile_pic(self, obj):
        # Fetch the user profile for the order's user
        user_profile = UserProfile.objects.get(user=obj.user)
        # Serialize the profile_pic field
        return UserProfileSerializer(user_profile).data['profile_pic']