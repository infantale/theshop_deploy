from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractUser

from .utilities import get_timestamp_path
# from likes.models import Like
# Create your models here.

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, \
                                        verbose_name='Прошёл активацию')

    # При удалении пользователя удаляются оставленные им объявления
    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, \
                            verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, \
                                     verbose_name='Порядок')
    super_category = models.ForeignKey('SuperCategory', \
                     on_delete=models.PROTECT, null=True, blank=True, \
                     verbose_name='Надкатегория')


# Указываем условия фильтрации
class SuperCategoryManager(models.Manager):
    # Выбирает только записи с пустым полем super_category, т.е. надкатегории
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(Category):
    objects = SuperCategoryManager()

    # def _get_child(self):
    #     return self.

    def __str__(self):
        return self.name

    # Прокси модель используется для изменения поведения модели, например, чтобы
    # включить дополнительные методы или различные мета параметры.
    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надкатегория'
        verbose_name_plural = 'Надкатегории'


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)


class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return '%s - %s' % (self.super_category.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_category__order', 'super_category__name', 'order', \
                    'name')
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Bb(models.Model):
    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, \
                                    verbose_name='Категория')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    contacts = models.TextField(verbose_name='Контакты')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, \
                                    verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, \
                                    verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True,\
                                        verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                        verbose_name='Опубликовано')

    # Перед удалением текущей записи мы перебираем и вызовом метода delete()
    # удаляем все связанные дополнительные иллюстрации
    # def delete(self, *args, **kwargs):
    #     for ai in self.additionalimage_set.all():
    #         ai.delete()
    #     super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']


class AddiionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


# class Outfit(models.Model):
#     author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, \
#                                 verbose_name='Автор образа')
#     title = models.CharField(max_length=40, default=0, verbose_name='Образ')
#     price = models.FloatField(default=0, verbose_name='Цена')
#     image = models.ImageField(blank=False, upload_to=get_timestamp_path, \
#                                 verbose_name='Изображение')
#     likes = GenericRelation(Like)
#
#     def __str__(self):
#         return self.title
#
#     @property
#     def total_likes(self):
#         return self.likes.count()
#
#     class Meta:
#         verbose_name_plural = 'Образы'
#         verbose_name = 'Образ'
