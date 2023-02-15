/*
* Copyright (C) 2022 Joan Andreu Sánchez <jandreu@dsic.upv.es>.
*
* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 3 of the License, or (at
* your option) any later version.
*
* This program is distributed in the hope that it will be useful, but
* WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
* General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <getopt.h>
#include <math.h>
#include <string.h>
#include <values.h> /* FLT_MAX */

#define MAXMOD 1                   /* Maximum number of models */
#define EPSILON 0.00001 /* Smooth values of the emission probs. */
#define MAXSAMPLES 40000

#define MAXCAD 16384
#define MAXTRELLIS 1024

typedef struct _nodeHash {
  char *c;
  int n;
  struct _nodeHash *next;
} nodeHash;

typedef struct _HMM{
  int nest, neti;
  double *pi;
  double **a;
  double **b;
  nodeHash **labels;
  int tableSize;
} HMM;

typedef struct _setOfSamples {
  int **s,                                  /* Set of samples */
    *sSize,                            /* Size of each sample */
    n;                                   /* Number of samples */
} setOfSamples;

/***************************************************************/
/********* GLOBAL VARIABLES  ***********************************/
/***************************************************************/
float eps2;           /* Smooth value for emission probabilities */
setOfSamples *samples;
int verbosidad;
double smooth;

/***************************************************************/
void printMatDouble(double **m, int f, int c) {
  int i,j;

  for (i=0; i<=f; i++) {
    fprintf(stderr,"%d-> ",i);
    for (j=0; j<=c; j++)
      fprintf(stderr,"%e ",m[i][j]);
    fprintf(stderr,"\n");
  }
}

/***************************************************************/
void printMatInt(double **m, int f, int c) {
  int i,j;

  for (i=0; i<=f; i++) {
    fprintf(stderr,"%d-> ",i);
    for (j=0; j<=c; j++)
      fprintf(stderr,"%2d ", (int)m[i][j]);
    fprintf(stderr,"\n");
  }
}

/***************************************************************/
void printMat(double **m, int f, int c) {
  int i,j;

  for (i=0; i<=f; i++) {
    fprintf(stderr,"%d-> ",i);
    for (j=0; j<=c; j++)
      fprintf(stderr,"%.6f ",m[i][j]);
    fprintf(stderr,"\n");
  }
}

/***************************************************************/
double ** CreateMat(int f, int c) {
   int i; 
  double **a, *aux;

  if ((a = (double **) malloc(f * sizeof(double *))) == NULL) 
    return NULL;
  if ((aux = (double *) malloc(f * c * sizeof(double))) == NULL) 
    return NULL;
  for (i=0; i<f; i++)
    a[i] = &(aux[i*c]);

  return a;
}

/***************************************************************/
void freeMat(double **a) {
  if (&(a[0][0]) != NULL) {
    free(&(a[0][0]));
    free(&(a[0]));
  }
}

/***************************************************************/
int isInHashTab(char *str, int j, nodeHash **labels, int tableSize) {
#define A 0.61803398874989484820 /* (sqrt(5) - 1) / 2 */
  
  double val, base;
  unsigned int pos;
  char *straux;
  nodeHash * head;

  /* A = (sqrt(5) -1) / 2; */
  val = 0;
  base = 1;
  straux = str;
  while (*straux != '\0') {
    val += base * (*straux);
    base *= 2;
    straux++;
  }
  pos = (unsigned int) floor(tableSize * modf(val * A, &base));
  head = labels[pos];
  while ((head != NULL) && (strcmp(str, head->c) != 0))
    head = head->next;

  if (head == NULL) {
    head = (nodeHash *)malloc(sizeof(nodeHash));
    head->c = (char *)malloc((strlen(str)+1) * sizeof(char));
    strcpy(head->c, str);
    head->n = j;
    head->next = labels[pos];
    labels[pos] = head;
  }
  return(head->n);
}

