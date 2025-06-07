

def categories_processor(request):
    from store.models import CategoryModel
    categories = CategoryModel.objects.all()
    return {'categories': categories}


def category_processor_nested(request):
    from store.models import CategoryModelMPTT
    # categories_nested = CategoryModelMPTT.objects.root_nodes()  # N+1 query
    categories_nested = CategoryModelMPTT.objects.root_nodes().prefetch_related('children')  #TODO: check optimiz.
    return {'categories_nested': categories_nested}