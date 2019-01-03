
from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
# Create your views here.
class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args , **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        context['query']= self.request.GET.get('q')
        return context

    def get_queryset(self , *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q' , None)
        print(query)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
        '''

        __icontains = field contains this
        __iexact = fields is exactly this
        '''
