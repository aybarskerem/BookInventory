from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from book_inventory.models import BookInventory


# Create your tests here.
class CreateBook(APITestCase):
    '''
    Test the correctness of POST request and the status of the resources
    afterwards.
    
    POST is non-idempotent, so no idempotency tests are performed.
    '''

    def test_create_book(self):
        initial_book_count = BookInventory.objects.count()
        new_book_fields = {
            'author': 'Superman',
            'title' : "A hero's life",
            'number_of_pages': 100,
            #'published_date': '2022-02-26'
        }
        response = self.client.post(
            reverse('book_inventory'), 
            new_book_fields, 
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            BookInventory.objects.count(),
            initial_book_count + 1,
        )
        for attr, expected_value in new_book_fields.items():
            self.assertEqual(response.data[attr], expected_value)


class ListBooks(APITestCase):
    '''
    Test GET request for correctness.
    
    GET should be idempotent.
    '''
    def setUp(self):
        NUMBER_OF_ENTRIES_TO_CREATE = 4 # some random number to do GET request
        for i in range(1, NUMBER_OF_ENTRIES_TO_CREATE+1):
            book_fields = {
                'author': f'Author {i} to update',
                'title' : f"Title {i} to update",
                'number_of_pages': i,
                'published_date': f'2022-0{i}-26'
            }
        response = self.client.post( 
            reverse('book_inventory'), 
            book_fields, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_details(self):
        response = self.client.get( reverse('book_inventory') )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('test_get_slash')
    def test_slash(self):
        '''
        Test whether putting '/' at the end of a url or not putting results
        into the same page.
        '''
        response_non_slash = self.client.get(
            reverse('book_inventory'))
        response_slash     = self.client.get(
            f'{reverse("book_inventory")}/')
        self.assertEqual(response_non_slash.data, response_slash.data)

class UpdateBook(APITestCase):
    '''
    Test the correctness of PATCH and PUT requests and the status of the
    resources afterwards.

    PUT should be idempotent whereas some PATCH operations could be
    non-idempotent (such as adding a field). Hence only PUT idempotency is
    tested.
    '''
    def setUp(self):
        book_fields = {
            'author': 'Author to update',
            'title' : "A title to update",
            'number_of_pages': -1,
            'published_date': '2022-02-26'
        }
        response = self.client.post(
            reverse('book_inventory'), 
            book_fields, 
            format='json')
        self.book_id = response.data['id']

    def test_patch_book(self):
        initial_book_count = BookInventory.objects.count()
        book_fields_to_update_with = {
            'author': 'Superman',
            'title' : "A hero's life",
            'published_date': '2022-02-26'
        }
        response = self.client.patch(
            reverse('book_details', args=(self.book_id,) ),
            book_fields_to_update_with,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BookInventory.objects.count(),
            initial_book_count
        )

        for key in book_fields_to_update_with: 
            self.assertEqual( 
            response.data[key], 
            book_fields_to_update_with[key] )

    def test_replace_book(self): # PUT request
        initial_book_count = BookInventory.objects.count()
        new_book_fields_to_replace_with = {
            'author': 'Superman',
            'title' : "A hero's life",
            'number_of_pages' : 30,
            'published_date': '2022-02-26'
        }
        response = self.client.put(
            #f'/api/books/{self.book_id}/' or 
            # reverse('book_details', kwargs={'id': self.book_id}) or
            reverse('book_details', args=(self.book_id,) ),
            new_book_fields_to_replace_with,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            BookInventory.objects.count(),
            initial_book_count
        )

        for key in new_book_fields_to_replace_with: 
            self.assertEqual( 
            response.data[key], 
            new_book_fields_to_replace_with[key] )

    @tag('test_put_idempotency')
    def test_idempotency(self):
        NUMBER_OF_PUT_REQUESTS = 5 # some random number to make a put request
        for _ in range(NUMBER_OF_PUT_REQUESTS):
            self.test_replace_book()

    
class DeleteBook(APITestCase):
    '''
    Test DELETE request.
    
    DELETE should be idempotent, so its idempotency is tested.
    '''

    def setUp(self):
        book_fields = {
            'author': 'Author to delete',
            'title' : "A title to delete",
            'number_of_pages': -1,
            'published_date': '2022-02-26'
        }
        response = self.client.post(reverse('book_inventory'), book_fields, format='json')
        self.book_id = response.data['id']

    def test_delete_book(self):
        initial_book_count = BookInventory.objects.count()
        if initial_book_count != 0:
            response = self.client.delete( 
                reverse('book_details', args=(self.book_id,) )
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertRaises(
                BookInventory.DoesNotExist,
                BookInventory.objects.get, id=self.book_id)


    @tag('test_delete_idempotency')
    def test_idempotency(self):
        NUMBER_OF_DELETE_REQUESTS = 5 # some random number to test idempotency
        initial_book_count = BookInventory.objects.count()
        
        for _ in range(NUMBER_OF_DELETE_REQUESTS):
            self.test_delete_book()
        
        # check if a book is deleted (in case it existed)
        if initial_book_count != 0:
            self.assertEqual(
                BookInventory.objects.count(),
                initial_book_count - 1,
            )
        else: 
            # if no book existed before, delete should not change the state
            self.assertEqual(
                BookInventory.objects.count(),
                initial_book_count,
            )
