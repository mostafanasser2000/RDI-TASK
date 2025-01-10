# Generated by Django 5.1.4 on 2025-01-10 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageitem',
            name='size',
        ),
        migrations.AddField(
            model_name='imageitem',
            name='color_mode',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='imageitem',
            name='file_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='imageitem',
            name='file_size',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='imageitem',
            name='format',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='pdfitem',
            name='file_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='pdfitem',
            name='file_size',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='number_of_channels',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='width',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdfitem',
            name='number_of_pages',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdfitem',
            name='page_height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdfitem',
            name='page_width',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
