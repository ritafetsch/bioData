
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import * 
from .serializers import * 


# I wrote this code myself guided by lecture material and online support 
@api_view(['GET'])
def protein_detail(request, protein_id): 
    try: 
        # query for all protein objects with protein_id of incoming protein_id
        proteins = Protein.objects.filter(protein_id=protein_id)
        # get first protein
        protein = proteins.first()
        # store protein serializer in variable 
        serializer = ProteinSerializer(protein)
        # store all response data in a python dictionary, 
        # extracting the necessary components from the serializer
        response = {
            'protein_id': serializer.data['protein_id'],
            'sequences': serializer.data['sequences'],
            'taxonomy': serializer.data['taxonomy'],
            'length': serializer.data['length'],
            'domains': serializer.data['domains']
        }
        # if successful query and protein data retrieved, return json reponse with the data
        return JsonResponse(response, json_dumps_params={'indent': 4})
    except:
        # Else return a 404 http response 
        return HttpResponse(status=404)
    # End of code I wrote this code myself guided by lecture material and online support 

# I wrote this code myself guided by lecture material and online support 
@api_view(['GET'])
def get_domain(request, pfam_id):
    try:
        # get all domain objects currently in database based on incoming pfam_id
        domain = Domain.objects.get(pfam_id=pfam_id)
        # get reponse data based on domain objects returned 
        response = {
            'domain_id': domain.pfam_id,
            'domain_description': domain.description,
        }
         # if successful query and domain data retrieved, return json reponse with the data
        return JsonResponse(response, json_dumps_params={'indent': 4})
    except:
        # Else return a 404 http response 
        return HttpResponse(status=404)
# End of code I wrote this code myself guided by lecture material and online support 
    
# I wrote this code myself guided by lecture material and online support 
@api_view(['GET']) 
def get_organism_proteins(request, taxa_id):
    try:
        # get all protein objects currently in database filtered by incoming taxa_id
        proteins = Protein.objects.filter(taxa_id=taxa_id)
        # get reponse data based on objects returned
        response = [
            {'id': protein.custom_pk, 
             'protein_id': protein.protein_id}
            #  get id and protein_id iterating through all proteins that have been returned as 
            # one protein can belong to many domains
            for protein in proteins
        ]
        # if successful query and domain data retrieved, return json reponse with the data
        return JsonResponse(response, safe=False, json_dumps_params={'indent': 4})
    # Else if protein doens't exist return a 404 http response 
    except Protein.DoesNotExist:
        return HttpResponse(status=404)
# End of code I wrote this code myself guided by lecture material and online support 

# I wrote this code myself guided by lecture material and online support 
@api_view(['GET'])
def get_pfams(request, taxa_id):
    try:
        # get all protein and domain objects currently in database filtered by incoming taxa_id
        proteins = Protein.objects.filter(taxa_id=taxa_id)
        domains = Domain.objects.filter(protein_id__in=proteins)
        # get reponse data based on objects returned
        response = [
            {
                'id': domain.id,
                'pfam_id': {
                    'domain_id': domain.pfam_id,
                    'domain_description': domain.description,
                }
            }
            # iterate over domains as there can be many to a given protein
            for domain in domains
        ]
        # if successful query and domain data retrieved, return json reponse with the data
        return JsonResponse(response, safe=False, json_dumps_params={'indent': 4})
    # Else if protein doens't exist return a 404 http response 
    except Protein.DoesNotExist or Domain.DoesNotExist:
        return HttpResponse(status=404)
# End of code I wrote this code myself guided by lecture material and online support 

# I wrote this code myself guided by lecture material and online support 
@api_view(['GET'])
def get_coverage(request, protein_id):
    try:
        proteins = Protein.objects.filter(protein_id=protein_id)
    
        total_coverage = 0
        total_proteins = 0
        # iterate over each protein with the incoming protein id
        for protein in proteins:
            # for each protein with given protein_id, get all associated domains
            domains = Domain.objects.filter(protein_id=protein)
            protein_length = protein.length
            accumulated_domain_length = 0
            for domain in domains:
                # calcualte accumulated domain length by adding differences between start and stop for each one
                accumulated_domain_length += domain.stop - domain.start + 1
            # get coverage in each loop by dividing accumulated domain length by the length of the protein
            coverage = accumulated_domain_length / protein_length
            total_coverage += coverage
            total_proteins += 1
        # after iterating through all proteins, average coverage is calculated by dividing total accumulated 
        # coverage by the total number of proteins (both of which have been calculated in each loop just above)
        average_coverage = total_coverage / total_proteins
        # store average coverage calculated in response data to pass in 
        response = {
            'coverage': average_coverage
        }
        # if successful query and domain data retrieved, return json reponse with the data
        return JsonResponse(response, json_dumps_params={'indent': 4})
    # Else if protein doesn't exist return a 404 http response 
    except Protein.DoesNotExist:
        return HttpResponse(status=404)
# End of code I wrote this code myself guided by lecture material and online support 

