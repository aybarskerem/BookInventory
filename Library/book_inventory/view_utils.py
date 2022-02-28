from book_inventory.models import BookInventory

def get_books_filter_if_needed(request):
    '''
    Private function used by get methods to get all books and filter out some
    if necessary
    '''
    # Put all the field names inside the BookInventory model to be able to 
    # filter on all of these fields (later in this function).
    book_inventory_fields = \
        [field.name for field in BookInventory._meta.get_fields()]

    # a dictionary holding the values and the fields to apply to filter to
    # an example entry is 'author__icontains : Tol' to search all the author
    # names includes the text Tol such as Tolstoy
    filter_params = {}
    for field in book_inventory_fields:
        query_value = request.GET[field] if field in request.GET else None
        if query_value is not None: # an empty field might be valid in the future
            filter_params[field+"__icontains"] = query_value

    books = BookInventory.objects.all()
    return books.filter(**filter_params)