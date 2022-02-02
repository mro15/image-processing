#! /usr/bin/env python
# Ex4: Projecao de histograma
# Marcela Ribeiro de Oliveira
# GRR20157372

import cv2
import argparse
import numpy as np
import scipy.signal

def read_args():
	parser = argparse.ArgumentParser(description='Os parametros sao:')
	parser.add_argument('-i', '--input', type=str, required=True, help='nome da imagem de entrada')
	return parser.parse_args()

if __name__ == "__main__":
	args = read_args()
	img = cv2.imread(args.input, 0)
	ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	i = th2.shape[0]
	j = th2.shape[1]

	vet = np.zeros(i)
	for ii in range(0, i): #all lines
		vet[ii] = j - (np.sum(th2[ii])/255)

	# #Find a way to suavize peaks (blur filter)
	vet = cv2.blur(vet,(10,10))

	indexes = scipy.signal.argrelextrema(
    	np.array(vet),
    	comparator=np.greater,order=40
		)
	#print('Peaks are: %s' % (indexes[0]))
	print len(indexes[0])

	#draw the lines
	for i in range(0, len(indexes[0])):
		cv2.line(img, (0, indexes[0][i]),(j, indexes[0][i]),(0,0,255),2)
	cv2.imwrite("lines.png", img)
