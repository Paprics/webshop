

def categories_processor(request):
    from store.models import CategoryModel
    categories = CategoryModel.objects.all()
    return {'categories': categories}


def category_processor_nested(request):
    from store.models import CategoryModelMPTT
    categories = CategoryModelMPTT.objects.all().order_by('tree_id', 'lft')
    return {'categories': categories}