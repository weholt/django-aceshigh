# Generated by Django 5.0.6 on 2024-06-05 17:46

import aceshigh.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="yourmodel",
            name="code",
            field=aceshigh.fields.AceEditorField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="yourmodel",
            name="description",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="yourmodel",
            name="name",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
