import base64
import os
from io import BytesIO

import magic
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from pdf2image import convert_from_bytes
from PIL import Image
from rest_framework import serializers

from . import constants
from .models import ImageItem, PDFItem


class PDFItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFItem
        fields = "__all__"


class ImageItemSerializer(serializers.ModelSerializer):
    angel = serializers.FloatField(required=False, default=0, write_only=True)

    class Meta:
        model = ImageItem
        fields = "__all__"


class UploaderSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, write_only=True)

    def validate_file(self, file):
        if file.content_type != "text/plain":
            raise ValidationError("only text files with base64 content are allowed")
        if file.size > constants.MAX_FILE_SIZE:
            raise ValidationError("File size should not exceed 10MB for testing reason")

        try:
            file_content = file.read().decode("utf-8").strip()
            decoded_file = base64.b64decode(file_content)
            file_type = magic.from_buffer(decoded_file, mime=True)
            if file_type not in constants.SUPPORTED_FILE_TYPES:
                raise ValidationError(
                    f"Unsupported file type {file_type}. {', '.join(constants.SUPPORTED_FILE_TYPES.keys())} files are supported."
                )

            return {
                "content": decoded_file,
                "mime_type": file_type,
                "extension": constants.SUPPORTED_FILE_TYPES[file_type],
                "file_name": file.name,
            }

        except base64.binascii.Error:
            raise ValidationError("Invalid base64 content")
        except Exception as e:
            raise ValidationError(f"Error processing file: {str(e)}")

    def create(self, validated_data):
        data = validated_data["file"]

        original_file_name = os.path.splitext(data["file_name"])[0]
        new_file_name = f"{original_file_name}{data['extension']}"
        file_type = data["mime_type"]
        decoded_file = ContentFile(data["content"], name=new_file_name)

        item = None
        if file_type == "application/pdf":
            item = PDFItem.objects.create(item=decoded_file)
            return PDFItemSerializer(instance=item).data

        else:
            item = ImageItem.objects.create(item=decoded_file)
            return ImageItemSerializer(instance=item).data


class ImageRotateSerializer(serializers.Serializer):
    image_id = serializers.PrimaryKeyRelatedField(
        queryset=ImageItem.objects.all(), write_only=True
    )

    angel = serializers.FloatField(required=False, default=0, write_only=True)

    def validate_angel(self, value):
        return value % 360

    def create(self, validated_data):
        item = validated_data["image_id"]
        angel = validated_data["angel"]

        with Image.open(item.item.path) as image:
            rotated_image = image.copy()
            rotated_image = rotated_image.rotate(angel, expand=True)

            buffer = BytesIO()
            format = image.format or "PNG"
            rotated_image.save(buffer, format=format)
            buffer.seek(0)

        return {
            "file_name": f"rotated_{angel}_degrees_{item.file_name}",
            "rotated_image": buffer,
            "format": format.lower(),
        }


class PDFToImageSerializer(serializers.Serializer):
    pdf_id = serializers.PrimaryKeyRelatedField(
        queryset=PDFItem.objects.all(), write_only=True
    )

    def create(self, validated_data):
        item = validated_data["pdf_id"]
        with item.item.open("rb") as f:
            images = convert_from_bytes(f.read(), fmt="png")
            image = images[0]
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

        return {
            "image": buffer,
            "file_name": f"{item.file_name}.png",
            "format": "png",
        }