/***************************************************************/
HMM * readModel(char *filemod) {
  FILE *fmod;
  int i, j, states, nLabels;
  char str1[MAXCAD], *straux, str2[MAXCAD];
  HMM *mod;
  
  if ((fmod = fopen(filemod,"r")) == NULL)
    {fprintf(stderr,"(00) "); return NULL;}
  mod = (HMM *)malloc(sizeof(HMM));
  mod->tableSize = 30001;
  if ((mod->labels=(nodeHash**)malloc(mod->tableSize * sizeof(nodeHash*))) == NULL)
    {fprintf(stderr,"(03) "); return NULL;}
  for (i=0; i<mod->tableSize; i++)
    mod->labels[i] = NULL;

  if(fgets(str1,MAXCAD,fmod) == NULL) {
    fprintf(stderr,"Error: incorrect format in the first line (00).\n");
    return NULL;
  }
  
  if (strncmp(str1,"HMM",4) == 0) {
    fprintf(stderr,"Error: expected HMM.\n");
    return NULL;
  }

  if (sscanf(str1,"%s %d %d",
	     str2,&states,&nLabels) != 3) {
    fprintf(stderr,"Error: incorrect format in the first line (01).\n");
    return NULL;
  }

  mod->neti = nLabels;
  mod->nest = states;
  mod->pi =  (double *) malloc((states-1) * sizeof(double));
  mod->a = CreateMat(states - 1, states);
  mod->b = CreateMat(states, nLabels);

  if (fgets(str1, MAXCAD, fmod) == NULL) {/*Read probability of initial state*/ 
    fprintf(stderr,"Error: incorrect format in initial probability.\n");
    return NULL;
  }
  str1[strlen(str1)-1] = '\0';
  j=0;
  straux = strtok(str1," ");
  while ((j < states) && (straux != NULL)) {
    mod->pi[j] =  atof(straux);
    straux = strtok(NULL," ");
    j++;
  }
  if (j != states-1) {
    fprintf(stderr,"Error: incorrect state number.\n");
    return NULL;
  }
  i=0;
  while (i<states-1) { /* Read transition matrix */
    if (fgets(str1,MAXCAD,fmod) == NULL) {
      fprintf(stderr,"Error: problems reading transition matrix.\n");
      return NULL;
    }
    j=0;
    straux = strtok(str1," ");
    while ((j < states) && (straux != NULL)) {
      mod->a[i][j] = atof(straux);
      straux = strtok(NULL," ");
      j++;
    }
    if (j != states)
      {fprintf(stderr,"(06) "); return NULL;}
    i++;
  }
  i=0;
  while (i < nLabels) { /* Read emision matrix */
    if (fgets(str1,MAXCAD,fmod)== NULL) {
      fprintf(stderr,"Error: not enough emission probabilities.\n");
      return NULL;
    }
    str1[strlen(str1)-1] = '\0';
    j = 0;
    straux = strtok(str1," ");
    while ((j < states) && (straux != NULL)) {
      mod->b[j][i] = atof(straux);
      straux = strtok(NULL," ");
      j++;
    }
    if (j != states) {
      fprintf(stderr,"Error: not enough emission probabilities in state.\n");
      return NULL;
    }
    mod->b[states-1][i] = 0.0;
    j = isInHashTab(straux, i, mod->labels, mod->tableSize);
    i++;
  }
  if (fgets(str1,MAXCAD,fmod) == NULL)
    {fprintf(stderr,"(07) "); return NULL;}

  fclose(fmod);
  return mod;
}

