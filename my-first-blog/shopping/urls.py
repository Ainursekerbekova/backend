from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),

    path('accounts/', include('django.contrib.auth.urls')),

    path('register.html', include('blog.urls')),
    path('index.html', include('blog.urls')),
    path('wishlist.html', include('blog.urls')),
    path('cart.html', include('blog.urls')),
    path('checkout.html', include('blog.urls')),

]

if (settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


