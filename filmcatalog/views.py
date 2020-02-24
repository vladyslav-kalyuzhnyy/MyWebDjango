from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Actor, Genre
from .forms import ReviewForm, AuthUserForm, RegisterUserForm


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    """Movies List"""
    context_object_name = "movie_list"
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie_list.html"


class MovieDetailView(GenreYear, DetailView):
    """Movie Details"""
    model = Movie
    slug_field = "url"
    template_name = "movies/movie_detail.html"


class CatalogLoginView(LoginView):
    template_name = 'movies/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('edit_page')


class RegisterUserView(ListView):
    model = User
    template_name = 'movies/register_page.html'
    form_class = RegisterUserForm
    success_msg = 'Success!'



class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    template_name = 'movies/movie_list.html'

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset
