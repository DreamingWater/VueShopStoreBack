# Generated by Django 3.2 on 2023-05-18 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230518_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifytoken',
            name='email_code_updated',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='verifytoken',
            name='img_code_updated',
            field=models.FloatField(default=0, null=True),
        ),
    ]