/***************************************************************/
void writeModel(char *filemod, HMM *mod) {
  FILE *fmod;
  int i, j, k, cont0;
  double n1;
  char **Vocab;
  nodeHash *node;
  
  fmod = fopen(filemod,"w");
  fprintf(fmod,"HMM %d %d\n", mod->nest, mod->neti);
  for (i=0; i<mod->nest - 2; i++) /*Write initial probs*/
    fprintf(fmod,"%.6f ", mod->pi[i]);
  fprintf(fmod,"%.6f\n", mod->pi[mod->nest - 2]);

  for (i=0; i<mod->nest - 1; i++) { /*Write transit. probs*/
    for (j=0; j< mod->nest - 1; j++)
      fprintf(fmod,"%.6f ", mod->a[i][j]);
    fprintf(fmod,"%e\n", mod->a[i][mod->nest-1]);
  }
  
  Vocab = (char **)malloc(mod->neti * sizeof(char *));
  
  for (k=0; k<mod->tableSize; k++)
    for (node=mod->labels[k]; node!=NULL; node=node->next)
      Vocab[node->n] = node->c;

  if (smooth != 0.0)
    for (i=0; i<mod->nest-1; i++) {
      n1 = smooth;
      cont0 = 0;
      for (j=0; j<mod->neti; j++)
	if (mod->b[i][j] != 0.0) n1 += mod->b[i][j];
	else                     cont0++;
      if (n1 != 0.0)
	for (j=0; j<mod->neti; j++)
	  if (mod->b[i][j] == 0.0) mod->b[i][j] = smooth / cont0 / n1;
	  else                     mod->b[i][j] = mod->b[i][j] / n1;
      else
	fprintf(stderr,"Warning: detected not emiting state: %d.\n",i);
    }
  
  for (i=0; i<mod->neti; i++) { /*Write emis. probs*/
    for (j=0; j<mod->nest; j++)
      if  (smooth == 0.0)
	fprintf(fmod,"%.6f ",mod->b[j][i]);
      else
	fprintf(fmod,"%e ",mod->b[j][i]);
    fprintf(fmod,"%s\n",Vocab[i]);
  }
  fprintf(fmod,"\n");
  fclose(fmod);
}

/***************************************************************/
void alfa_proc(double **alfa, int *sample, int l, HMM *mod) {
  int t, ant, est, i;
 
  est = mod->nest;
  for (i=0; i<est-1; i++)
    alfa[i][0] = mod->pi[i] * mod->b[i][sample[0]];
  alfa[est-1][0] = 0.0;
  
  for (t=1; t<l; t++) 
    for (i=0; i<est-1; i++)
      for (ant=0; ant<est-1; ant++) 
	alfa[i][t] += alfa[ant][t-1] * mod->a[ant][i] *  mod->b[i][sample[t]];

  for (i=0; i<est-1; i++)
    alfa[est-1][l] += alfa[i][l-1] * mod->a[i][est-1];
}

/***************************************************************/
void initialize(double **a, int f, int c) {
  int i, j;
  
  for (i=0; i<f; i++) 
    for (j=0; j<c; j++)
      a[i][j] = 0.0;
}

/***************************************************************/
void initCounts(double **gamma1, double **gamma2, HMM *mod) {
  initialize(gamma1, mod->nest - 1,  mod->nest);
  initialize(gamma2, mod->nest - 1,  mod->neti);
}

/***************************************************************/
void beta_proc(double **beta, int *sample, int l, HMM *mod) {
  int t, ant, est, i;
  
  est = mod->nest;
  
  beta[est-1][l] = 1.0;

  for (ant=0; ant<est-1; ant++)
    beta[ant][l-1] = mod->a[ant][est-1];

  for (t=l-2; t>=0; t--) {
    for (i=0; i<est; i++)
      for (ant=0; ant < est-1; ant++)
	beta[ant][t] +=   mod->a[ant][i] *  mod->b[i][sample[t+1]] * beta[i][t+1];
  }
}

/***************************************************/
void viterbi(double **alfa, double **path, int *sample, int l, HMM *mod) {
  int t, est, ant, i;
  double aux;
  
  est = mod->nest;
  for (i=0; i<est-1; i++)
    alfa[i][0] = mod->pi[i] * mod->b[i][sample[0]];
  alfa[est-1][0] = 0.0;

  for (t=1; t<l; t++) 
    for (i=0; i<est-1; i++) {
      path[i][t] = -1;
      for (ant=0; ant<est-1; ant++)
	if ((aux= alfa[ant][t-1] * mod->a[ant][i] * mod->b[i][sample[t]]) > alfa[i][t]) {
	  alfa[i][t] = aux;
	  path[i][t] = ant;
	}      
    }

  for (i=0; i<est-1; i++)
    if ((aux= alfa[i][t-1] * mod->a[i][est-1]) > alfa[est-1][l]) {
      alfa[est-1][l] = aux;
      path[est-1][l] = i;
    }
}

