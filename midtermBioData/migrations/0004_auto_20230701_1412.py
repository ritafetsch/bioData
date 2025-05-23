# Generated by Django 4.2.1 on 2023-07-01 13:12

from django.db import migrations, models
# from midtermBioData.models import Protein, Sequence

def set_default_protein(apps, schema_editor):
    Sequence = apps.get_model('midtermBioData', 'Sequence')
    Protein = apps.get_model('midtermBioData', 'Protein')
    for sequence in Sequence.objects.all():
        protein = Protein.objects.filter(protein_id=sequence.protein_id).first()
        sequence.protein = protein
        sequence.save()

class Migration(migrations.Migration):

    dependencies = [
        ("midtermBioData", "0003_alter_protein_custom_pk"),
    ]

    operations = [migrations.RunPython(set_default_protein)]

    





