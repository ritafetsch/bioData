from django.test import TestCase
from django.urls import reverse 
from django.urls import reverse_lazy 
from rest_framework.test import APIRequestFactory 
from rest_framework.test import APITestCase
from rest_framework import status 
from midtermBioData.model_factories import * 
from .serializers import *

# All API test functions personally written but inspired by 
# lecture content. Further advice found online regarding  
# what to test and reccomended methods for doing so 

# API tests
class APITests(APITestCase):
   
    def setUp(self):
        # create instance of protein data using protein factory for testing 
        self.protein = ProteinFactory()
        # create instance of domain data using domain factory for testing 
        self.domain = DomainFactory()
        # create instance of organism data using organsim factory for testing 
        self.organism = OrganismFactory()
        self.organism_id = self.organism.taxa_id
        self.protein_assign_taxa_id = ProteinFactory(taxa_id=self.organism)
        
    def test_get_protein_detail_not_found(self):
        # construct url for protein_detail passing in invaid protein
        url = reverse('protein_detail', args=['not-a-protein-id'])
        # send get request to django test client
        response = self.client.get(url)
        # make sure 404 response is returned for invalid data 
        self.assertEqual(response.status_code, 404)

    def test_get_domain(self):
        # construct url for get_domain passing pfam_id in as argument
        url = reverse('get_domain', args=[self.domain.pfam_id])
        response = self.client.get(url)
        # data is valid so check django test client returns status code of 200 
        self.assertEqual(response.status_code, 200)
        # ensure json response has domain_id key equal to domain.pfam_id
        self.assertEqual(response.json()['domain_id'], self.domain.pfam_id)

    def test_get_organism_proteins(self):
        # construct url for get_proteins passing organism_id in as argument
        url = reverse('get_proteins', args=[self.organism_id])
        # send get request to django test client
        response = self.client.get(url)
        # data is valid so check django test client returns status code of 200 
        self.assertEqual(response.status_code, 200)
        # check length of json response is one (that only one protein is returned)
        self.assertEqual(len(response.json()), 1)  

# End of API test functions personally written but inspired by 
# lecture content. Further advice found online regarding  
# what to test and reccomended methods for doing so 


# All serialization tests personally written but inspired by 
# lecture content. Further advice found online regarding  
# what to test and reccomended methods for doing so 

# serialization tests 
class SerializerTests(APITestCase):
    # variables originally set to None for use in 
    protein = None
    proteinSerializer = None 
    organism = None
    organismSerializer = None
    domain = None
    domainSerializer = None
    sequence = None
    sequenceSerializer = None

    # setup for testing - instances of different factories and respective serializers  
    def setUp(self):
        self.organism = OrganismFactory.create()
        self.organismSerializer = OrganismSerializer(instance=self.organism)
        self.protein = ProteinFactory(protein_id="protein1", taxa_id=self.organism)
        self.proteinSerializer = ProteinSerializer(instance=self.protein)
        self.domain = DomainFactory.create()
        self.domainSerializer = DomainSerializer(instance=self.domain)
        self.sequence = SequenceFactory.create()
        self.sequenceSerializer = SequenceSerializer(instance=self.sequence)

    def test_protein_serializer(self):
        data = self.proteinSerializer.data
        # check set of keys matches what protein model expects
        self.assertEqual(set(data.keys()), set(['protein_id', 'sequences', 'taxonomy', 'length', 'domains']))
  
    def test_protein_serializer_valid(self):
        # create instance of protein serializer and pass in dummy data as dict
        serializer = ProteinSerializer(data={'protein_id': 'protein', 'sequences': ['ABCDEF'], 'taxonomy': '123', 'length': 200, 'domains': ['Domain']})
        # check that serializer instance of data is valid 
        self.assertTrue(serializer.is_valid())
        
    def test_protein_serializer_invalid(self):
        # create instance of protein serializer and pass in dummy data as dict
        serializer = ProteinSerializer(data={'protein_id': '', 'sequences': ['ABCDEF'], 'taxonomy': '123', 'length': 200, 'domains': ['Domain']})
        # check if serializer fails validation based on invalid key 
        self.assertFalse(serializer.is_valid())
        # check if validation error correponds to key where error is expected (protein_id)
        self.assertEqual(set(serializer.errors.keys()), set(['protein_id']))

    def test_protein_serializer_update(self):
        # create instance of protein serializer and pass in dummy data as dict
        serializer = ProteinSerializer(instance=self.protein, data={'protein_id': 'updated_protein', 'sequences': ['ABCDEF'], 'taxonomy': '123', 'length': 200, 'domains': ['Domain']})
        # check serializer passes validation
        self.assertTrue(serializer.is_valid())
        # update existing protein instance with new data from above
        updated_instance = serializer.save()
        # check if protein_id of updated instance matches value before updated ('updated_protein')
        self.assertEqual(updated_instance.protein_id, 'updated_protein')
        
    def test_organism_serializer(self):
        # get serialized representation of organism data
        data = self.organismSerializer.data
        # check serialized fields match instances of data prior to serialization
        self.assertEqual(data['genus'], self.organism.genus)
        self.assertEqual(data['species'], self.organism.species)
        self.assertEqual(data['taxa_id'], self.organism.taxa_id)  

    def test_domain_serializer_valid(self):
        # create instance of domain serializer and pass in dummy data as dict
        serializer = DomainSerializer(data={'name': 'Domain1', 'start': 10, 'stop': 20, 'pfam_id': 'PF123', 'description': 'Test domain'})
        # check serializer passes validation
        self.assertTrue(serializer.is_valid())

    def test_sequence_serializer_invalid(self):
        # create instance of domain serializer and pass in dummy data as dict
        serializer = SequenceSerializer(data={'sequence': '', 'description': 'DNA Sequence'})
        # ensure serializer is not valid given missing data
        self.assertFalse(serializer.is_valid())
        # ensure source of error comes from missing sequence data
        self.assertEqual(set(serializer.errors.keys()), set(['sequence']))
    
    def test_sequence_serializer(self):
        # get serialized representation of sequence data
        data = self.sequenceSerializer.data
        # check serialized data contains expected keys
        self.assertEqual(set(data.keys()), set(['id', 'protein_id', 'sequence']))
        # check id key in serializer matches id atribute of serialized object 
        self.assertEqual(data['id'], self.sequence.id)
        # check sequence key in serializer matches sequence atribute of serialized object  
        self.assertEqual(data['sequence'], self.sequence.sequence)

