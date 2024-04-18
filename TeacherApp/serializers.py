from rest_framework import serializers
from .models import Course,Videos

class CourseSerializer(serializers.ModelSerializer):
    demo_video = serializers.FileField(required=False)
    thumbnail = serializers.FileField(required=False)
    user = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields= '__all__'
        # exclude = ('is_accepted', 'is_blocked', 'is_rejected')
        
    def get_user(self, obj):
        return obj.added_by.username

class VideosSerializer(serializers.ModelSerializer):
    video = serializers.FileField(required=False)
    class Meta:
        model = Videos
        exclude = ( 'is_blocked',)
