from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Category Model"""
    name = models.CharField('Category', max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    """Actors Model"""
    name = models.CharField('Actor', max_length=100)
    age = models.PositiveSmallIntegerField('Age', default=0)
    description = models.TextField('Description')
    image = models.ImageField('Actor Photo', upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor', kwargs={"slug": self.name})

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'


class Genre(models.Model):
    name = models.CharField('Genre', max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    """Movies Model"""
    title = models.CharField('Title', max_length=100)
    tagline = models.CharField('Movie tag', max_length=150, default='')
    description = models.TextField('Description')
    poster = models.ImageField('Poster', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Year of Movie', default=2020)
    country = models.CharField('Country', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='Director', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Actors', related_name='film_actors')
    genres = models.ManyToManyField(Genre, verbose_name='Genres')
    world_premiere = models.DateField('Date of World Premiere', default=date.today)
    budget = models.PositiveIntegerField('Budget', default=0, help_text='Value - USD')
    fees_in_usa = models.PositiveIntegerField('Fees in USA', default=0, help_text='Value - USD')
    fees_in_world = models.PositiveIntegerField('Fees in World', default=0, help_text='Value - USD')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField('Draft', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class MovieShots(models.Model):
    """Movie ScreenShots Model"""
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description')
    image = models.ImageField('Screenshot', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Movie', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Screenshot'
        verbose_name_plural = 'Screenshots'


class RatingStar(models.Model):
    """Rating Stars Model"""
    value = models.PositiveIntegerField('Value', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Rating Star'
        verbose_name_plural = 'Rating Stars'
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField('IP Address', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Star')
    movie = models.ForeignKey(Movie, on_delete=models.CharField, verbose_name='Movie')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Your name', max_length=100)
    text = models.TextField('Your text', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Parent', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='Movie', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
