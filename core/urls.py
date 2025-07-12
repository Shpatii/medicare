from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_form, name='upload'),
    path("upload/submit/", views.upload_file, name="upload_file"),  # for POST: handle the file
    path('chatbot/', views.chatbot, name='chatbot'),

    path('pneumonia/', views.pneumonia_page, name='pneumonia_page'),
    path('pneumonia/detect/', views.upload_xray, name='detect_pneumonia'),
    path("skin-detect/", views.skin_classifier, name='classify_skin_image'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])