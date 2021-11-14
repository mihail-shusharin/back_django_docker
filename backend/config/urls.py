from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from postman_task import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('images/<int:media_id>/resize/', views.ResizerView.as_view(), name='resize'),
    path('images/<int:media_id>/', views.DetailedView.as_view(), name='details'),
    path('images/', views.ImageView.as_view(), name='image')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("api/__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
