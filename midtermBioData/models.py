from django.db import models

# I wrote this code 
class Organism(models.Model):
    taxa_id = models.IntegerField(primary_key=True) 
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100)

    def __str__(self):
        return str(self.taxa_id)

class Protein(models.Model):
    custom_pk = models.AutoField(primary_key=True)
    protein_id = models.CharField(max_length=100)
    clade = models.CharField(max_length=100)
    length = models.IntegerField()
    pfam_id = models.CharField(max_length=100)
    taxa_id = models.ForeignKey(Organism, on_delete=models.CASCADE)

    def __str__(self):
        return self.protein_id
    
class Domain(models.Model):
    pfam_id = models.CharField(max_length=100)
    protein_id = models.ManyToManyField(Protein, related_name='domains')
    description = models.CharField(max_length=100)
    start = models.IntegerField()
    stop = models.IntegerField()

    def __str__(self):
        return self.pfam_id
    
class PfamID(models.Model):
    domain_id = models.OneToOneField(Domain, on_delete=models.CASCADE, primary_key=True)
    domain_description = models.CharField(max_length=100)

    def __str__(self):
        return self.domain_description
        
class Sequence(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='sequences', null=True, default=None)
    sequence = models.CharField(max_length=600)

    def __str__(self):
        return f"Sequence for {self.protein_id}"
    


# End of code I wrote 


