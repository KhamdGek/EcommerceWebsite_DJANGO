# Generated by Django 3.0.7 on 2020-12-30 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_auto_20201230_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]
