from urllib.parse import non_hierarchical
from django.shortcuts import render

# Create your views here.
from book_inventory.models import BookInventory
from book_inventory.serializers import BookInventorySerializer

from book_inventory import view_utils

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

# Add ReDoc and Swagger-UI Rest API documentation with the help of
# drf_spectacular tool.
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes


class BookInventoryView(APIView):
    '''
    Apply operations that are applied on the book inventory as a whole. 
    
    Append <id> to the url (e.g. /api/books/<id>) to go to the specified book's
    page.
    '''
    
    @extend_schema(
        responses={200: BookInventorySerializer}, 
        methods=['GET'])
    def get(self, request):
        '''
        Lists all the books in the book inventory.
        '''
        book_inventory_serializer = \
        BookInventorySerializer(
                view_utils.get_books_filter_if_needed(request),
            many=True)
        return Response(book_inventory_serializer.data)

    @extend_schema(
        request=BookInventorySerializer, 
        responses={
            201: BookInventorySerializer, # Created (successfully)
            400: None # Bad Request
        },
    methods=['POST'])
    def post(self, request):
        '''
        Creates a new book in the book inventory. 
        '''
        book_inventory_serializer = BookInventorySerializer(data=request.data)
        if book_inventory_serializer.is_valid():
            book_inventory_serializer.save()
            return Response(book_inventory_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(book_inventory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        request=BookInventorySerializer, 
        responses={204: None}, # No Content (success with no return body)
    )
    def delete(self, request):  
        '''
        Deletes all the books in the database.
        '''  
        BookInventory.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SelectedBookView(APIView):
    '''
    Apply the operations on the book specified (selected) with the given id.
    '''
    error404 = None # 404 response object if no book with the given id is found

    def dispatch(self, request, *args, **kwargs):
        try: 
            id = kwargs["id"]
            self.book = BookInventory.objects.get(pk=id) 
        except BookInventory.DoesNotExist:
            self.error404 = Response(
                {'error': f'No book with id {id} exists'}, 
                status=status.HTTP_404_NOT_FOUND) 
        return super().dispatch(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: BookInventorySerializer,
            404: OpenApiTypes.OBJECT
        }, 
    )
    def get(self, request, id):  
        '''
        List the details of the selected book.
        '''
        if self.error404:
            return self.error404
        book_inventory_serializer = BookInventorySerializer(self.book) 
        return Response(book_inventory_serializer.data) 

    @extend_schema(
        request=BookInventorySerializer, 
        responses={
            200: BookInventorySerializer,
            404: OpenApiTypes.OBJECT
        }
    )
    def patch(self, request, id):  
        '''
        Update the book either partially or completely.
        '''
        if self.error404:
            return self.error404
        book_inventory_serializer = \
        BookInventorySerializer( self.book, data=request.data, partial=True) 

        if book_inventory_serializer.is_valid(): 
            book_inventory_serializer.save() 
            return Response(book_inventory_serializer.data)

        return Response(
            book_inventory_serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST) 

    @extend_schema(
        request=BookInventorySerializer, 
        responses={
            200: BookInventorySerializer,
            404: OpenApiTypes.OBJECT
        }
    )
    def put(self, request, id):  
        '''
        At least, updates the required fields of the selected book (Normally,
        PUT should replace the book completely; but this implementation is
        deemed enough for simplicity purposes) as POST with the required fields
        is enough too. 
        '''
        if self.error404:
            return self.error404
        book_inventory_serializer = \
        BookInventorySerializer( self.book, data=request.data, partial=False) 

        if book_inventory_serializer.is_valid(): 
            book_inventory_serializer.save() 
            return Response(book_inventory_serializer.data)

        return Response(
            book_inventory_serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST) 


    @extend_schema(
        request=BookInventorySerializer, 
        responses={
            204: None,  # No Content (success with no return body)
            404: OpenApiTypes.OBJECT
        }, 
        methods=['DELETE'])
    def delete(self, request, id):  
        '''
        Deletes the selected book.
        '''
        if self.error404:
            return self.error404
        self.book.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    request=BookInventorySerializer, 
    responses={
        200: BookInventorySerializer,
        404: None
    }, 
    methods=['PATCH', 'PUT'])
@extend_schema(
    request=BookInventorySerializer, 
    responses={
        204: None,  # No Content (success with no return body)
        404: None
    }, 
    methods=['DELETE'])
@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def book_details(request, id):
    '''
    Apply operations on the book specified with the given id.

    - If the request is GET, list this book. 

    - If PATCH,  update the book either partially or completely. 

    - If PUT,    update the required fields of the
    book (Normally, PUT should replace the book completely; but this
    implementation is deemed enough for simplicity purposes) as POST with the
    required fields is enough too. 

    - If DELETE, delete the book.
    '''

    try: 
        book = BookInventory.objects.get(pk=id) 
    except BookInventory.DoesNotExist: 
        return Response(
            {'error': f'No book with id {id} exists'}, 
            status=status.HTTP_404_NOT_FOUND) 

 
    if request.method == 'GET': 
        book_inventory_serializer = BookInventorySerializer(book) 
        return Response(book_inventory_serializer.data) 
 
    elif request.method == 'PATCH' or request.method == 'PUT': 
        is_partial_update = (request.method == 'PATCH')
        book_inventory_serializer = BookInventorySerializer(
                                        book, 
                                        data=request.data, 
                                        partial=is_partial_update) 

        if book_inventory_serializer.is_valid(): 
            book_inventory_serializer.save() 
            return Response(book_inventory_serializer.data)

        return Response(
            book_inventory_serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        book.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)


def  list_all(request):
    '''
    List all of the books in the database    
    '''
    context = {
        'books': view_utils.get_books_filter_if_needed(request)
    }
    return render(request, "list.html", context)

def list_one(request, id):
    '''
    List the book with with the @param id.
    '''
    book = BookInventory.objects.get(pk=id)
    context = {
        'book': book
    }
    return render(request, "list_one.html", context)