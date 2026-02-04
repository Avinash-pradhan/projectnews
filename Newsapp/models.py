from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    location = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=100, default='Avinash Pradhan')

    def __str__(self):
        return self.title


class SavedNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"
