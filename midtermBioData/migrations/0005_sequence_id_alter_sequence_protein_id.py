# Generated by Django 4.2.1 on 2023-07-01 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("midtermBioData", "0004_auto_20230701_1412"),
    ]

    operations = [
        migrations.AddField(
            model_name="sequence",
            name="id",
            field=models.AutoField(default=None, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="sequence",
            name="protein_id",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sequences",
                to="midtermBioData.protein",
            ),
        ),
    ]
