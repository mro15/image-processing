#include "include/knn.h"

int main(int argc, char *argv[]){
    if(argc < 4){
      printf("Uso: ./knn <treinamento> <teste> <k>\n");
      exit(1);
    }
    int k, n_points_tr, n_points_ts, n_features_tr, n_features_ts, i, j, n_rejected = 0, n_error = 0, n_correct = 0;
    FILE *training, *test;
    if(!test_args(argc, argv, &training, &test, &k)){
      printf("Erro com as entradas\n");
      exit(1);
    }
    read_first_line(&training, &n_points_tr, &n_features_tr);
    printf("Base de treino, pontos: %d, caracteristicas: %d\n",
              n_points_tr, n_features_tr);
    read_first_line(&test, &n_points_ts, &n_features_ts);
    printf("Base de teste, pontos: %d, caracteristicas: %d\n",
              n_points_ts, n_features_ts);
    printf("k: %d\n", k);

    point *points_tr, *points_ts;
    points_tr = malloc(n_points_tr * sizeof(point));
    for (i=0; i<n_points_tr; ++i){
      points_tr[i].features = malloc(n_features_tr * sizeof(double));
    }
    read_file(&training, n_points_tr, n_features_tr, points_tr);

    points_ts = malloc(n_points_ts * sizeof(point));
    for (i=0; i<n_points_ts; ++i){
      points_ts[i].features = malloc(n_features_ts * sizeof(double));
    }
    read_file(&test, n_points_ts, n_features_ts, points_ts);

    double t;
    for (i=0; i< n_points_ts; ++i){
      ord_inf informations;
      inf *dis = (inf *)malloc(k * sizeof(inf));
      informations.size = k;
      informations.n_elements = 0;
      for (j=0; j<n_points_tr; ++j){
        t = calculate_distance(points_ts[i], points_tr[j], n_features_ts);
        //printf("%lf, %d\n", t, points_tr[j].rot_class);
        //insert T ordenated in informations
        insert_ord_inf(&informations, dis,  t, points_tr[j].rot_class);
      }
      int r = find_class(k, dis);
      if(r==REJECTED){
        n_rejected++;
        points_ts[i].rejected = 1;
      }else{
       points_ts[i].freq_class = r;
       if(points_ts[i].freq_class == points_ts[i].rot_class)
         n_correct++;
        else
          n_error++;
      }
      free(dis);
    }
		double p_a = ((double)n_correct/(double)n_points_ts), 
					 p_e = ((double)n_error/(double)n_points_ts),
					 p_r = ((double)n_rejected/(double)n_points_ts);
		char p = '%';
    printf("Acertos: (%d/%d)=%.5lf%c, Erros: (%d/%d)=%.5lf%c, Rejeicao: (%d/%d)=%.5lf%c\n", 
						n_correct, n_points_ts, p_a, p,  n_error, n_points_ts,
						p_e, p, n_rejected, n_points_ts, p_r, p);
    confusion_matrix(points_ts, n_points_ts, n_points_tr);
    free(points_tr);
    free(points_ts);
    return 0;
}

int get_mat_index(int **m, int c, int size){
	for(int i=1; i<size; ++i){
		if(m[i][0]==c)
			return i;
	}
	return -1;
}

void confusion_matrix(point *points_ts, int n_points_ts, int n_points_tr){
  int *c = malloc((n_points_tr*2)*(sizeof(int))), n_c = 0, found = 0, i, j;
  for(i=0; i<n_points_ts; ++i){
    found = 0;
    for(j=0; j<n_c && (!found); ++j){
      if(c[j]==points_ts[i].rot_class)
        found = 1;
    }
    if(!found){
      c[n_c] = points_ts[i].rot_class;
      n_c++;
    }
    found = 0;
    for(j=0; j<n_c && (!found); ++j){
      if(c[j]==points_ts[i].freq_class)
        found = 1;
    }
    if(!found){
      c[n_c] = points_ts[i].freq_class;
      n_c++;
    }
  }
  sort_class_vet(c, n_c);
  int size = n_c+1;
  int **confusion_matrix = (int **)malloc(size*sizeof(int*));

  for(i=0; i<size; ++i){
    confusion_matrix[i] = (int *)calloc(size, sizeof(int));
  }
  confusion_matrix[0][0] = n_c;
  //preenche linha 0 e coluna 0
  for(i=1; i<size; ++i){
    confusion_matrix[0][i] = c[i-1];
    confusion_matrix[i][0] = c[i-1];
  }
  free(c);
  for(i=0; i<n_points_ts; ++i){
		if(!points_ts[i].rejected){
			int x = get_mat_index(confusion_matrix, points_ts[i].freq_class, size);
			int y = get_mat_index(confusion_matrix, points_ts[i].rot_class, size);
			confusion_matrix[y][x] = confusion_matrix[y][x]+1;
		}
	}
  printf("Matriz de confusao\n");
  for(i=0; i<size; ++i){
    for(j=0; j<size; ++j){
      printf("%d\t", confusion_matrix[i][j]);
    }
    printf("\n");
  }
  for(i=0; i<size; ++i){
    free(confusion_matrix[i]);
  }
					free(confusion_matrix);
  return;
}

