from rest_framework import serializers
from .models import Genre,Book,UserBookStatus

# class GenreCreatingSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model=Genre
#         fields=["id","name","genre_cover","description","is_active"]
#         read_only_fields = ['created_by']



class GenreCreatingSerilizer(serializers.ModelSerializer):
    genre_cover_url = serializers.SerializerMethodField()
    genre_cover = serializers.ImageField(required=False, write_only=True)  # Add this line

    class Meta:
        model = Genre
        fields = ["id", "name", "genre_cover", "genre_cover_url", "description", "is_active"]
        read_only_fields = ['created_by']

    def get_genre_cover_url(self, obj):
        request = self.context.get('request')
        if obj.genre_cover and request:
            return request.build_absolute_uri(obj.genre_cover.url)
        return None

class BookCreateSerilizer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.first_name', read_only=True)
    genre = serializers.CharField(source='genre.name')
    class Meta:
        model=Book
        fields="__all__"
        read_only_fields = ['author', 'created_at', 'updated_at',]



from rest_framework import serializers
from .models import UserBookStatus

class UserBookStatusSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author.first_name', read_only=True)  # Adjust if author is User or has different name field
    book_cover = serializers.ImageField(source='book.cover_image', read_only=True)

    class Meta:
        model = UserBookStatus
        fields = [
            'id', 'book', 'book_title', 'book_author', 'book_cover',
            'status', 'started_at', 'finished_at', 'rating', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


