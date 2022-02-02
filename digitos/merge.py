#! /usr/bin/env python

import argparse

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-f', '--file', type=str, required=True, help='arquivo com o nome das imagens para extrair caracteristicas')
	parser.add_argument('-o', '--output', type=str, required=True, help='arquivo de saida')
	return parser.parse_args()

def read_files(f1, f2):
	with open(f1) as f:
		c = f.read().splitlines()
	with open(f2) as f:
		d = f.read().splitlines()
	lol = open("out.txt", 'w')
	for i in range(0, len(c)):
		line = ""
		#for j in range(0, len(c[i])):
		line = line + str(c[i]) + " " + str(d[i])
		line = line + "\n"
		lol.write(line)

if __name__ == "__main__":
	args = read_args()
	f1 = args.file
	f2 = args.output
	read_files(f1, f2)
