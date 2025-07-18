
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings    
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",include("accounts.urls")),
    path("api/store/",include("book.urls")),
    path('api/readinglist/',include("reading_list.urls"))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)