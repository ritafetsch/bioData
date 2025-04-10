import factory
import factory.fuzzy
from django.test import TestCase
from django.conf import settings 
from django.core.files import File
from .models import * 

# I wrote all factory models but guided by lecture content (following
# inspiration to make the tests more sophisitcated by generating different 
# values for the data)
class DomainFactory(factory.django.DjangoModelFactory):
    pfam_id = 'PF123'
    description = factory.Faker('word')
    start = factory.fuzzy.FuzzyInteger(50, 500)
    stop = factory.fuzzy.FuzzyInteger(50, 500)
    class Meta:
        model = Domain

class PfamIDFactory(factory.django.DjangoModelFactory):
    domain_id = factory.SubFactory(DomainFactory)
    domain_description = factory.Faker('word')
    class Meta: 
        model = PfamID

class OrganismFactory(factory.django.DjangoModelFactory):
    taxa_id = factory.Sequence(lambda n: n)
    genus = factory.Faker('word')
    species = factory.Faker('word')
    class Meta:
        model = Organism

class ProteinFactory(factory.django.DjangoModelFactory):
    custom_pk = factory.Sequence(lambda n: n)
    protein_id = factory.Faker('uuid4')
    clade = factory.Faker('word')
    length = factory.fuzzy.FuzzyInteger(50, 500)
    pfam_id = factory.Faker('word')
    taxa_id = factory.SubFactory(OrganismFactory)
    class Meta:
        model = Protein

class SequenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sequence
    id = factory.Sequence(lambda n: n)
    protein_id = factory.SubFactory(ProteinFactory)
    sequence = factory.Sequence(lambda n: f"AATTCCGG{n}")
# End of code I wrote for all factory models (again, guided by lecture content (following
# inspiration to make the tests more sophisitcated by generating different 
# values for the data)