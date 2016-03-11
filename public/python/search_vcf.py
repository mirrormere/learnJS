###############################
#           Env               #

import sys
from BCBio import GFF
import numpy as np
import pandas as pd
import json
import re

#import config
import vcf

#to time the program:
import time

###############################
#          Methods            #

def get_vcf_reader():
	return vcf.Reader(open('/Users/caryn/Dropbox/Project_RiceGeneticVariation/data/rice_chr2_3.vcf.gz', 'r'))

def get_info ( gene ):
	info = open('/Users/caryn/Dropbox/Project_jsLearn/simple_genes/data/Chr2.locus_brief_info.7.0', 'r')
	gene_info = []
	myregex = r"(.*)" + re.escape(gene) + r"(.*)"
	for line in info:
		if re.match(myregex, line):
			gene_info.append(line)

	#check for multiple isoform information
	if (len(gene_info) > 1):
		maxlen = 0
		gene_info_keep = []
		#get the lengths of all the gene isoforms
		for line in gene_info:
			splitline = line.split('\t')
			length = int(splitline[4]) - int(splitline[3])
			if (length > maxlen):
				maxlen = length
				gene_info_keep = line
		return gene_info_keep

	#if there are no isoforms, return gene_info
	return gene_info

def get_start_stop ( info_line ):
	splitline = info_line.split('\t')

	info = {
		"chrom" : splitline[0],
		"gene_id" : splitline[1],
		"start" : int(splitline[3]),
		"end" : int(splitline[4]),
		"annotation" : splitline[9]
	}
	return info


def get_vcf_info ( info_dict ):
	"""get the genotypes for each position for each sample"""
	chrom = info_dict['chrom']
	start = info_dict['start']
	end = info_dict['end']

	vcf_reader = get_vcf_reader()

	gene_records = []
	for record in vcf_reader.fetch(chrom, start, end):
		gene_records.append(record)

	return gene_records

###############################
#            Main             #

if __name__ == '__main__':
	file, gene = sys.argv

	info_line = get_info(gene)
	info = get_start_stop(info_line)
	results = get_vcf_info(info)
	print results
	sys.stdout.flush()
