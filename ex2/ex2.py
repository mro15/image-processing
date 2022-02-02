#! /usr/bin/env python
# Ex2: Classificacao com Histogramas
# Marcela Ribeiro de Oliveira
# GRR20157372

import cv2
import cv
import argparse
import sys
from collections import OrderedDict

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-i', '--input', type=str, required=True, help='nome da imagem de entrada')
	parser.add_argument('-n', '--names', type=str, required=True, help='arquivo com o nome das imagens para comparar')
	parser.add_argument('-m', '--method', type=str, required=True, help='metodo de comparacao a ser utilizado')
	return parser.parse_args()

def calculate_similarity(img1, comp_hash, comp_met):
	o = OrderedDict(sorted(comp_hash.items()))
	#print o
	#print comp_met
	if comp_met == "BHATTACHARYYA" or comp_met == "CHISQR":
		#o mais semelhante e o menor valor
		print "O mais parecido com " + img1 + " e: "
		print o.items()[0][1][0]
	else:
		#o mais semelhante e o maior valor
		print "O mais parecido com " + img1 + " e: "
		print o.items()[-1][1][0]

def read_input(img_in, file_in):
	imgs = []
	with open(file_in) as img:
		for line in img:
			imgs.append(line.rstrip())
	imgs.remove(img_in)
	return imgs

def calculate_histograms(img_in, imgs, compare):
	channels = ['b', 'g', 'r']
	methods = {	"BHATTACHARYYA": (cv.CV_COMP_BHATTACHARYYA),
							"CORREL": (cv.CV_COMP_CORREL),
							"CHISQR": (cv.CV_COMP_CHISQR),
							"INTERSECT": (cv.CV_COMP_INTERSECT)}
	comp = cv2.imread(img_in)
	compare_method = methods[compare]
	h_c = []
	c = []
	for ch, col in enumerate(channels):
		h_c.append(cv2.calcHist([comp], [ch], None, [256], [0, 255]))
		cv2.normalize(h_c[-1], h_c[-1], 0, 255, cv2.NORM_MINMAX)
		c.append(cv2.compareHist(h_c[-1], h_c[-1], compare_method))
	#print "comparacao da imagem com ela mesma"
	#print c

	batata = {}
	for i in imgs:
		img = cv2.imread(i)
		bhat = []
		j = 0
		for ch, col in enumerate(channels):
			hist = cv2.calcHist([img], [ch], None, [256], [0, 255])
			cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
			bhat.append(cv2.compareHist(h_c[j], hist, compare_method))
			j = j+1
		summ = sum(bhat)
		summ = summ/3.0
		batata.update({summ: (i, bhat)})
	#print batata
	calculate_similarity(img_in, batata, compare)


if __name__ == "__main__":
	args = read_args()
	imgs = read_input(args.input, args.names)
	methods = ["BHATTACHARYYA", "CORREL", "CHISQR", "INTERSECT"]
	if args.method in methods:
		calculate_histograms(args.input, imgs, args.method)
	else:
		print "Esse metodo de comparacao nao existe, os possiveis sao:"
		print methods
		sys.exit()
