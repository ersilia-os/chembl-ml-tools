from setuptools import setup, find_packages
from packagename.version import Version

with open("requirements.txt") as f:
    install_requires = [r for r in f.read().splitlines() if not r.startswith("#")]

setup(name='chembl_ml_tools',
      version='0.0.1',
      description='Tools for obtaining Chembl data for machine learning models',
      long_description=open('README.md').read().strip(),
      author='Marcos de la Torre',
      author_email='marcostorrework@gmail.com',
      url='https://github.com/ersilia-os/chembl_ml_tools',
      install_requires=[],
      license='MIT',
      python_requires='>=3.7',
      install_requires=[
        'pandas',
        'psycopg2',
        'os',
      ],
      packages=find_packages(include=['chembl_ml_tools', 'chembl_ml_tools.*']),
      keywords='drug-discovery machine-learning ersilia chembl',
      classifiers=[],
      )
