from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include('documentation.urls')),
]

from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/docs/', permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
