from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import ReadingListManage,ListIteamManage
from .models import ReadingList,ListItem

class ReadingListManageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            reading_lists = ReadingList.objects.filter(user=request.user).order_by('-created_at')
            serializer = ReadingListManage(reading_lists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data.copy()
            data['user'] = request.user.id 

            serializer = ReadingListManage(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Reading List Created"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def put(self, request, readinglist_id):
        try:
            readinglist = ReadingList.objects.get(id=readinglist_id, user=request.user)
            serializer = ReadingListManage(readinglist, data=request.data, partial=True)  

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Reading List Updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ReadingList.DoesNotExist:
            return Response({"error": "Reading List not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def delete(self, request, readinglist_id):
        try:
            readinglist = ReadingList.objects.get(id=readinglist_id, user=request.user)
            readinglist.delete()
            return Response({"message": "Reading List deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except ReadingList.DoesNotExist:
            return Response({"error": "Reading List not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
           
           
class ListIteamManageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, list_id):
        try:
            reading_list = ReadingList.objects.get(id=list_id, user=request.user)
            items = ListItem.objects.filter(list=reading_list).order_by('order')

            serializer = ListIteamManage(items, many=True)

            return Response({"list": reading_list.name, "items": serializer.data}, status=status.HTTP_200_OK)
        
        except ReadingList.DoesNotExist:
            return Response({"message": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def post(self, request):
        try:
            serializer = ListIteamManage(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Item added", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
        
    def put(self, request,listiteam_id):
        try:
            item = ListItem.objects.get(id=listiteam_id)
            serializer = ListIteamManage(instance=item, data=request.data, partial=True, context={'request': request})
        
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Item updated", "data": serializer.data}, status=200)
            else:
                return Response({"message": "Validation failed", "errors": serializer.errors}, status=400)

        except ReadingList.DoesNotExist:
            return Response({"message": "Reading list not found or unauthorized"}, status=404)
    
        except ListItem.DoesNotExist:
            return Response({"message": "Item not found in this list"}, status=404)
     
        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)}, status=500)
 
    
    
    def delete(self, request, listiteam_id):
        try:
            item = ListItem.objects.get(id=listiteam_id)
            if item.list.user != request.user:
                return Response({"message": "Unauthorized to delete this item"}, status=403)

            item.delete()
            return Response({"message": "Item deleted successfully"}, status=200)
    
        except ListItem.DoesNotExist:
            return Response({"message": "Item not found"}, status=404)
    
        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)}, status=500)

        
               