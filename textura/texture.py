#! /usr/bin/env python
# Textura
# Marcela Ribeiro de Oliveira
# GRR20157372

import cv2
import numpy as np
import argparse
import os
import bisect

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-d', '--directory', type=str, required=True, help='diretorio com as imagens')
	parser.add_argument('-ta', '--train', type=str, required=True, help='arquivo de saida (treino)')
	parser.add_argument('-te', '--test', type=str, required=True, help='arquivo de saida (teste)')
	parser.add_argument('-m', '--method', type=int, required=True, help='1 - lbp sem zoneamento\n 2 - lbp com 4 zonas\n 3 - lbp com 8 zonas')
	parser.add_argument('-r', '--radius', type=int, required=True, help='Raio do lbp\n')
	return parser.parse_args()

def read_dir(dir_name):
	imgs = []
	for content in os.listdir(dir_name):
		bisect.insort(imgs, content)
	return imgs

def find_classes(imgs):
	classes = {}
	cont = 0
	w = imgs[1].split("_")[0]
	classes.update({cont:w})
	for i in range(1, len(imgs)):
		w = imgs[i].split("_")[0]
		if(w!=classes.items()[-1][1]):
			cont = cont + 1
			classes.update({cont:w})
	print classes
	return classes

#only lbp
def c1(imgs, dir_name, radius):
	all_lbp = []
	for i in range(0, len(imgs)):
		img_name = dir_name + imgs[i]
		img = cv2.imread(img_name, 0)
		h = np.size(img, 0)
		w = np.size(img, 1)
		lbp_array = []
		for j in range(radius, h-radius):
			for k in range(radius, w-radius):
				lbp_result = calculate_lbp(j, k, img, radius)
				lbp_array.append(lbp_result)
		hist, bins = np.histogram(lbp_array, 256, [0, 255])
		all_lbp.append(hist)
	return all_lbp

#lbp to 4 zones
def c2(imgs, dir_name, radius):
	all_lbp = []
	for i in range(0, len(imgs)):
		img_name = dir_name + imgs[i]
		img = cv2.imread(img_name, 0)
		all_lbp.append(zones4(img, radius))
	return all_lbp

#lbp to 8 zones
def c3(imgs, dir_name, radius):
	all_lbp = []
	for i in range(0, len(imgs)):
		img_name = dir_name + imgs[i]
		img = cv2.imread(img_name, 0)
		all_lbp.append(zones8(img, radius))
	return all_lbp

def zones4(img, radius):
	hh, ww = img.shape[:2]
	hi = int(hh/2)
	wi = int(ww/2)
	n = img[0:hi, 0:wi]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone1 = hist

	n=img[hi:hh, 0:wi]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone2 = hist

	n=img[0:hi, wi:ww]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone3 = hist

	n=img[hi:hh, wi:ww]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone4 = hist

	return np.concatenate((zone1, zone2, zone3, zone4), axis=0)

def zones8(img, radius):
	hh, ww = img.shape[:2]
	hi = int(hh/2)
	wi = int(ww/4)
	n = img[0:hi, 0:wi]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone1 = hist

	n=img[hi:hh, 0:wi]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone2 = hist

	n=img[0:hi, wi:(wi*2)]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone3 = hist

	n=img[hi:hh, wi:(wi*2)]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone4 = hist

	n=img[0:hi, (wi*2):(wi*3)]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone5 = hist

	n=img[hi:hh, (wi*2):(wi*3)]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone6 = hist

	n=img[0:hi, (wi*3):ww]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone7 = hist

	n=img[hi:hh, (wi*3):ww]
	h = np.size(n, 0)
	w = np.size(n, 1)
	lbp_array = []
	for j in range(radius, h-radius):
		for k in range(radius, w-radius):
			lbp_result = calculate_lbp(j, k, n, radius)
			lbp_array.append(lbp_result)
	hist, bins = np.histogram(lbp_array, 256, [0, 255])
	zone8 = hist

	return np.concatenate((zone1, zone2, zone3, zone4, zone5, zone6, zone7, zone8), axis=0)



def calculate_lbp(j,k, img, radius):
	lbp_result = 0
	center = img[j][k]
	if(img[j-radius][k-radius]>=center):
		lbp_result = lbp_result+1
	if(img[j-radius][k]>=center):
		lbp_result = lbp_result+2
	if(img[j-radius][k+radius]>=center):
		lbp_result = lbp_result+4
	if(img[j][k-radius]>=center):
		lbp_result = lbp_result+8
	if(img[j][k+radius]>=center):
		lbp_result = lbp_result+16
	if(img[j+radius][k-radius]>=center):
		lbp_result = lbp_result+32
	if(img[j+radius][k]>=center):
		lbp_result = lbp_result+64
	if( img[j+radius][k+radius]>=center):
		lbp_result = lbp_result+128
	return lbp_result

def write_lbp(imgs, all_lbp, classes, file_train, file_test, n_min, n_max, n_features):
	first_line = "1120 " + str(n_features) + "\n"
	file_test.write(first_line)
	file_train.write(first_line)
	for s in range(0, len(imgs), 280):
		for i in range(s, s+140):
			w = imgs[i].split("_")[0]
			for j, k in classes.items():
				if (k == w):
					line = ""
					for l in range(0, len(all_lbp[i])):
						d = all_lbp[i][l]*1.0
						value = (d-n_min)/(n_max-n_min)
						line = line + str(value) + " "
					line = line + " " + str(j) + "\n"
					file_train.write(line)
	for s in range(140, len(imgs), 280):
		for i in range(s, s+140):
			w = imgs[i].split("_")[0]
			for j, k in classes.items():
				if (k == w):
					line = ""
					for l in range(0, len(all_lbp[i])):
						d = all_lbp[i][l]*1.0
						value = (d-n_min)/(n_max-n_min)
						line = line + str(value) + " "
					line = line + " " + str(j) + "\n"
					file_test.write(line)

if __name__ == "__main__":
	args = read_args()
	file_train = open(args.train, 'w')
	file_test = open(args.test, 'w')
	m = args.method
	radius = args.radius
	imgs = read_dir(args.directory)
	classes = find_classes(imgs)
	if m==1:
		all_lbp = c1(imgs, args.directory, radius)
		n_min = np.amin(all_lbp)
		n_max = np.amax(all_lbp)
		write_lbp(imgs, all_lbp, classes, file_train, file_test, n_min, n_max, 256)
	if m==2:
		all_lbp = c2(imgs, args.directory, radius)
		n_min = np.amin(all_lbp)
		n_max = np.amax(all_lbp)
		write_lbp(imgs, all_lbp, classes, file_train, file_test, n_min, n_max, 1024)
	if m==3:
		all_lbp = c3(imgs, args.directory, radius)
		n_min = np.amin(all_lbp)
		n_max = np.amax(all_lbp)
		write_lbp(imgs, all_lbp, classes, file_train, file_test, n_min, n_max, 2048)

