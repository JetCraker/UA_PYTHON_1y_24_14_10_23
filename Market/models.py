from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    age = models.IntegerField()
    mail = models.EmailField()
    test2 = models.IntegerField(default=100)


class Passport(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='passport')
    serial_number = models.IntegerField()


class Musician(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    instrument = models.CharField(max_length=100)
    test = models.CharField(max_length=100)


class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_start = models.IntegerField()
    test = models.IntegerField(default=10)
    test2 = models.IntegerField(default=10)

class Listener(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18, blank=True, null=True)
    albums = models.ManyToManyField(Album, blank=True)


class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Чернетка'
        PUBLISHED = 'PB', 'Опубліковано'
        ARCHIVED = 'AR', 'Архівовано'


    title = models.CharField(max_length=200, verbose_name='Назва книги')
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='books')
    pages = models.PositiveIntegerField(default=0, verbose_name='Кількість сторінок')
    is_published = models.BooleanField(default=False, verbose_name='Чи опубліковано')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 1)
        return 0

    def stars_range(self):
        return range(int(self.average_rating()))

    def __str__(self):
        return f"{self.title} - {self.author}"


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user} - {self.book} ({self.value})"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
