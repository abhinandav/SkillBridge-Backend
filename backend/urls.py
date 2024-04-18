from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from chat.consumers import ChatConsumer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include("User.api.urls")),
    path('adminapp/', include("Adminapp.urls")),
    path('teacher/', include("TeacherApp.urls")),
    path('student/', include("StudentApp.urls")),
    path('chat/', include("chat.urls")),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



