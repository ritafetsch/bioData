import os
import sys
import django
import pandas as pd

# I wrote this code guided by lecture material where script is written for populating data

# Add the parent directory to the Python path
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(parent_dir)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midtermProject.settings')

# Initialize Django
django.setup()
# I wrote code I wrote guided by lecture material where script is written for populating data 

from midtermBioData.models import Organism, Protein, Sequence, Domain, PfamID

# I wrote all of the following code for loading in the data. Support was found online for fixing bugs in the code 
def delete_current_data():
    Domain.objects.all().delete()
    Organism.objects.all().delete()
    Protein.objects.all().delete()
    Sequence.objects.all().delete()
    PfamID.objects.all().delete()

# function for loading all code from csv files after data has been deleted 
def load_data():
    # execute above function for deleting any data currently in the database
    delete_current_data()

    
    current_dir = os.path.dirname(__file__)
    # Construct the path to the CSV files directory
    csv_dir = os.path.join(current_dir, '..', '..', 'csv_data_files')




    # Load data from Organism.csv using pandas
    organism_csv_file_path = os.path.join(csv_dir, 'Organism.csv')
    organism_dataframe = pd.read_csv(organism_csv_file_path)


    # iterate over each row in organism dataframe 
    for _, row in organism_dataframe.iterrows():
        # create new organism object and save it to the database, values for the required fields are extracted 
        # current row in the loop using the column name as the key
        Organism.objects.create(
            taxa_id=row['taxa_id'],
            genus=row['genus'],
            species=row['species']
        )

    # Construct the relative path to the Protein.csv file using os.path.join()
    protein_csv_file_path = os.path.join(csv_dir, 'Protein.csv')
    # Read the Protein.csv file into a DataFrame
    protein_dataframe = pd.read_csv(protein_csv_file_path)



    # iterate over each row in protein dataframe
    for _, row in protein_dataframe.iterrows():
        # get organism object that matches taxa_id in current row of dataframe
        organism = Organism.objects.get(taxa_id=row['taxa_id'])
        # filter protein objects based on the protein_id found in current row of dataframe 
        proteins = Protein.objects.filter(protein_id=row['protein_id'])
        # if a matching protein object is found
        if proteins.exists():
            # retrieve the first object returned from the query
            protein = proteins.first()
            # update fields with values from current dataframe row 
            protein.clade = row['clade']
            protein.length = row['length']
            protein.pfam_id = row['pfam_id']
            protein.taxa_id = organism
            # save changes to the existing protein
            protein.save()
        else:
            # else if not matching protein objects were found, create one with the values 
            # from the current row of the dataframe
            Protein.objects.create(
                protein_id=row['protein_id'],
                clade=row['clade'],
                length=row['length'],
                pfam_id=row['pfam_id'],
                taxa_id=organism
            )

    # Load data from Sequence.csv using pandas
    sequence_csv_file_path = os.path.join(csv_dir, 'Sequence.csv')
    sequence_dataframe = pd.read_csv(sequence_csv_file_path)


    # iterate over each row in sequence dataframe
    for _, row in sequence_dataframe.iterrows():
        # filter protein objects based on the protein_id found in current row of dataframe
        proteins = Protein.objects.filter(protein_id=row['protein_id'])
        # if a matching protein object is found
        if proteins.exists():
            # retrieve the first object returned from the query
            protein = proteins.first()
            # create new sequence object with values from current row of dataframe 
            Sequence.objects.create(
                protein_id=protein,
                sequence=row['sequence']
            )


    # Load data from Domain.csv using pandas
    domain_csv_file_path = os.path.join(csv_dir, 'Domain.csv')
    domain_dataframe = pd.read_csv(domain_csv_file_path)



    # iterate over each row in domain dataframe
    for _, row in domain_dataframe.iterrows():
        # filter proteins objects based on protein_id found in current row of dataframe 
        proteins = Protein.objects.filter(protein_id__in=row['protein_id'].split(','))
        # if a matching protein object is found
        if proteins.exists():
            # create new domain object in database using values from current row of dataframe
            domain = Domain.objects.create(
                pfam_id=row['pfam_id'],
                description=row['description'],
                start=row['start'],
                stop=row['stop']
            )
            # associates domain object with filtered proteins by adding them to Many to Many field of domain object
            domain.protein_id.set(proteins)

    # Load data from PfamID.csv using pandas
    pfamID_csv_file_path = os.path.join(csv_dir, 'PfamID.csv')
    pfamID_dataframe = pd.read_csv(pfamID_csv_file_path)


    
    # iterate over each row in pfamID dataframe
    for _, row in pfamID_dataframe.iterrows():
        # filter domain objects based on pfam_id found in current row of dataframe 
        domains = Domain.objects.filter(pfam_id=row['domain_id'])
        # if a matching domain object exists with specified pfam 
        if domains.exists():
            # retrieve first object returned by the query
            domain = domains.first()
            # get domain description from current row
            domain_description = row['domain_description']
            # if exisitng pfam object associated with domain exists, get it
            pfam_id, created = PfamID.objects.get_or_create(
                domain_id=domain,
                defaults={'domain_description': domain_description}
            )
            # if not created, create it
            if not created:
                pfam_id.domain_description = domain_description
                pfam_id.save()

load_data()
# End of code I wrote for loading in the data. Support was found online for fixing bugs in the code 
