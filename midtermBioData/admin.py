from django.contrib import admin
from .models import * 

# Code guided by lecture videos - adapted for own purposes 
class OrganismAdmin(admin.ModelAdmin):
    list_display = ('taxa_id','genus','species')
admin.site.register(Organism, OrganismAdmin)

class ProteinAdmin(admin.ModelAdmin):
    list_display = ('protein_id','clade','length', 'pfam_id')
admin.site.register(Protein, ProteinAdmin)

class DomainAdmin(admin.ModelAdmin):
    list_display = ('pfam_id','start','stop','description')
admin.site.register(Domain, DomainAdmin)

class SequenceAdmin(admin.ModelAdmin):
    list_display = ('protein_id','sequence')
admin.site.register(Sequence, SequenceAdmin)

class PfamIDAdmin(admin.ModelAdmin):
    list_display = ('domain_id','domain_description')
admin.site.register(PfamID, PfamIDAdmin)
# End of code guided by lecture videos - adapted for own purposes 
