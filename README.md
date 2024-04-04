# chembl_ml_tools

Tools to obtain data from the ChEMBL database to be used as input for Machine Learning models.

This package provides:

- Function `chembl_activity_target`, to extract all assay results for a given organism.

- Class `ChemblMoleculeSampler`, to obtain a random sample of molecules existing in the ChEMBL database, excluding a list of known molecules. Useful to generate negative cases for a model.

## Requirements

These tools require access to a postgres database server containing the ChEMBL database. You may install ChEMBL in your own computer 
by following these instructions: [How to install ChEMBL](doc/install_chembl.md)

This package is a general ChEMBL access prepared to work within the [Antimicrobial ML tasks package](https://github.com/ersilia-os/antimicrobial-ml-tasks). If you want to use it for other applications please make the necessary modifications.

## Installation

To install the package in a conda environment, please run:
```
pip install git+https://github.com/ersilia-os/chembl_ml_tools.git
```
## Testing

You can use the folowing code to check that the package is working. This test assumes that there is a DB user called `chembl_user` with permissions to read the database.

Before running, make sure that the postgres service with the ChEMBL database is up.

```
import pandas as pd
from chemblmltools import chembl_activity_target

df1 = chembl_activity_target(
        db_user='chembl_user',
        db_password='aaa',
        organism_contains='enterobacter',
        max_heavy_atoms=100)

print(df1.head(5))
```
