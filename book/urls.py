
from django.urls import path
from . import views

urlpatterns = [
    path('book/',views.BookCreateView.as_view(),name="book"),
    path('book/<int:book_id>/',views.BookCreateView.as_view(),name="edit-book"),
    path('genre/',views.CreateGenreView.as_view(), name='genre'),
    path('genre/<int:genre_id>/',views.CreateGenreView.as_view(), name='edit-genre'),
    
    path('book/read/<int:book_id>/',views.BookDetailView.as_view(),name="read-book"),
    path("books/", views.ListBooksView.as_view(), name="book-list"),
    path("genres/",views.ListGenreView.as_view(),name="all-genre"),

    path('shelf/', views.GetMyShelf.as_view(), name='get-my-shelf'),
    path('shelf/add/', views.AddToShelfAPIView.as_view(), name='add-to-shelf'),
    path('shelf/update/<int:book_id>/', views.UpdateShelfStatusAPIView.as_view(), name='update-shelf-status'),
    path('shelf/remove/<int:book_id>/', views.RemoveFromShelfAPIView.as_view(), name='remove-from-shelf'),
]

    
    
    

