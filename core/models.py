from django.db import models


class GithubLinkMixin(models.Model):
    github_url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True
