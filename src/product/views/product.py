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


from collections import defaultdict

class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    model = Product
    context_object_name = 'items'
    queryset = Product.objects.filter()
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = self.query_filter(queryset)
        # Retrieve the filtering parameters from the request
        product_title = self.request.GET.get('title')
        created_at = self.request.GET.get('date')
        variant_title = self.request.GET.get('variant_title')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')

        # Filter the queryset based on the provided parameters
        query = Q()
        if product_title:
            query &= Q(title__icontains=product_title)
        if created_at:
            query &= Q(created_at__date=created_at)
        queryset = queryset.filter(query)

        if variant_title:
            queryset = queryset.filter(productvariant__variant_title__icontains=variant_title).distinct()

        if price_from and price_to:
            queryset = queryset.filter(productvariantprice__price__range=[price_from, price_to]).distinct()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_variants = ProductVariant.objects.all()
        variant_options = defaultdict(set)
        # Group variant_title options by Variant title
        for variant in product_variants:
            variant_options[variant.variant.title].add(variant.variant_title)
        context['variant_options'] = dict(variant_options)
        return context