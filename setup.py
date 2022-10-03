from setuptools import setup, find_packages

setup(name='chemblmltools',
      version='0.0.1',
      description='Tools for obtaining Chembl data for machine learning models',
      long_description=open('README.md').read().strip(),
      author='Marcos de la Torre',
      author_email='marcostorrework@gmail.com',
      url='https://github.com/ersilia-os/chembl_ml_tools',
      license='MIT',
      python_requires='>=3.7',
      install_requires=[
        'pandas',
        'psycopg2-binary'
      ],
      packages=find_packages(exclude=("utilities")),
      keywords='drug-discovery machine-learning ersilia chembl',
      classifiers=[
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Scientific/Engineering :: Artificial Intelligence",
      ],
      include_package_data=True
      )