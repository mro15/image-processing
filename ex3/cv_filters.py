#! /usr/bin/env python
# Ex3: Filtros da Media e Mediana
# Marcela Ribeiro de Oliveira
# GRR20157372

import cv2
import argparse
import sys
import os.path
import numpy as np

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-k', '--kernel', type=str, required=True, help='nome do arquivo com a mascara')
	parser.add_argument('-i', '--input', type=str, required=True, help='nome da imagem de entrada')
	return parser.parse_args()

def gaussian_filter(img, i, j):
	new_img = cv2.GaussianBlur(img, (i, j), 0)
	cv2.imwrite("img_gaussian_cv.png", new_img)

def blur_filter(img, i, j):
	new_img = cv2.blur(img, (i, j))
	cv2.imwrite("img_blur_cv.png", new_img)

def twoD_filter(img, kernel):
	new_img = cv2.filter2D(img, -1, kernel)
	cv2.imwrite("img_2d_cv.png", new_img)

def median_filter(img, i):
	new_img = cv2.medianBlur(img, i)
	cv2.imwrite("img_median_cv.png", new_img)

def mount_kernel(file_in):
	if not(os.path.exists(file_in)) or  not(os.path.isfile(file_in)):
		print "Arquivo de entrada nao existe"
		sys.exit()
	f = open(file_in, 'r')
	kernel = []
	for line in f:
		line = line.replace('[','').replace(']','')
		fields = line.strip().split(',')
		for field in fields:
			kernel.append([ int(x) for x in field.strip().split(' ') ])
	f.close()
	return kernel

if __name__ == "__main__":
	args = read_args()
	kernel = np.array(mount_kernel(args.kernel))
	i, j = kernel.shape
	img = cv2.imread(args.input)
	gaussian_filter(img, i, j)
	blur_filter(img, i, j)
	twoD_filter(img, kernel)
	median_filter(img, i)

