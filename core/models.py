import os

import pypdf
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from PIL import Image


def upload_file_to(instance, filename):
    cur_date = timezone.now()
    return f"{"pdfs" if isinstance(instance, PDFItem)  else "images"}/{cur_date.year}/{cur_date.month}/{cur_date.day}/{filename}"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.item:
            self.file_name = os.path.basename(self.item.name)
            self.file_size = self.item.size
        super().save(*args, **kwargs)


class PDFItem(BaseModel):
    item = models.FileField(
        upload_to=upload_file_to,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    number_of_pages = models.PositiveIntegerField(blank=True, null=True)
    page_width = models.FloatField(blank=True, null=True)
    page_height = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "PDF"
        verbose_name_plural = "PDFs"

    def initialize_pdf_info(self):
        try:
            with self.item.open("rb") as f:
                pdf_reader = pypdf.PdfReader(f)
                self.number_of_pages = len(pdf_reader.pages)

                if self.number_of_pages > 0:
                    first_page = pdf_reader.pages[0]
                    self.page_width = float(first_page.mediabox.width)
                    self.page_height = float(first_page.mediabox.height)

        except Exception as e:
            raise ValidationError(f"Error processing PDF: {str(e)}")

    def save(self, *args, **kwargs):
        is_added = self.pk is None
        if is_added and self.item:
            self.initialize_pdf_info()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name or "Unnamed PDF"


class ImageItem(BaseModel):
    item = models.ImageField(upload_to=upload_file_to)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    number_of_channels = models.PositiveIntegerField(blank=True, null=True)
    format = models.CharField(max_length=10, blank=True)
    color_mode = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def initialize_image_info(self):
        try:
            with self.item.open("rb") as f:
                image = Image.open(f)
                self.width = image.width
                self.height = image.height
                self.color_mode = image.mode
                self.format = image.format
                if image.mode == "RGB":
                    self.number_of_channels = 3
                elif image.mode == "RGBA":
                    self.number_of_channels = 4
                elif image.mode == "L":
                    self.number_of_channels = 1
                else:
                    self.number_of_channels = len(image.getbands())

        except Exception as e:
            raise ValidationError(f"Error processing image: {str(e)}")

    def save(self, *args, **kwargs):
        is_added = self.pk is None
        if is_added and self.item:
            self.initialize_image_info()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name or "Unnamed Image"
