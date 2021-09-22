from django.db import models


# Create your models here.
class Movie(models.Model):
	movieId		= models.IntegerField(primary_key=True)	
	title   	= models.CharField(max_length=200)
	genres  	= models.CharField(max_length=100)
	movie_logo  = models.ImageField() 

	def __str__(self):
		return self.title

RATE_CHOICES = [
	(1,'1-Trash'),
	(1.5,'1.5-Terrible'),
	(2,'2-Bad'),
	(2.5,'2.5-Ok'),
	(3,'3-Watchable'),
	(3.5,'3.5-Good'),
	(4,'4-Very Good'),
	(4.5,'4.5-Perfect'),
	(5,'5-Master Piece'),
]

class Myrating(models.Model):
	userId  = models.ForeignKey('users.Profile',on_delete=models.CASCADE,to_field='userId') 
	movieId = models.ForeignKey(Movie,on_delete=models.CASCADE,to_field='movieId')
	rating 	= models.FloatField(choices=RATE_CHOICES, blank=True,null=True)