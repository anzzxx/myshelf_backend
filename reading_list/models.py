from django.db import models
from accounts.models import Accounts
from book.models import Book

class ReadingList(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='reading_lists')
    name = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.user}"

class ListItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    list = models.ForeignKey(ReadingList, on_delete=models.CASCADE, related_name='items')
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'list')
        ordering = ['order']

    def __str__(self):
        return f"{self.book.title} in {self.list.name}"
