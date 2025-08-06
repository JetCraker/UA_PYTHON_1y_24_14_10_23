from django.db import models


class Rubric(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rubric.name} - {self.title}'

