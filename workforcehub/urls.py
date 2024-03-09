
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('employees.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

""" 
# Error handling (middleware is in use at the moment for testing and logging purposes)
# uncomment the following lines to use the error handling views
handler404 = 'employees.views.error_404'
handler500 = 'employees.views.error_500'
handler403 = 'employees.views.error_403'
"""