# End of serialization tests personally written but inspired by 
# lecture content. Further advice found online regarding  
# what to test and reccomended methods for doing so 


# Series of tests to check integrity of models. This code was written and adapted
# personally but with online guidance regarding what aspects of the models can 
# and should be tested

# test models - no comments as test names are informative and tests are simple
class ModelTests(TestCase):
    def test_create_protein(self):
        protein = ProteinFactory.create()
        self.assertIsInstance(protein, Protein)
        self.assertIsNotNone(protein.pk)

    def test_update_protein(self):
        protein = ProteinFactory.create()
        updated_length = 150
        protein.length = updated_length
        protein.save()
        updated_protein = Protein.objects.get(pk=protein.pk)
        self.assertEqual(updated_protein.length, updated_length)

    def test_delete_protein(self):
        protein = ProteinFactory.create()
        protein.delete()
        self.assertFalse(Protein.objects.filter(pk=protein.pk).exists())

    def test_get_protein_by_id(self):
        protein = ProteinFactory.create(protein_id='A123456')
        retrieved_protein = Protein.objects.get(protein_id='A123456')
        self.assertEqual(retrieved_protein, protein)

    def test_get_all_proteins(self):
        ProteinFactory.create_batch(4)
        proteins = Protein.objects.all()
        self.assertEqual(proteins.count(), 4)

    def test_create_organism(self):
        organism = OrganismFactory.create()
        self.assertIsInstance(organism, Organism)
        self.assertIsNotNone(organism.pk)

    def test_update_organism(self):
        organism = OrganismFactory.create()
        new_species = 'abc'
        organism.species = new_species
        organism.save()
        updated_organism = Organism.objects.get(pk=organism.pk)
        self.assertEqual(updated_organism.species, new_species)

    def test_delete_organism(self):
        organism = OrganismFactory.create()
        organism.delete()
        self.assertFalse(Organism.objects.filter(pk=organism.pk).exists())

    def test_get_organism_by_genus_name(self):
        organism = OrganismFactory.create(genus='abc', species='abcdef')
        get_organism = Organism.objects.get(genus='abc')
        self.assertEqual(get_organism, organism)

    def test_get_all_organisms(self):
        OrganismFactory.create_batch(3)
        organisms = Organism.objects.all()
        self.assertEqual(organisms.count(), 3)

    def test_create_domain(self):
        domain = DomainFactory.create()
        self.assertIsInstance(domain, Domain)
        self.assertIsNotNone(domain.pk)

    def test_update_domain(self):
        domain = DomainFactory.create()
        updated_description = 'some-description'
        domain.description = updated_description
        domain.save()
        updated_domain = Domain.objects.get(pk=domain.pk)
        self.assertEqual(updated_domain.description, updated_description)
# 
    def test_delete_domain(self):
        domain = DomainFactory.create()
        domain.delete()
        self.assertFalse(Domain.objects.filter(pk=domain.pk).exists())

    def test_get_domain_by_name(self):
        domain = DomainFactory.create(description='domain123')
        retrieved_domain = Domain.objects.get(description='domain123')
        self.assertEqual(retrieved_domain, domain)

    def test_get_all_domains(self):
        DomainFactory.create_batch(4)
        domains = Domain.objects.all()
        self.assertEqual(domains.count(), 4)

    def test_create_PfamID(self):
        pfam_id = PfamIDFactory.create()
        self.assertIsInstance(pfam_id, PfamID)
        self.assertIsNotNone(pfam_id.pk)

    def test_delete_PfamID(self):
        pfam_id = PfamIDFactory.create()
        pfam_id.delete()
        self.assertFalse(PfamID.objects.filter(pk=pfam_id.pk).exists())

    def test_get_all_PfamIDs(self):
        PfamIDFactory.create_batch(4)
        pfam_ids = PfamID.objects.all()
        self.assertEqual(pfam_ids.count(), 4)

# End of series of tests checking integrity of models. This code was written and adapted
# personally but with online guidance regarding what aspects of the models can 
# and should be tested
