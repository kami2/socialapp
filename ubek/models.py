from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='user_avatar', default='default_avatar.png')
    about = models.TextField(default="Say something about yourself")
    birth_date = models.DateField(null=True, blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PostWall(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    like_post = models.ManyToManyField(User, related_name='liked')

    def __str__(self):
        return str(self.title)


class CommentPost(models.Model):
    post = models.ForeignKey(PostWall, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post)


class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return  "From " + str(self.from_user) + " to " + str(self.to_user)
