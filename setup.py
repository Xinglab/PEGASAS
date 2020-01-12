#!/usr/bin/env python

from setuptools import setup


def main():
	setup(
		name='PEGASAS',
		  
		version='1.1.0',
		  
		description='',

		author='Yang Pan',

		author_email='panyang@ucla.edu',

		url='',

		packages=['PEGASAS','PEGASAS.data'],

		scripts=['bin/PEGASAS'],

		include_package_data=True,

		package_data={'PEGASAS.data':[
		'hallmarks50.gmt.txt'],'PEGASAS':[
		'cor_matrix_direct_perm.R', 'GO_plot.R','GO_enrichr_plot.R']},
		install_requires=['matplotlib','numpy','scipy']
		 )
	return

if __name__ == '__main__':
	main()

