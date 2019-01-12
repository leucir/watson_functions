from setuptools import setup, find_packages

setup(
  name='asdemo',
  version='1.0.5',
  packages=find_packages(),
  dependency_links=['h5py','tensorflow','keras']
  )
