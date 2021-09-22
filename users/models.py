from django.db import models
from django.contrib.auth.models import User
from PIL import Image

def from_611():
    '''
    Returns the next default value for the `ones` field,
    starts from 500
    '''
    # Retrieve a list of `YourModel` instances, sort them by
    # the `ones` field and get the largest entry
    largest = Profile.objects.all().order_by('userId').last()
    if not largest:
        # largest is `None` if `YourModel` has no instances
        # in which case we return the start value of 500
        return 611
    # If an instance of `YourModel` is returned, we get it's
    # `userId` attribute and increment it by 1
    return largest.userId + 1

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userId = models.IntegerField(primary_key=True, default=from_611)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self) :
    #   super().save()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            

