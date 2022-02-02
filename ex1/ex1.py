#! /usr/bin/env python
# Ex1: Amostragem e quantizacao
# Marcela Ribeiro de Oliveira
# GRR20157372
import numpy as np
import cv2
import argparse
from scipy.stats import mode

def read_args():
  parser = argparse.ArgumentParser(description='Os parametros sao:')
  parser.add_argument('-i', '--input', type=str, required=True, help='nome da imagem de entrada')
  parser.add_argument('-o', '--output', type=str, required=True, help='nome da imagem de saida')
  parser.add_argument('-p', '--percentage', type=int, required=True, help= 'percentual de amostragem')
  parser.add_argument('-q', '--amount', type=int, required=True, help= 'quantidade de niveis de cinza')
  parser.add_argument('-t', '--technique', type=str, required=True, help= 'tecnica: media, mediana ou moda')
  return parser.parse_args()

def sampling_aum(img, n, tec):
  h = np.size(img, 0)
  w = np.size(img, 1)
  ph = int(h*n)
  pw = int(w*n)
  cont_h = 0
  cont_w = 0
  new_image = np.zeros((h+ph, w+pw, 1), np.uint8)
  for wi in range(0, w, w/pw):
    for he in range(0, h, h/ph):
      offset_w = wi
      offset_h = he
      summ = 0
      a = []
      for wid in range(offset_w, offset_w+(w/pw)):
        for hei in range(offset_h, offset_h+(h/ph)):
          if (wid==w) or (hei==h):
            break
          else:
            summ += img[hei, wid]
            a.append(img[hei, wid])
        if(wid==w):
          break
      if tec == "media":
        average = summ
        #img[offset_h:offset_h+n, offset_w:offset_w+n] = average
        new_image[offset_h:he, offset_w:wi] = average
      if tec == "moda":
        #img[offset_h:offset_h+n, offset_w:offset_w+n] = mode(a)[0]
        new_image[he, wi] = mode(a)[0]
      if tec == "mediana":
        #img[offset_h:offset_h+n, offset_w:offset_w+n] = np.median(a)
        new_image[he, wi] = np.median(a)
      cont_w = cont_w + 1
      cont_h = cont_h + 1
  #quantization(new_image, args.amount)
  cv2.imwrite(args.output, new_image)

def sampling(img, n, tec):
  h = np.size(img, 0)
  w = np.size(img, 1)
  new_image = np.zeros((h/n, w/n, 1), np.uint8)
  for wi in range(0, w/n):
    for he in range(0, h/n):
      offset_h = n * he
      offset_w = n * wi
      summ = 0
      a = []
      for wid in range(offset_w, offset_w+n):
        for hei in range(offset_h, offset_h+n):
          summ += img[hei, wid]
          a.append(img[hei, wid])
      if tec == "media":
        average = summ/(n*n)
        #img[offset_h:offset_h+n, offset_w:offset_w+n] = average
        new_image[he, wi] = average
      if tec == "moda":
        #img[offset_h:offset_h+n, offset_w:offset_w+n] = mode(a)[0]
        new_image[he, wi] = mode(a)[0]
      if tec == "mediana":
        #img[offset_h:offset_h+n, offset_w:offset_w+n] = np.median(a)
        new_image[he, wi] = np.median(a)
  quantization(new_image, args.amount)

def quantization(img, amount):
  h = np.size(img, 0)
  w = np.size(img, 1)
  div = int(256/amount)
  for wi in range (0,w):
    for he in range(0, h):
      i = 0
      while i <= 256:
        if ((img[he, wi] < (i+div)) and (img[he, wi] >= (i))):
          img[he,wi] = (i+(i+div))/2
        i = i+div
  cv2.imwrite(args.output, img)

if __name__ == "__main__":
  args = read_args()
  img = cv2.imread(args.input, 0)
  if args.percentage <= 100:
    n = (100/args.percentage)
    sampling(img, int(n), args.technique)
  else:
    #n = (args.percentage-100)/(100.0)
    #sampling_aum(img, n, args.technique)
    quantization(img, args.amount)


