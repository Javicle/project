from django.contrib import admin

# Register your models here.
from .models import Carousel, CarouselImage, Category, Tag, Article, Comment, Like, AuthorProfile, SciencePerson


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category',
                    'published_date', 'updated_date')
    list_filter = ('category', 'published_date', 'author', 'photo')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)
    filter_horizontal = ('tags',)
    autocomplete_fields = ('author', 'category')
    date_hierarchy = 'published_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username')
    autocomplete_fields = ('article', 'author')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'article__title')


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'biography')
    search_fields = ('user__username',)
    autocomplete_fields = ('user',)


@admin.register(SciencePerson)
class SciencePersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'age', 'birth_date')
    search_fields = ('name', 'description')
    autocomplete_fields = ('article',)
    list_filter = ('birth_date',)


class CarouselImageInline(admin.TabularInline):
    model = CarouselImage
    extra = 1


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    inlines = [CarouselImageInline]
    list_display = ('title',)
