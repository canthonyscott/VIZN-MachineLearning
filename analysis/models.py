from django.db import models

# Create your models here.


class Result(models.Model):
    filename = models.CharField(max_length=255)
    results = models.BinaryField()
    datetime = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='results')
    plate_size = models.IntegerField()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return self.filename


