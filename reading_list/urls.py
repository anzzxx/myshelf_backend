from django.urls import path
from .views import ReadingListManageView,ListIteamManageView
urlpatterns=[
   path("view/",ReadingListManageView.as_view(),name="view-reading-list"),
   path("create/",ReadingListManageView.as_view(),name="create-reading-list"),
   path("edit/<int:readinglist_id>/",ReadingListManageView.as_view(),name="edit-reading-list"),
   path("delete/<int:readinglist_id>/",ReadingListManageView.as_view(),name="delete-reading-list"),
   
   path("list-item-create/",ListIteamManageView.as_view(),name="create-listiteam"),
   path("<int:list_id>/items/",ListIteamManageView.as_view(),name="list-all-iteams"),
   path("update_order/<int:listiteam_id>/",ListIteamManageView.as_view(),name="update-order"),
   path("remove iteam/<int:listiteam_id>/",ListIteamManageView.as_view(),name="delete iteam ")
   
]