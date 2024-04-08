from setuptools import setup, find_packages

setup(name='chemblmltools',
      version='0.0.2',
      description='Tools for obtaining Chembl data for machine learning models',
      long_description=open('README.md').read().strip(),
      author="Ersilia Open Source Initiative",
      author_email="hello@ersilia.io",
      url='https://github.com/ersilia-os/chembl-ml-tools',
      license='GPLv3',
      python_requires='>=3.7',
      install_requires=[
        'pandas',
        'rdkit',
        'psycopg2-binary'
      ],
      packages=find_packages(exclude=("utilities")),
      keywords='drug-discovery machine-learning ersilia chembl',
      classifiers=[
          "Programming Language :: Python :: 3.10",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          "Topic :: Scientific/Engineering :: Artificial Intelligence",
      ],
      include_package_data=True
      )