from django.views import generic
from django.db.models import Q
from product.models import Variant, ProductVariant
from product.models import Product

def format_search_string(fields, keyword):
    Qr = None
    for field in fields:
        q = Q(**{"%s__contains" % field: keyword})
        if Qr:
            Qr = Qr | q
        else:
            Qr = q

    return Qr


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    model = Product
    context_object_name = 'items'
    queryset = Product.objects.all()
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = self.query_filter(queryset)

        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = ProductVariant.objects.all()
        context['product'] = True
        context['variants'] = variants
        return context