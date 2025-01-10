from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ImageItem, PDFItem
from .serializers import (
    ImageItemSerializer,
    ImageRotateSerializer,
    PDFItemSerializer,
    PDFToImageSerializer,
    UploaderSerializer,
)


class UploaderView(APIView):
    serializer_class = UploaderSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = UploaderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PDFFilesView(viewsets.ModelViewSet):
    queryset = PDFItem.objects.all()
    serializer_class = PDFItemSerializer
    page_size = 10
    http_method_names = ["get", "delete"]


class ImageFilesView(viewsets.ModelViewSet):
    queryset = ImageItem.objects.all()
    serializer_class = ImageItemSerializer
    page_size = 10
    http_method_names = ["get", "delete"]


class ImageRotateView(APIView):
    serializer_class = ImageRotateSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ImageRotateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.save()
                content_type = f"image/{data["format"]}"
                return FileResponse(
                    data["rotated_image"],
                    as_attachment=True,
                    filename=data["file_name"],
                    content_type=content_type,
                )
            except Exception:
                return Response(
                    {"error": "Error while rotating image"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PDFToImageView(APIView):
    serializer_class = PDFToImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = PDFToImageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.save()
                content_type = f"image/{data['format']}"
                return FileResponse(
                    data["image"],
                    as_attachment=True,
                    filename=data["file_name"],
                    content_type=content_type,
                )
            except Exception:
                return Response(
                    {"error": "Error while converting PDF to image"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
