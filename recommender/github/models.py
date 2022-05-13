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

class GithubRepos(models.Model):
    full_name=models.CharField(max_length=500,blank=True)
    owner=models.CharField(max_length=500,blank=True)
    github_url=models.URLField(max_length=500,blank=True)
    homepage=models.URLField(max_length=500,blank=True)
    created_at=models.DateTimeField(max_length=500,blank=True)
    fork_counts=models.IntegerField(default=0)
    open_issues=models.IntegerField(default=0)
    stargazers_count=models.IntegerField(default=0)
    watchers=models.IntegerField(default=0)
    description=models.TextField(max_length=1000,blank=True)
    topics=models.TextField(max_length=1000,blank=True)
    languages=models.TextField(max_length=1000,blank=True)
    content=models.TextField(max_length=1000,blank=True)