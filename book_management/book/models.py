from django.db import models
from accounts.models import Accounts

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    genre_cover=models.ImageField(upload_to="genre/cover")
    is_active=models.BooleanField(default=True)
    created_by = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="genres")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    book_file = models.FileField(upload_to='books/pdf/', blank=True, null=True)
    cover_image = models.ImageField(upload_to="cover/image")
    page_count = models.IntegerField()
    reading_time = models.IntegerField(help_text="Time in minutes")
    published_date = models.DateField()
    is_active=models.BooleanField(default=True)
    language = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserBookStatus(models.Model):
    STATUS_CHOICES = [
        ('to_read', 'To Read'),
        ('reading', 'Reading'),
        ('read', 'Read')
    ]

    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)  # assuming Accounts is your user model
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='to_read')
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="Rating out of 5")
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')  # prevents duplicate entries

    def __str__(self):
        return f"{self.user} - {self.book.title} - {self.status}"
