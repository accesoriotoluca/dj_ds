# Generated by Django 4.2 on 2023-04-23 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_alter_blank_test_2_created_test_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blank_test_2',
            name='total_price_test_2',
            field=models.FloatField(blank=True, null=True),
        ),
    ]