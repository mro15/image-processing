#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define REJECTED -1

typedef struct point{
  double *features;
  int rot_class;
  int freq_class;
  int rejected;
}point;

typedef struct inf{
  double distance;
  int rot_class;
}inf;

typedef struct ord_inf{
  int size;
  int n_elements;
}ord_inf;

typedef struct c{
  int class_c;
  int amount;
}c;

int test_args(int argc, char *argv[], FILE **training, FILE **test, int *k);
void read_first_line(FILE **file_in, int *n_points, int *n_features);
void read_file(FILE **file_in, int n_points, int n_features, point *p);
double calculate_distance(point p1, point p2, int n_features);
void insert_ord_inf(ord_inf *p, inf *dis, double distance, int rot_class);
int find_class(int k, inf dis[]);
int find_big(c vet[], int cont);
void confusion_matrix(point *points_ts, int n_points_ts, int n_points_tr);
void sort_class_vet(int *v, int size);
int get_mat_index(int **m, int c, int size);
