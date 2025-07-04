from rest_framework import serializers
from .models import ReadingList,ListItem

class ReadingListManage(serializers.ModelSerializer):
    class Meta:
        model=ReadingList
        fields="__all__"
        read_only_fields = ['created_at', 'updated_at']
        
class ListIteamManage(serializers.ModelSerializer):
    class Meta:
        model=ListItem
        fields="__all__"
        read_only_fields = ['created_at', 'updated_at']