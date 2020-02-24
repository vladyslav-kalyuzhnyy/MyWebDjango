from django.urls import path

from . import views

urlpatterns = [
    path("", views.MoviesView.as_view()),
    path("login/", views.CatalogLoginView.as_view(), name="login_page"),
    path("register/", views.RegisterUserView.as_view(), name="register_page"),
    path("filter/", views.FilterMoviesView.as_view(), name="filter"),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor"),
]
