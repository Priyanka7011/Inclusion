from django.db import models

# Create your models here.
class GithubUsers(models.Model):
    login=models.CharField(max_length=500,blank=True)
    avatar_url=models.URLField(max_length=500,blank=True)
    url=models.URLField(max_length=500,blank=True)
    git_url=models.URLField(max_length=500,blank=True)
    top5_repos=models.TextField(max_length=2000,blank=True)
    name=models.CharField(max_length=500,blank=True)
    total_repos=models.IntegerField(default=0)
    all_repos=models.TextField(max_length=5000,blank=True)
    orgs=models.TextField(max_length=5000,blank=True)