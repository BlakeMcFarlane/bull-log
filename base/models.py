from django.db import models

class Course(models.Model):
    title=models.CharField(max_length=100,null=True,blank=True)
    subject=models.CharField(max_length=5,null=True,blank=True)
    course_number=models.IntegerField(default=0,null=True,blank=True)
    total_seats=models.IntegerField(default=0,null=True,blank=True)
    available_seats=models.IntegerField(default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title