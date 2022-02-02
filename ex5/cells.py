#! /usr/bin/env python
# Ex5: Morfologia Matematica
# Marcela Ribeiro de Oliveira
# GRR20157372

import cv2
import argparse
import numpy as np

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-i', '--input', type=str, required=True, help='nome da imagem de entrada')
	return parser.parse_args()

def cell_contour_mean(c):
	med = 0
	for i in c:
		med +=len(i)
	med /= len(contours)
	return med

def cell_contour_median(c):
	med = []
	for i in c:
		med.append(len(i))
	return np.median(med)

def count_and_draw_cells(img, c, med):
		cont = 0
		for i in c:
			cv2.drawContours(img, [i], -1, (255, 0, 0), 2)
			l = len(i)
			if l > med:
				cont += int(round(l/med)) #se for maior que o contorno medio incrementa o contador na proporcao que e maior
			else:
				cont += 1
		print "Numero de celulas detectadas: " + str(cont)
		return img


if __name__ == "__main__":
	args = read_args()
	img = cv2.imread(args.input, 0)
	img_out = cv2.imread(args.input)

	ret, th2 = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY_INV); #binariza

	h, w = th2.shape[:2]
	kernel = np.zeros((h+2, w+2), np.uint8)
	img_f = th2.copy();

	cv2.floodFill(img_f, kernel, (220,5), 255); #flood fill
	img_fi = cv2.bitwise_not(img_f) #inverte pretos e brancos
	img_back = th2 | img_fi #subtrai a imagem binarizada da invertida pra separar o fundo

	#aplica fechamento pra fechar os nucleos das celulas
	img_c = cv2.morphologyEx(img_back, cv2.MORPH_CLOSE, cv2.getStructuringElement( cv2.MORPH_ELLIPSE, (3,3)))
	kernel1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
	img_e = cv2.erode(img_c, kernel1, iterations=5) #erosao pra separar celular grudadas

	#encontra os contornos da imagem
	contours, hierarchy = cv2.findContours(img_e,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#med = cell_contour_mean(contours) #acha o tamanho medio dos contornos
	median = cell_contour_median(contours) #acha a mediana do tamanhos dos contornos
	final = count_and_draw_cells(img_out, contours, median)
	cv2.imshow("final", final)
	#cv2.imshow("th2", th2)
	#cv2.imshow("imgf", img_f)
	#cv2.imshow("img_fi", img_fi)
	cv2.waitKey(0)
	cv2.imwrite("cells_detected.jpg", final)