/***************************************************/
void viterbiLearning(double **alfa, double **path, 
		     double **gamma1, double **gamma2, double *gamma3,
		     int *sample, int l, HMM *mod) {
  int t, ant, est, actual;
  
  initialize(alfa, mod->nest, l+1);
  initialize(path, mod->nest, l+1);
  viterbi(alfa, path, sample, l, mod);
  
  est =  mod->nest;
  ant = path[est-1][l];
  if (ant != -1) {
    gamma1[ant][est-1]++;
    actual = ant;
    for (t=l-1; t>0; t--) {
      gamma2[actual][sample[t]]++;
      ant = path[actual][t];
      gamma1[ant][actual]++;
      actual = ant;
     }
    gamma2[actual][sample[0]]++;
    gamma3[actual]++;
  }
}
 
/***************************************************************/
/* Acumulate the denominator and numerator for each sample     */
/***************************************************************/
void compute_freq(double **alfa, double **beta, 
		  double **gamma1, double **gamma2, double *gamma3,
                  int *sample, int l, HMM *mod) {
  int est, i, j, t, simb;
  double sampleProb, aux;

  est = mod->nest;

  sampleProb = alfa[est-1][l];

  for (i=0; i<est-1; i++) {
    for (j=0; j<est-1; j++) {
      aux = 0.0;
      for (t=0; t<l-1; t++)
	aux += alfa[i][t] * mod->a[i][j] * mod->b[j][sample[t+1]] * beta[j][t+1];
      aux = aux / sampleProb;      
      gamma1[i][j] += aux;
    }
  }

  /* printMat(alfa, est-1, l);fprintf(stdout,"\n");
     printMat(beta, est-1, l);fprintf(stdout,"\n"); */
  
  for (i=0; i<est-1; i++)
    gamma1[i][est-1] += alfa[i][l-1] * mod->a[i][est-1]  / sampleProb;

  /* printMat(gamma1, est-1, est-1);   exit(-1); */
  
  for (i=0; i<est-1; i++) {
    for (simb=0; simb<mod->neti; simb++) {
      aux = 0.0;
      for (t=0; t<l; t++)
	if (sample[t] == simb)
          aux += alfa[i][t] * beta[i][t];
      aux = aux / sampleProb;
      gamma2[i][simb] += aux; 
    }    
    gamma3[i] += alfa[i][0] * beta[i][0] / sampleProb;
  }

  /* printMat(gamma1, est-2, est-1); exit(-1); */
}

/***************************************************************/
void estimate(double **gamma1, double **gamma2, double *gamma3, HMM *mod) {
  int i, j, est;
  double n1;
  
  est = mod->nest;
   
  for (i=0; i<est-1; i++) {
    n1 = 0.0;
    for (j=0; j<est; j++) n1 += gamma1[i][j];
    if (n1 != 0.0) for (j=0; j<est; j++) mod->a[i][j] = gamma1[i][j] / n1;
  }

  /*printMat(gamma1, est-2, est-1); fprintf(stdout,"\n");
    printMat(mod->a, est-2, est-1); exit(-1);*/
  
  for (i=0; i<est-1; i++) {
    n1=0.0;
    for (j=0; j<mod->neti; j++) n1 += gamma2[i][j];
    if (n1 != 0.0) for (j=0; j<mod->neti; j++) mod->b[i][j] = gamma2[i][j] / n1;
    else           for (j=0; j<mod->neti; j++) mod->b[i][j] = 0.0;
  }
  n1=0.0;
  for (i=0; i<est-1; i++) n1+=gamma3[i];
  for (i=0; i<est-1; i++) mod->pi[i] = gamma3[i] / n1;
}

