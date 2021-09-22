from django.urls import path
from.import views
urlpatterns = [
    path('', views.home,name='Movie_Recommender-home'),
    path('search/', views.search,name='Movie_Recommender-search'),
    path('moviedetail/<int:movie_id>/', views.moviedetail,name='Movie_Recommender-moviedetail'),
    path('recommendations/', views.recommendations,name='Movie_Recommender-recommendations'), 
]