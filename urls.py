from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from postorius.views import list as list_views

urlpatterns = [
    url(r'^$', list_views.list_index),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^postorius/', include('postorius.urls')),
    url(r'^listinfo/', RedirectView.as_view(url='/', permanent=True)),
    url(r'', include('django_mailman3.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
