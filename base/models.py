from django.db import models

class SavedCourse(models.Model):
    term = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=4)
    course_number = models.IntegerField(null=True, blank=True)
    availability = models.CharField(max_length=10)
    class_id = models.IntegerField(primary_key=True)
    seats = models.IntegerField(null=True, blank=True)
    seats_avail = models.IntegerField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title