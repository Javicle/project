from django.db.models import Count
from .models import Article


class DataMixin:
    title_page = None
    extra_context: dict[str, str] = {}

    def __init__(self) -> None:
        if self.title_page:
            self.extra_context['title'] = self.title_page

    @staticmethod
    def get_mixin_context(context: dict, **kwargs) -> dict[str, str]:
        context.update(kwargs)
        return context


class BaseDataMixin(DataMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = (
            Article.objects
            .select_related('author', 'category')
            .prefetch_related('tags', 'comments', 'science_persons')
            .annotate(likes_count=Count('likes'))
        )

        return self.get_mixin_context(context, **kwargs)
