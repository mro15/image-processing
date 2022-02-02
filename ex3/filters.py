#! /usr/bin/env python
# Ex3: Filtros da Media e Mediana
# Marcela Ribeiro de Oliveira
# GRR20157372

import cv2
import argparse
import sys
import os.path
import numpy as np
import time

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-k', '--kernel', type=str, required=True, help='nome do arquivo com a mascara')
	parser.add_argument('-i', '--input', type=str, required=True, help='nome da imagem de entrada')
	return parser.parse_args()

def mean_filter(img, kernel):
	print "MY MEAN"
	i, j = kernel.shape
	new_img = np.copy(img)
	h = np.size(img, 0)
	w = np.size(img, 1)
	center = i/2
	den = np.sum(kernel)
	s_time = time.time()

	for ii in range(0, h-i+1):
		for jj in range(0, w-j+1):
			summ = [0,0,0]
			for k in range(0, i):
				for l in range(0, j):
					#print ii+k, jj+l
					summ[0] = summ[0] + (img[ii+k][jj+l][0]*kernel[k, l])
					summ[1] = summ[1] + (img[ii+k][jj+l][1]*kernel[k, l])
					summ[2] = summ[2] + (img[ii+k][jj+l][2]*kernel[k, l])
					if k == l and k == center:
						subh = ii+k
						subw = jj+l
						#print subh, subw
			new_img[subh, subw][0] = summ[0]/den
			new_img[subh, subw][1] = summ[1]/den
			new_img[subh, subw][2] = summ[2]/den
	f_time = time.time() - s_time
	cv2.imwrite("my_mean.png", new_img)
	print "Time: ", f_time

def median_filter(img, kernel):
	print "MY MEDIAN"
	i, j = kernel.shape
	new_img = np.copy(img)
	h = np.size(img, 0)
	w = np.size(img, 1)
	center = i/2
	s_time = time.time()

	for ii in range(0, h-i+1):
		for jj in range(0, w-j+1):
			summ = [[], [], []]
			for k in range(0, i):
				for l in range(0, j):
					#print ii+k, jj+l
					summ[0].append(img[ii+k][jj+l][0])
					summ[1].append(img[ii+k][jj+l][1])
					summ[2].append(img[ii+k][jj+l][2])
					if k == l and k == center:
						subh = ii+k
						subw = jj+l
			new_img[subh, subw][0] = int(np.median(summ[0]))
			new_img[subh, subw][1] = int(np.median(summ[1]))
			new_img[subh, subw][2] = int(np.median(summ[2]))
	f_time = time.time() - s_time
	cv2.imwrite("my_median.png", new_img)
	print "Time: ", f_time

def gaussian_filter(img, i, j):
	print "CV GAUSSIAN"
	s_time = time.time()
	new_img = cv2.GaussianBlur(img, (i, j), 0)
	f_time = time.time() - s_time
	cv2.imwrite("cv_gaussian.png", new_img)
	print "Time: ", f_time

def blur_filter(img, i, j):
	print "CV BLUR"
	s_time = time.time()
	new_img = cv2.blur(img, (i, j))
	f_time = time.time() - s_time
	cv2.imwrite("cv_blur.png", new_img)
	print "Time: ", f_time

def twoD_filter(img, kernel):
	print "CV 2D"
	s_time = time.time()
	new_img = cv2.filter2D(img, -1, kernel)
	f_time = time.time() - s_time
	cv2.imwrite("cv_2d.png", new_img)
	print "Time: ", f_time

def cv_median_filter(img, i):
	print "CV MEDIAN"
	s_time = time.time()
	new_img = cv2.medianBlur(img, i)
	f_time = time.time() - s_time
	cv2.imwrite("cv_median.png", new_img)
	print "Time: ", f_time

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
	mean_filter(img, kernel)
	median_filter(img, kernel)
	gaussian_filter(img, i, j)
	blur_filter(img, i, j)
	twoD_filter(img, kernel)
	cv_median_filter(img, i)

