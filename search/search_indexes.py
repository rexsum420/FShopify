# search_indexes.py
from haystack import indexes
from products.models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
