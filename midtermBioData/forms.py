from django import forms 
from .models import *

# I wrote this code guided by lecture material
class ProteinForm(forms.ModelForm): 
     class Meta:
        model = Protein
        fields = ['protein_id', 'clade', 'length', 'pfam_id', 'taxa_id']
# End of code I wrote this code guided by lecture material
 