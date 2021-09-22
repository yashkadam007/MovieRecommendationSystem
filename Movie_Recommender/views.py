from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Movie,Myrating
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from Movie_Recommender.forms import RateForm
from django.contrib.auth.models import User
from django.contrib import messages
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from .recommendation import recommend_movies

# Create your views here.
def home(request):
	movies = Movie.objects.all()[:48]
	return render(request,'Movie_Recommender/home.html',{'movies': movies})

def search(request):
	query = request.GET['query']
	movies = Movie.objects.filter(Q(title__icontains=query) | Q(genres__icontains=query))[:100]
	return render(request,'Movie_Recommender/search.html',{'movies': movies})

@login_required
def moviedetail(request,movie_id):
	movie = get_object_or_404(Movie,movieId=movie_id)

	if request.method == 'POST':
		form = RateForm(request.POST)
		if form.is_valid():
			rating = form.save(commit=False)
			rating.userId = request.user.profile
			rating.movieId = movie
			rating.save()
			messages.success(request, f'Your rating has been submitted')
			return redirect('Movie_Recommender-home')
	else:
		form = RateForm()

	context = {
		'form':form,
		'movie':movie,
	}	
	return render(request,'Movie_Recommender/moviedetail.html',context)


@login_required
def recommendations(request):
	current_user_id= request.user.profile.userId
	current_user= request.user.profile.user
	movies = pd.DataFrame(list(Movie.objects.all().values('movieId','title','genres','movie_logo')))
	current_user_rating = pd.DataFrame(list(Myrating.objects.all().filter(userId = current_user_id).values('userId','movieId','rating')))
	dataset_rating = pd.read_csv("ratings.csv")
	ratings = dataset_rating.append(current_user_rating,ignore_index=True)
	Ratings_matrix = ratings.pivot(index = 'userId', columns ='movieId', values = 'rating').fillna(0)
	R = Ratings_matrix.values
	U, sigma, Vt = svds(R, k = 50)
	sigma = np.diag(sigma)
	all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)
	preds = pd.DataFrame(all_user_predicted_ratings, columns = Ratings_matrix.columns)

	# already_rated, predictions = recommend_movies(preds, current_user_id, movies, ratings, 20)
	# user_row_number = current_user_id - 1 # User ID starts at 1, not 0
	# sorted_user_predictions = preds.iloc[user_row_number].sort_values(ascending=False) # User ID starts at 1
	
	# Get the user's data and merge in the movie information.
	# user_data = original_ratings[original_ratings.userId == (userID)]
	# user_full = (user_data.merge(movies, how = 'left', left_on = 'movieId', right_on = 'movieId').
	# 				 sort_values(['rating'], ascending=False)
	# 			 )

	# # print('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
	# # print('Recommending highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
	
	# # Recommend the highest predicted rating movies that the user hasn't seen yet.
	# recommendations = (movies[~movies['movieId'].isin(user_full['movieId'])].
	# 	 merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
	# 		   left_on = 'movieId',
	# 		   right_on = 'movieId').
	# 	 rename(columns = {user_row_number: 'Predictions'}).
	# 	 sort_values('Predictions', ascending = False).
	# 				   iloc[:num_recommendations, :-1]
	# 				  )
	# predictions = recommendations
	already_rated, predictions = recommend_movies(preds, current_user_id, movies, ratings, 20)
	movie_list = predictions['movieId'].tolist()
	already_rated_movie_list = already_rated['movieId'].tolist()
	movies = Movie.objects.filter(movieId__in=movie_list)
	already_rated_movies = Movie.objects.filter(movieId__in=already_rated_movie_list)
	context = {
		# 'current_user_id':current_user_id,
		'current_user':current_user,
		'movies':movies,
		'already_rated_movies':already_rated_movies,
	}

	return render(request,'Movie_Recommender/recommendations.html',context)