void sort_class_vet(int *v, int size){
  int tmp;
  for(int i=0; i<size; ++i){
    for(int j=i+1; j<size; ++j){
     if(v[i]>v[j]){
       tmp = v[i];
       v[i] = v[j];
       v[j] = tmp;
      }
    }
  }
}

int find_class(int k, inf dis[]){
  c *aux = malloc(k * sizeof(c));
  int i, cont=0, found = 0, pos;
  for(i=0; i<k; ++i){
    aux[i].amount = 0;
  }
  aux[0].class_c = dis[0].rot_class;
  aux[0].amount = aux[0].amount+1;
  cont+=1;
  for(i=1; i<k; ++i){
    found = 0;
    for(int j=0; j<cont && (!found); ++j){
      if(aux[j].class_c == dis[i].rot_class){
        found = 1;
        pos = j;
      }
    }
    if(found)
      aux[pos].amount = aux[pos].amount+1;
    else{
      aux[cont].class_c = dis[i].rot_class;
      aux[cont].amount = aux[cont].amount+1;
      cont+=1;
    }
  }
  //test
  /*for(i=0; i<cont; ++i){
    printf("Class: %d, Amount %d\n", aux[i].class_c, aux[i].amount);
  }*/

  int pos_big = find_big(aux, cont);
  if(pos_big==REJECTED)
    return REJECTED;
  else
    return aux[pos_big].class_c;
}

int find_big(c vet[], int cont){
  int big = vet[0].amount, rej = 0, pos_big=0;
  for(int i=1; i<cont; ++i){
    if(vet[i].amount>big){
      big = vet[i].amount;
      pos_big = i;
      rej=0;
    }
		else{
    	if(vet[i].amount==big)
      	rej=1;
		}
  }
  if(rej)
    return REJECTED;
  return pos_big;
}
void insert_ord_inf(ord_inf *p, inf *dis, double distance, int rot_class){
  int i, j;
  inf aux;
  aux.distance = distance;
  aux.rot_class = rot_class;
  if(p->n_elements < p->size){
    for(i=0; i<p->n_elements && dis[i].distance<distance; ++i);
    inf aux1 = dis[i];
    dis[i].distance = distance;
    dis[i].rot_class = rot_class;
    p->n_elements = p->n_elements+1;

    for(j=i+1; j<p->n_elements; ++j){
      inf aux2 = dis[j];
      dis[j] = aux1;
      aux1 = aux2;
    }
  }
  else{
    for(i=0; i<p->size; ++i){
      if(dis[i].distance > aux.distance){
          inf aux2 = dis[i];
          dis[i].distance = aux.distance;
          dis[i].rot_class = aux.rot_class;
          aux = aux2;
      }
    }
  }
}

double calculate_distance(point p1, point p2, int n_features){
  double s = 0.0;
  double d;
  for(int i=0; i<n_features; ++i){
    d = p1.features[i] - p2.features[i];
    s+=(d*d);
  }
  return s;

}
int test_args(int argc, char *argv[], FILE **training, FILE **test, int *k){
  if(!(*training = fopen(argv[1], "r")))
    return -1;
  if(!(*test = fopen(argv[2], "r")))
    return -1;
  *k = atoi(argv[3]);
  return 1;
}

void read_first_line(FILE **file_in, int *n_points, int *n_features){
  if(!*file_in)
    exit(1);
  if(!fscanf(*file_in, "%d %d", n_points, n_features))
    exit(1);
  return;
}

void read_file(FILE **file_in, int n_points, int n_features, point *p){
  int i, j, w;
  if(!*file_in)
    exit(1);
  for(i=0; i<n_points; ++i){
    for(j=0; j<n_features; ++j){
        w = fscanf(*file_in, "%lf", &(p[i].features[j]));
    }
    w = fscanf(*file_in, "%d", &(p[i]).rot_class);
    p[i].rejected = 0;
  }
  if(w)
    return;
}