/***************************************************************/
void learn(HMM *mod, int baum, int ite, int mSize) {
  int longSample, est, s, i, nSamplesUsed;
  double VeroAct, PrCad;
  double **gamma1=NULL, **gamma2=NULL, **alfa=NULL, **beta=NULL,
    *gamma3=NULL;
  
  est = mod->nest;

  gamma1 = CreateMat(est,est+1);
  gamma2 = CreateMat(est,mod->neti);
  gamma3 = (double *)malloc(est*sizeof(double)); /* initial state */
  alfa = CreateMat(est+1, MAXTRELLIS);
  beta = CreateMat(est+1, MAXTRELLIS);

  VeroAct = 0.0;
  do {
    VeroAct = 0.0;
    nSamplesUsed = 0;
    
    initCounts(gamma1, gamma2, mod);
    for (i=0; i<est; i++) gamma3[i] = 0.0;
    
    for (s=0; s<samples->n; s++){
      longSample = samples->sSize[s];
      if (verbosidad >= 3) fprintf(stderr,"%d\n",s);
      if (longSample <= mSize) {
	initialize(alfa, est+1, longSample+1);
	initialize(beta, est+1, longSample+1);
	if (baum == 0) {
	  alfa_proc(alfa, samples->s[s], longSample, mod);
	  beta_proc(beta, samples->s[s], longSample, mod);
	  PrCad = alfa[est-1][longSample];
	  /* fprintf(stdout," %e",PrCad); */
	  if (PrCad != 0.0) {
	    compute_freq(alfa,beta,gamma1,gamma2,gamma3,
			 samples->s[s],
			 longSample,mod);
	    VeroAct = VeroAct + log(alfa[est-1][longSample]);
	    nSamplesUsed++;
	  }
	  else
	    fprintf(stderr,
		    "Warning: sample %d of length %d not accepted.\n",
		    s, longSample);
	}
	else {
	  viterbiLearning(alfa,beta,gamma1,gamma2,gamma3,
		  samples->s[s],longSample,mod);
	  PrCad = alfa[est-1][longSample];
	  if (PrCad != 0.0) {
	    VeroAct = VeroAct + log(alfa[est-1][longSample]);
	    nSamplesUsed++;
	  }
	  else
	    fprintf(stderr,
		    "Warning: sample %d of length %d not accepted.\n",
		    s, longSample);
	}
      }
    }
    estimate(gamma1, gamma2, gamma3, mod);
    fprintf(stdout,"\t%e %d\n", VeroAct/nSamplesUsed, nSamplesUsed);
    ite--;
  } while (ite>0);

  freeMat(gamma1);
  freeMat(gamma2);
  freeMat(alfa);
  freeMat(beta);
  free(gamma3);
}
 

/***************************************************************/
void viterbiDecoding(int *s, int l, HMM *mod, char **Vocab) {
#define MAXEST 50
  int est, ant, stack[MAXTRELLIS], tS=0, actual, t;
  double **alfa=NULL, **path=NULL;
  
  alfa = CreateMat(MAXEST, MAXTRELLIS);
  path = CreateMat(MAXEST, MAXTRELLIS);
  initialize(alfa, mod->nest, l+1);
  initialize(path, mod->nest, l+1);

  viterbi(alfa, path, s, l, mod);

  /* printMat(alfa, mod->nest-1, l); 
  printMatInt(path, mod->nest-1, l);  exit(-1); */

  if (alfa[mod->nest - 1][l] != 0.0) {
    est =  mod->nest;
    ant = path[est-1][l];
    if (ant != -1) {
      stack[tS++] = est;
      actual = ant;
      for (t=l-1; t>0; t--) {
	stack[tS++] = actual;
	ant = path[actual][t];
	actual = ant;
      }
      stack[tS++] = actual;
    }
    for (tS--; tS>0; tS--)
      fprintf(stdout," %s@%d",Vocab[s[l-tS]],stack[tS]);
    fprintf(stdout,"\n");
  }
  else
    fprintf(stderr,"Warning: sample not accepted.\n");

  freeMat(alfa);
  freeMat(path);  
}

/***************************************************************/
 setOfSamples * readSamples(char *sampleFile, HMM *mod) {
  setOfSamples *sa;
  int i, j, k, l;
  int vaux[MAXTRELLIS];
  FILE *fd;
  char cad1[MAXCAD], *cad3;

  if ((sa = (setOfSamples *)malloc(sizeof(setOfSamples))) == NULL)
    return NULL;
  if ((sa->s = (int **)malloc(MAXSAMPLES * sizeof (int *))) == NULL)
    return NULL;
  if ((sa->sSize = (int *)malloc(MAXSAMPLES * sizeof(int))) == NULL)
    return NULL;
  sa->n = 0;
  
  if (strcmp(sampleFile,"") != 0) {
    if ((fd = fopen(sampleFile,"r")) == NULL)
      return NULL;
  }
  else
    fd = stdin;

  i=0;
  while (fgets(cad1, MAXCAD, fd) != NULL) {
    cad1[strlen(cad1)-1] = '\0';
    cad3 = (char *) strtok(cad1," ");   
    j = 0;
    while (cad3 != NULL) {
      k = isInHashTab(cad3, -1, mod->labels, mod->tableSize);
      if (k == -1) {
	fprintf(stderr,"Warning: %s => UNK.\n",cad3);
	return NULL;
      }
      
      vaux[j] = k;
      j++;
      if (j==MAXTRELLIS) {
	fprintf(stderr,"Error: increase trellis size.\n");
	return NULL;
      }
      cad3 = (char *) strtok(NULL," ");
    }
    if ((sa->s[i] = (int *)malloc(j * sizeof(int))) == NULL)
      return NULL;
    for (l=0; l<j; l++)
      sa->s[i][l] = vaux[l];
    sa->sSize[i] = j;
    i++;
  }
  sa->n = i;
  return sa; 
}


