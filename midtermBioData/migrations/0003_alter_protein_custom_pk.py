# Generated by Django 4.2.1 on 2023-07-01 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("midtermBioData", "0002_alter_protein_custom_pk"),
    ]

    operations = [
        migrations.AlterField(
            model_name="protein",
            name="custom_pk",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
