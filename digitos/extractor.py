#! /usr/bin/env python
# Reconhecimento de Digitos Manuscritos
# Marcela Ribeiro de Oliveira
# GRR20157372

import cv2
import numpy as np
import argparse

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-f', '--file', type=str, required=True, help='arquivo com o nome das imagens para extrair caracteristicas')
	parser.add_argument('-o', '--output', type=str, required=True, help='arquivo de saida')
	parser.add_argument('-m', '--method', type=str, required=True,
											help='1 - histograma do contorno - 4 zonas\n, 2 - histograma do contorno - 8 zonas\n, 3 - histograma do contorno - 16 zonas,\n 4, 5, 6 (com resize das imagens),\n 7 - perfil do histograma')
	return parser.parse_args()


def read_input(file_in):
	imgs = []
	with open(file_in) as img:
		for line in img:
			imgs.append(line.split())
	return imgs

def min_max_norm(lol):
	v_min = lol[0][0][0]
	v_max = lol[0][0][0]
	for k in range(0, len(lol)):
		for i in range(0, len(lol[k])):
			for j in range(0, len(lol[k][i])):
				if(lol[k][i][j] > v_max):
					v_max = lol[k][i][j]
				if(lol[k][i][j] < v_min):
					v_min = lol[k][i][j]
	values = []
	values.append(v_min)
	values.append(v_max)
	return values

def normalize(lol, f, min_max, imgs):
	for k in range(0, len(lol)):
		line = ""
		#print len(lol[k])
		for i in range(0, len(lol[k])):
			#print len(lol[k][i])
			for j in range(0, len(lol[k][i])):
				value = (lol[k][i][j] - min_max[0])/(min_max[1] - min_max[0])
				line = line + " " + str(value)
		line = line + " " + str(imgs[k][1]) + "\n"
		f.write(line)

