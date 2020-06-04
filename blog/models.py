from django.db import models

class Blogger(models.Model):
    full_name = models.CharField('Full name', max_length=180)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    class Meta:
        pass


class Blog(models.Model):
    title = models.CharField('Title', max_length=255)
    short_description = models.TextField('Sort description', max_length=500)
    blogger_full_name = models.CharField('Blogger full name', max_length=180)
    content = models.TextField('Content', max_length=10000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        pass
    
    def save(self, *args, **kwargs):
        Blogger.objects.get_or_create(full_name=self.blogger_full_name)
        return super().save(*args, **kwargs)


