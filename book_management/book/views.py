from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import GenreCreatingSerilizer,BookCreateSerilizer,UserBookStatusSerializer
from .models import Genre,Book,UserBookStatus

class CreateGenreView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=GenreCreatingSerilizer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message":"Genre created","data":serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    # def get(self, request):
    #     user = request.user
    #     genres = Genre.objects.filter(created_by=user)
    #     serializer = GenreCreatingSerilizer(genres, many=True)
    #     return Response({"message":"genre fetched!","data":serializer.data},status=status.HTTP_200_OK)
    def get(self, request):
        user = request.user
        genres = Genre.objects.filter(created_by=user,is_active=True)
        serializer = GenreCreatingSerilizer(genres, many=True, context={"request": request})
        return Response({"message": "genre fetched!", "data": serializer.data}, status=status.HTTP_200_OK)

    
    
    def put(self, request, genre_id):
        try:
            user = request.user
            genre = Genre.objects.get(id=genre_id)

            if genre.created_by != user:
                return Response({"error": "You do not have permission to update this genre."},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = GenreCreatingSerilizer(genre, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Genre updated!", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Genre.DoesNotExist:
            return Response({"error": "Genre not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, genre_id):
        try:
            genre = Genre.objects.get(id=genre_id)

            if genre.created_by != request.user:
                return Response({"error": "You do not have permission to delete this genre."},
                                status=status.HTTP_403_FORBIDDEN)

            genre.is_active = False  # Soft delete
            genre.save()

            return Response({"message": "Genre deleted successfully (soft delete)."},
                            status=status.HTTP_200_OK)

        except Genre.DoesNotExist:
            return Response({"error": "Genre not found."},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class BookCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        serializer=BookCreateSerilizer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=user)
            
            return Response({"message":"book creted!","data":serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        user = request.user
        try:
            books = Book.objects.filter(author=user,is_active=True)
            serializer = BookCreateSerilizer(books, many=True)
            return Response({"message": "Books fetched!", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def put(self, request, book_id):
        try:
            user = request.user
            book = Book.objects.get(id=book_id)

            # Check if the logged-in user is the author of the book
            if book.author != user:
                return Response({"error": "You do not have permission to update this book."},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = BookCreateSerilizer(book, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Book updated successfully.", "data": serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)

            if book.author != request.user:
                return Response({"error": "You do not have permission to delete this genre."},
                                status=status.HTTP_403_FORBIDDEN)

            book.is_active = False  # Soft delete
            book.save()

            return Response({"message": "Book deleted successfully (soft delete)."},
                            status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response({"error": "Book not found."},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
        
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ListBooksView(ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = BookCreateSerilizer
    pagination_class = StandardResultsSetPagination
    queryset = Book.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['genre', 'author'] 
                 
class ListGenreView(ListAPIView):
    serializer_class = GenreCreatingSerilizer
    pagination_class = StandardResultsSetPagination
    queryset = Genre.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'created_by'] 
    


class AddToShelfAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserBookStatusSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.validated_data['book']
            user = request.user

            if UserBookStatus.objects.filter(user=user, book=book).exists():
                return Response({"error": "This book is already on your shelf."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateShelfStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, book_id):
        try:
            entry = UserBookStatus.objects.get(user=request.user, book__id=book_id)
        except UserBookStatus.DoesNotExist:
            return Response({"error": "Book not found in your shelf."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserBookStatusSerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveFromShelfAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_id):
        try:
            entry = UserBookStatus.objects.get(user=request.user, book__id=book_id)
            entry.delete()
            return Response({"message": "Book removed from your shelf."}, status=status.HTTP_204_NO_CONTENT)
        except UserBookStatus.DoesNotExist:
            return Response({"error": "Book not found in your shelf."}, status=status.HTTP_404_NOT_FOUND)


class GetMyShelf(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            my_shelf = UserBookStatus.objects.filter(user=request.user)
            serializer = UserBookStatusSerializer(my_shelf, many=True)
            return Response({
                "message": "Shelf fetched successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Failed to fetch shelf.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BookDetailView(APIView):
    permission_classes=[AllowAny]
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookCreateSerilizer(instance=book)
            return Response({"message": "Book fetched!", "data": serializer.data}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)