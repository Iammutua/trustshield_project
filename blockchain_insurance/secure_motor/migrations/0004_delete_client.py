# Generated by Django 4.2.7 on 2023-12-27 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_motor', '0003_rename_username_client_first_name_client_last_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Client',
        ),
    ]
