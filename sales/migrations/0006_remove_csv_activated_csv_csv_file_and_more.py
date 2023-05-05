# Generated by Django 4.2 on 2023-05-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_delete_blank_test_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csv',
            name='activated',
        ),
        migrations.AddField(
            model_name='csv',
            name='csv_file',
            field=models.FileField(null=True, upload_to='csvs'),
        ),
        migrations.AlterField(
            model_name='csv',
            name='file_name',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
