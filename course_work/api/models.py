from django.db import models
from django.urls import reverse

from core.models import AdvUser
from core.utilities import get_timestamp_path
# Create your models here.

class Outfit(models.Model):
    title = models.CharField(max_length=40, default=0, verbose_name='Образ')
    price = models.FloatField(default=0, verbose_name='Цена')
    image = models.ImageField(upload_to=get_timestamp_path, \
                                     verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.SET_NULL, \
                            null=True, related_name='my_outfits', \
                            verbose_name='Автор образа')
    likes = models.ManyToManyField(AdvUser, blank=True, \
                                    related_name='outfits')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('api:page_outfits')

    def get_api_like_url(self):
        return reverse('api:like-api-toggle', kwargs={'pk': self.pk})
    # def count_fans(self):
    #     self.fans = len(self.fans)
    #     return self.fans


# class UserOutfitRelation(models.Model):
#     RATE_CHOICES = (
#         (1, 'Ok'),
#         (2, 'Fine'),
#         (3, 'Good'),
#         (4, 'Amazing'),
#         (5, 'Incredible')
#     )
#
#     user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
#     # user = models.ManyToManyField(AdvUser)
#     outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
#     like = models.BooleanField(default=False)
#     rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
#
#     def __str__(self):
#         return f'id: {self.user.id} {self.user.username}: {self.outfit.title}, RATE {self.rate}'
