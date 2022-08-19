#!/usr/bin/env python
"""
	Increments a semantic version string (of the form 0.0.0)

	-M --> Increment the major number (1.0.0 --> 2.0.0)
	-m --> Increment the minor number (0.1.0 --> 0.2.0)
	-p --> Increment the patch number (0.0.1 --> 0.0.2)
	If no switches given, will increment the patch only.

	If M or m are incremented , the 'smaller' parts of the semvar are
	reset to zero: 
	# semvar++ -m 2.3.6  -->  2.4.0
	# semvar++ -M 2.3.6  -->  3.0.0
"""
import argparse
from re import findall

if __name__ == "__main__":
	par=argparse.ArgumentParser()
	cg = par.add_mutually_exclusive_group()
	cg.add_argument('-M', help='major', action='store_true', default=False)
	cg.add_argument('-m', help='minor', action='store_true', default=False)
	cg.add_argument('-p', help='patch', action='store_true', default=True)
	par.add_argument('version', help="The SemVar string you want to increment")
	argv = par.parse_args()
	
	# This parsing is really simplified. edge cases won't be 
	# accepted. 
	x = findall('^[Vv]?(\d+)\.(\d+)\.(\d+)$', argv.version)
	if len(x) == 0:
		print("0.0.0")
		exit(-1)
	try:
		M = int(x[0][0])
		m = int(x[0][1])
		p = int(x[0][2])
	except:
		print("0.0.0")
		exit(-1)

	if argv.M:
		M += 1
		m = 0
		p = 0
		print(f"{M}.{m}.{p}")
		exit(0)

	if argv.m:
		m += 1 
		p = 0
		print(f"{M}.{m}.{p}")
		exit(0)

	if argv.p:
		p +=1
		print(f"{M}.{m}.{p}")
		exit(0)
