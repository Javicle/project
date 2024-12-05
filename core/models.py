import os

from django.db import models  # type: ignore
from django.utils.text import slugify  # type: ignore
from django.urls import reverse


def transliterate(text: str) -> str:
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }

    # Заменяем каждую букву по словарю
    return ''.join(translit_dict.get(char, char) for char in text)


# Create your models here.
def carouse_image_upload_to(instance, filename: str):
    title = instance.title
    title_slug = slugify(transliterate(title))
    if len(title_slug) >= 100:
        title_slug = title_slug[:50]

    print(
        f'Вот должен быть путь: carousel//{title_slug}/{filename}')
    return os.path.join(
        'carousel',
        title_slug,
        filename,
    )


def article_image_upload_to(instance, filename: str):
    category = instance.category

    print(category.name)
    print(instance.title)
    category_slug = slugify(transliterate(category.name))
    article_slug = slugify(transliterate(instance.title))

    if len(article_slug) > 50:
        article_slug = article_slug[:50]

    print(
        f'Вот должен быть путь: categories/{category_slug}/{article_slug}/{filename}')

    return os.path.join(
        'categories',
        category_slug,
        article_slug,
        filename,
    )


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="category")
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    photo = models.ImageField(verbose_name="Изображение продукта",
                              upload_to=article_image_upload_to, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'


class Like(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Пользователь может поставить лайк только один раз
        unique_together = ('user', 'article')

    def __str__(self):
        return f'Like by {self.user} on {self.article}'


class AuthorProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class SciencePerson(models.Model):
    name = models.CharField(max_length=100)
    article = models.ForeignKey(
        Article, related_name='science_persons', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    age = models.IntegerField(null=False)
    birth_date = models.DateField(null=False)

    def __str__(self):
        return f'{self.name} - {self.article.title}'


class Carousel(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class CarouselImage(models.Model):
    image = models.ImageField(upload_to=carouse_image_upload_to)
    carousel = models.ForeignKey(
        Carousel, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'Image for {self.carousel.title}'
