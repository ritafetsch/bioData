from django.urls import include, path
from . import views
from . import api 

# I wrote this code with guidance of lecture videos 
urlpatterns = [
    # main view urls
    path('', views.index, name='index'),
    path('proteins/', views.proteins, name='proteins'),
    path('protein/<str:protein_id>', views.protein, name='protein'),

    # api urls  
    path('api/protein/<str:protein_id>', api.protein_detail, name='protein_detail'),
    path('api/pfam/<str:pfam_id>', api.get_domain, name='get_domain'),
    path('api/proteins/<int:taxa_id>', api.get_organism_proteins, name='get_proteins'),
    path('api/pfams/<int:taxa_id>', api.get_pfams, name='get_pfams'),
    path('api/coverage/<str:protein_id>', api.get_coverage, name='get_coverage'), 
]
# End of code I wrote this code with guidance of lecture videos 


