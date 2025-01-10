from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("pdfs", views.PDFFilesView, basename="pdf")
router.register("images", views.ImageFilesView, basename="image")

urlpatterns = [
    path("", include(router.urls)),
    path("upload/", views.UploaderView.as_view(), name="upload"),
    path("rotate/", views.ImageRotateView.as_view(), name="rotate"),
    path("convert-pdf-to-image/", views.PDFToImageView.as_view(), name="pdf-to-image"),
]
