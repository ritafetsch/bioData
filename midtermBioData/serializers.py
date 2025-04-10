from rest_framework import serializers
from .models import *

# all code in this file written personally but adapted from lecture content 
# except where otherwise noted in comments 

class PfamIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PfamID
        fields = ('domain_id', 'domain_description')

class DomainSerializer(serializers.ModelSerializer):
    # I wrote this code after looking up how to incorporiate other serializers
    pfam_id = PfamIDSerializer(read_only=True, source='pfamid')
    # End of code I wrote after looking up how to incorporiate other serializers
    class Meta:
        model = Domain
        fields = ('pfam_id', 'description', 'start', 'stop')

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ('taxa_id', 'genus', 'species')


class ProteinSerializer(serializers.ModelSerializer):
    # I wrote this code - required assitance from online documentation and 
    # forums to work through bugs 

    # define three fields for the in order to obtain related data from other 
    # tables. These will be included in the fields set at the bottom. Taxonomy 
    # and sequences are are populated but the following two functions 
    # get_taxonomy and get_sequence, domains obtains an instance of the 
    # DomainSerializer. 
    taxonomy = serializers.SerializerMethodField()
    sequences = serializers.SerializerMethodField()
    domains = DomainSerializer(many=True, read_only=True)

    def get_taxonomy(self, protein):
        return {
            'taxa_id': protein.taxa_id.taxa_id,
            'clade': protein.clade,
            'genus': protein.taxa_id.genus,
            'species': protein.taxa_id.species,
        }
    def get_sequences(self, protein):
        return list(protein.sequences.values_list('sequence', flat=True))
    # End of code I wrote this code - requiring assitance from online documentation and 
    # forums to work through bugs 

    class Meta:
        model = Protein
        fields = ('protein_id', 'sequences', 'taxonomy', 'length', 'domains')



class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields = ('id', 'protein_id', 'sequence')

