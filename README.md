# BookInventory
- A simple Django Rest API project with a simple front-end, drf backend,
  Swagger-ui &amp; ReDoc documentation and Docker support.  

## Non-API Pages (URLs):
- http://localhost:8000/ to see all the books listed. Then any of the books 
can be clicked on to see its details. This url is also the root page. To list
a book, firstly, books have to be created using [the API pages](#api-pages-(urls):).  

## API Pages (URLs):
- http://localhost:8000/api/schema/ to download the schema in yaml format.  
- http://localhost:8000/api/schema/swagger-ui/ to see a Swagger-UI formatted
documentation.  
- http://localhost:8000/api/schema/redoc/ to see a ReDoc formatted
  documentation.
- http://localhost:8000/api/books to see Django Rest Framework's autogenerated
documentation.
  
Note that, in the API documentation pages, documentations for GET, POST, PATCH,
PUT and DELETE requests for the BookInventory can be seen. Moreover, in 
Swagger-UI for example, making a query is quite easy with example formats.    

## Query Functionality:
- To filter the author names including 'tol' and book titles with 'peace' for
example, we can add our query appending a '?' to the root page and doing our 
queries like:  
    - http://localhost:8000?author=tol&title=peace

## To run in a Docker container:
- `docker-compose build`  
- `docker-compose up`  

## Keywords:
- Django
- Rest API
- Model View Template
- MVT
- drf
- drf-spectacular 
- Swagger-UI
- ReDoc
- Docker 
