from django.shortcuts import render
from .models import *
from .forms import ProteinForm
from django.http import HttpResponseRedirect
from django.contrib import messages

# I wrote this code guided by lecture material 
# home page view - renders index.html passing all proteins in as context data
def index(request): 
    proteins = Protein.objects.all()
    return render(request, 'midtermBioData/index.html', {'proteins':proteins})
# End of code I wrote guided by lecture material 

# proteins page view - renders proteins.html passing in all proteins currently in database 
# and protein form for posting data
def proteins(request):

# I wrote this code guided structurally by lecture material
    proteins = Protein.objects.all()
    if request.method == 'POST': 
        # initilaize protein form 
        form = ProteinForm(request.POST)
        # If form data is validly entered, get cleaned data 
        if form.is_valid():
            # initialize protein object for database
            protein = Protein()
            # get all fields from form
            protein.protein_id = form.cleaned_data['protein_id']
            protein.clade = form.cleaned_data['clade']
            protein.length = form.cleaned_data['length']
            protein.pfam_id = form.cleaned_data['pfam_id']
            protein.taxa_id = form.cleaned_data['taxa_id']
            # save protein object to database 
            protein.save() 
            messages.success(request, 'Protein added successfully.')
            return HttpResponseRedirect('/proteins/')
    # else if method is not post, display form
    else:
        form = ProteinForm() 
        return render(request, 'midtermBioData/proteins.html', {'proteins':proteins, 'form':form})
# End of code I wrote guided structurally by lecture material


# protein page view - renders protein.html - displays details of protein that has been clicked on
def protein(request, protein_id):
    # try retrieving all protein data based on protein clicked on from proteins page 
    try: 
        # I wrote all queries but required online help from documentation with bugs
        proteins = Protein.objects.filter(protein_id=protein_id)
        sequence = Sequence.objects.get(protein_id__in=proteins)   
        organism = Organism.objects.get(taxa_id=proteins.first().taxa_id.taxa_id)
        domains = Domain.objects.filter(protein_id__in=proteins).distinct()
        pfam_ids = PfamID.objects.filter(domain_id__pfam_id__in=domains.values('pfam_id'))

        first_protein = proteins.first()
        # End of queries code I wrote requiring online help from documentation with bugs
    
    # except if protein does not exist 
    except Protein.DoesNotExist:
        pass
    # render protein page with context data for displaying proteins
    return render(request, 'midtermBioData/protein.html', {'pfam_ids': pfam_ids, 'first_protein': first_protein,'organism': organism, 'proteins':proteins,  'sequence': sequence, 'domains': domains})
   
    
   