def contour_histogram(zones):
	hist = []
	for i in range(0, len(zones)):
		contours, hierarchy = cv2.findContours(zones[i],cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		vet = np.zeros(8)
		for j in range(0, len(contours)):
			x = contours[j][0][0][0]
			y = contours[j][0][0][1]
			for k in range(1, len(contours[j])):
				xi = contours[j][k][0][0]
				yi = contours[j][k][0][1]
				if(xi==x+1 and yi==y):
					# direcao 0
					vet[0] = vet[0]+1
				elif(xi==x+1 and yi==y+1):
					#direcao 1
					vet[1] = vet[1]+1
				elif(xi==x and yi==y+1):
					#direcao 2
					vet[2] = vet[2]+1
				elif(xi==x-1 and yi==y+1):
					#direcao 3
					vet[3] = vet[3]+1
				elif(xi==x-1 and yi==y):
					#direcao 4
					vet[4] = vet[4]+1
				elif(xi==x-1 and yi==y-1):
					#direcao 5
					vet[5] = vet[5]+1
				elif(xi==x and yi==y-1):
					#direcao 6
					vet[6] = vet[6]+1
				elif(xi==x+1 and yi==y-1):
					#direcao 7
					vet[7] = vet[7]+1
				x = xi
				y = yi
		hist.append(vet)
	return hist

def resize(imgs):
	rett = []
	for i in range(0, len(imgs)):
	#for i in range(0, 10):
		img = cv2.imread(imgs[i][0], 0)
		ret, imgray = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		img2 = cv2.resize(imgray, (64, 64))
		rett.append([img2, imgs[i][1]])
	return rett

def not_resize(imgs):
	rett = []
	for i in range(0, len(imgs)):
	#for i in range(0, 10):
		img = cv2.imread(imgs[i][0], 0)
		ret, imgray = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		rett.append([img, imgs[i][1]])
	return rett

#todo dar resize pra metade
def histogram_profiles(imgs, o):
	lol = []
	f = open(o, 'w')
	for k in range(0, len(imgs)):
		img = imgs[k][0]
		i = img.shape[0]
		j = img.shape[1]
		vet = np.zeros(i)
		for ii in range(0, i): #all lines
			vet[ii] = j - (np.sum(img[ii])/255)
		lol.append(vet)
	big = lol[0][0]
	low = lol[0][0]
	for i in range(0, len(lol)):
		for j in range(1, len(lol[i])):
			if(lol[i][j]>big):
				big = lol[i][j]
			if(lol[i][j]<low):
				low = lol[i][j]
	for i in range(0, len(lol)):
		line = ""
		for j in range(0, len(lol[i])):
			value = (lol[i][j] - low)/(big - low)
			line = line + " " + str(value)
		line = line + " " + str(imgs[i][1]) + "\n"
		f.write(line)


def zoning16(imgs, o):
	lol = []
	f = open(o, 'w')
	for i in range(0, len(imgs)):
	#for i in range(0, 10):
		img = imgs[i][0]
		#img = cv2.imread(imgs[i][0], 0)
		ret, imgray = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		h, w = imgray.shape[:2]
		if(h>1 and w>1):
			hi = int(h/4)
			wi = int(w/4)
			n = []
			n.append(imgray[0:hi, 0:wi])
			n.append(imgray[hi:(hi*2), 0:wi])
			n.append(imgray[(hi*2):(hi*3), 0:wi])
			n.append(imgray[(hi*3):h, 0:wi])
			n.append(imgray[0:hi, wi:(wi*2)])
			n.append(imgray[hi:(hi*2), wi:(wi*2)])
			n.append(imgray[(hi*2):(hi*3), wi:(wi*2)])
			n.append(imgray[(hi*3):h, wi:(wi*2)])
			n.append(imgray[0:hi, (wi*2):(wi*3)])
			n.append(imgray[hi:(hi*2), (wi*2):(wi*3)])
			n.append(imgray[(hi*2):(hi*3), (wi*2):(wi*3)])
			n.append(imgray[(hi*3):h, (wi*2):(wi*3)])
			n.append(imgray[0:hi, (wi*3):w])
			n.append(imgray[hi:(hi*2), (wi*3):w])
			n.append(imgray[(hi*2):(hi*3), (wi*3):w])
			n.append(imgray[(hi*3):h, (wi*3):w])
			lol.append(contour_histogram(n))
		else:
			if(w>8):
		 		wi = int(w/16)
				n = []
				n.append(imgray[0:h, 0:wi])
				n.append(imgray[0:h, wi:(wi*2)])
				n.append(imgray[0:h, (wi*2):(wi*3)])
				n.append(imgray[0:h, (wi*3):(wi*4)])
				n.append(imgray[0:h, (wi*4):(wi*5)])
				n.append(imgray[0:h, (wi*6):(wi*7)])
				n.append(imgray[0:h, (wi*7):(wi*8)])
				n.append(imgray[0:h, (wi*8):(wi*9)])
				n.append(imgray[0:h, (wi*9):(wi*10)])
				n.append(imgray[0:h, (wi*10):(wi*11)])
				n.append(imgray[0:h, (wi*12):(wi*13)])
				n.append(imgray[0:h, (wi*13):(wi*14)])
				n.append(imgray[0:h, (wi*14):(wi*15)])
				n.append(imgray[0:h, (wi*15):w])
				lol.append(contour_histogram(n))
			elif(h>8):
				#todo: fix
				hi = int(h/16)
				n = []
				n.append(imgray[0:hi, 0:w])
				n.append(imgray[hi:(hi*2), 0:w])
				n.append(imgray[(hi*2):(hi*3), 0:w])
				n.append(imgray[(hi*3):(hi*4), 0:w])
				n.append(imgray[(hi*5):(hi*6), 0:w])
				n.append(imgray[(hi*6):(hi*7), 0:w])
				n.append(imgray[(hi*7):h, 0:w])
				lol.append(contour_histogram(n))
			else:
				print "deu ruim"
				print imgs[i][1]
	min_max = min_max_norm(lol)
	normalize(lol, f, min_max, imgs)

def zoning8(imgs, o):
	lol = []
	f = open(o, 'w')
	for i in range(0, len(imgs)):
	#for i in range(0, 10):
		img = imgs[i][0]
		#img = cv2.imread(imgs[i][0], 0)
		ret, imgray = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		h, w = imgray.shape[:2]
		if(h>1 and w>1):
			hi = int(h/2)
			wi = int(w/4)
			n = []
			n.append(imgray[0:hi, 0:wi])
			n.append(imgray[hi:h, 0:wi])
			n.append(imgray[0:hi, wi:(wi*2)])
			n.append(imgray[hi:h, wi:(wi*2)])
			n.append(imgray[0:hi, (wi*2):(wi*3)])
			n.append(imgray[hi:h, (wi*2):(wi*3)])
			n.append(imgray[0:hi, (wi*3):w])
			n.append(imgray[hi:h, (wi*3):w])
			lol.append(contour_histogram(n))
		else:
			if(w>8):
		 		wi = int(w/8)
				n = []
				n.append(imgray[0:h, 0:wi])
				n.append(imgray[0:h, wi:(wi*2)])
				n.append(imgray[0:h, (wi*2):(wi*3)])
				n.append(imgray[0:h, (wi*3):(wi*4)])
				n.append(imgray[0:h, (wi*4):(wi*5)])
				n.append(imgray[0:h, (wi*6):(wi*7)])
				n.append(imgray[0:h, (wi*7):w])
				lol.append(contour_histogram(n))
			elif(h>8):
				hi = int(h/8)
				n = []
				n.append(imgray[0:hi, 0:w])
				n.append(imgray[hi:(hi*2), 0:w])
				n.append(imgray[(hi*2):(hi*3), 0:w])
				n.append(imgray[(hi*3):(hi*4), 0:w])
				n.append(imgray[(hi*4):(hi*5), 0:w])
				n.append(imgray[(hi*5):(hi*6), 0:w])
				n.append(imgray[(hi*6):(hi*7), 0:w])
				n.append(imgray[(hi*7):h, 0:w])
				lol.append(contour_histogram(n))
			else:
				print "deu ruim"
				print imgs[i][1]
	min_max = min_max_norm(lol)
	normalize(lol, f, min_max, imgs)

def zoning4(imgs, o):
	lol = []
	f = open(o, 'w')
	for i in range(0, len(imgs)):
	#for i in range(0, 10):
		#img = cv2.imread(imgs[i][0], 0)
		img = imgs[i][0]
		ret, imgray = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		h, w = imgray.shape[:2]
		if(h>1 and w>1):
			hi = int(h/2)
			wi = int(w/2)
			n = []
			n.append(imgray[0:hi, 0:wi])
			n.append(imgray[hi:h, 0:wi])
			n.append(imgray[0:hi, wi:w])
			n.append(imgray[hi:h, wi:w])
			lol.append(contour_histogram(n))
		else:
			if(w>4):
		 		wi = int(w/4)
				n = []
				n.append(imgray[0:h, 0:wi])
				n.append(imgray[0:h, wi:(wi*2)])
				n.append(imgray[0:h, (wi*2):(wi*3)])
				n.append(imgray[0:h, (wi*3):w])
				lol.append(contour_histogram(n))
			if(h>4):
				hi = int(h/4)
				n = []
				n.append(imgray[0:hi, 0:w])
				n.append(imgray[hi:(hi*2), 0:w])
				n.append(imgray[(hi*2):(hi*3), 0:w])
				n.append(imgray[(hi*3):h, 0:w])
				lol.append(contour_histogram(n))
	min_max = min_max_norm(lol)
	normalize(lol, f, min_max, imgs)

if __name__ == "__main__":
	args = read_args()
	imgs = read_input(args.file)
	m = int(args.method)
	o = args.output
	if(m==1):
		r = not_resize(imgs)
		zoning4(r, o)
	elif(m==2):
		r = not_resize(imgs)
		zoning8(r, o)
	elif(m==3):
		r = not_resize(imgs)
		zoning16(r, o)
	elif(m==4):
		r = resize(imgs)
		zoning4(r, o)
	elif(m==5):
		r = resize(imgs)
		zoning8(r, o)
	elif(m==6):
		r = resize(imgs)
		zoning16(r, o)
	elif(m==7):
		r = resize(imgs)
		histogram_profiles(r, o)
