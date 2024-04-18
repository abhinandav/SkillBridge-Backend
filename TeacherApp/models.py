from django.db import models
from User.models import User


class Course(models.Model):
    course_name=models.CharField(max_length=250)
    added_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User")
    description=models.TextField()
    category=models.CharField(max_length=250,blank=True,null=True)
    level=models.CharField(max_length=250)
    demo_video=models.FileField(upload_to='video/demo_video',null=True,blank=True)
    thumbnail=models.FileField(upload_to='video/thumbnail',null=True,blank=True)
    benefit1=models.CharField(max_length=250,blank=True,null=True)
    benefit2=models.CharField(max_length=250,blank=True,null=True)
    benefit3=models.CharField(max_length=250,blank=True,null=True)

    date_added=models.DateField(auto_now_add=True)

    original_price=models.CharField(max_length=250)
    offer_price=models.CharField(max_length=250)

    is_accepted=models.BooleanField(default=False)
    is_blocked=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    reject_reason=models.TextField(null=True,blank=True)


    def __str__(self) -> str:
        return f" {self.course_name} added by {self.added_by.username}"
    

class Videos(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="Course")
    video_name=models.CharField(max_length=250)
    description=models.TextField()
    video=models.FileField(upload_to='video/videos',blank=True,null=True)
    is_accepted=models.BooleanField(default=False)
    is_blocked=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    rejected_reason=models.TextField(null=True,blank=True)
    duration=models.CharField(blank=True, null=True)


    def __str__(self) -> str:
        return f" {self.video_name} of {self.course.course_name}  added by {self.course.added_by.username}"
    