/***************************************************************/
void sintaxis(char *comando) {
  fprintf(stdout,"\nUsage: %s [-h] -i mI",comando);
  fprintf(stdout," [-S sF] [-l sZ]");
  fprintf(stdout," [[-v] [-o mO] [-I ite] [-s sm]] | [-D]] [-V n]\n\n");
  fprintf(stdout,"\t-i mI\tinput model file\n");
  fprintf(stdout,"\t-S sF\tsample file (stdin by default)\n");
  fprintf(stdout,"\t-l sZ\tuse strings up to length sZ (60 by default)\n");
  fprintf(stdout,"\t-v\tViterbi learning (Bawm-Welch by default)\n");
  fprintf(stdout,"\t-o mO\toutput model file (mI by default)\n");
  fprintf(stdout,"\t-I ite\tnumber of traing iterations (1 by default)\n");
  fprintf(stdout,"\t-s sm\tsmooth value for emission probabilities (float, not by default)\n");
  fprintf(stdout,"\t-D\tdecoding (useless in training mode)\n");
  fprintf(stdout,"\t-V n\tverbosity level (0 by default, 3 max)\n");
  fprintf(stdout,"\t-h\tthis help\n\n");
  fprintf(stdout,"If option -D is used, then options -v, -o, and -I");
    fprintf(stdout," are ignored.\n\n");
  exit(-1);
}

/***************************************************************/
/***************************************************************/
int main(int argc,char *argv[]) {
  extern char *optarg;
  extern int opterr;

  HMM *mod = NULL;
  char sampleFile[MAXCAD], Modin[MAXCAD], Modout[MAXCAD], **Vocab;
  int option, baum=0, s, ite=1, mSize = 60, decoding=0, i;
  nodeHash *node;

  strcpy(sampleFile,"");
  strcpy(Modin,"");
  strcpy(Modout,"");
  smooth = 0.0;
  
  if (argc == 1) sintaxis(argv[0]);
  while ((option=getopt(argc,argv,"hi:vo:S:s:I:l:DV:")) != EOF ) {
    switch(option) {
    case 'i': strcpy(Modin,optarg);strcpy(Modout,optarg);break;
    case 'o': strcpy(Modout,optarg);break;
    case 'S': strcpy(sampleFile,optarg);break;
    case 's': smooth = (double) atof(optarg);break;
    case 'v': baum = 1;break;
    case 'I': ite = atoi(optarg);break;
    case 'V': verbosidad = atoi(optarg);break;
    case 'l': mSize = atoi(optarg);break;
    case 'D': decoding = 1;break;
    case 'h': sintaxis(argv[0]);
    default: sintaxis(argv[0]);
    }
  }

  if ((mod = readModel(Modin)) == NULL) {
    fprintf(stderr,"Error: incorrect model format.\n");
    return -1;
  }

  if ((samples = readSamples(sampleFile, mod)) == NULL) {
    fprintf(stderr,"Error: incorrect sample format.\n");
    return -1;
  }

  if (decoding==0) { 
    learn(mod, baum, ite, mSize);
    writeModel(Modout, mod);
  }
  else {
    Vocab = (char **)malloc(mod->neti * sizeof(char *));
    for (i=0; i<mod->tableSize; i++)
      for (node=mod->labels[i]; node!=NULL; node=node->next)
	Vocab[node->n] = node->c;

    for (s=0; s<samples->n; s++)
      viterbiDecoding(samples->s[s], samples->sSize[s], mod, Vocab);
  }
  return 0;
}
