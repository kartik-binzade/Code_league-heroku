from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=30, default="None of the above")
    is_mentor = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Comment(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Answer(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment)


class Questions(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment)
    answers = models.ManyToManyField(Answer)


class TimeChoice(models.Model):
    start = models.DateTimeField()
    duration = models.IntegerField()
    votes = models.IntegerField()
    voters = models.ManyToManyField(Profile)


class Classes(models.Model):
    name = models.CharField(max_length=240)
    description = models.CharField(max_length=5000)
    attendees = models.ManyToManyField(Profile)
    comments = models.ManyToManyField(Comment)
    times = models.ManyToManyField(TimeChoice)


class Group(models.Model):
    name = models.CharField(max_length=240)
    description = models.CharField(max_length=5000)
    attendees = models.ManyToManyField(Profile)
    comments = models.ManyToManyField(Comment)
    classes = models.ManyToManyField(Classes)
    questions = models.ManyToManyField(Questions)
    

class BlogPost(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Entry(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}...."

class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Edits(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


class Meta:
    verbose_name_plural = 'entry'

    def __str__(self):
        return f"{self.text[:50]}...."


