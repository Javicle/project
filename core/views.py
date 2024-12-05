from django.db.models import Count
from django.views.generic import TemplateView
from .utils import DataMixin, BaseDataMixin


# Create your views here.
class IndexHome(BaseDataMixin, TemplateView):
    title_page = "Главная"
    template_name = 'core/index.html'

class Test(BaseDataMixin, TemplateView):
    title_page = "тест"
    template_name = 'core/test.html'

    
