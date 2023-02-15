#!/bin/bash

if [ $# -eq 0 ]
then
  echo ""
  echo "Usage: $0 hmm"
  echo ""
  exit
fi

awk  '
BEGIN {
  printf("digraph hmm {\n");
  printf("  rankdir=LR;\n");
}
{
  if (NR == 1) {
    nC = split($0,a);
    nState = a[2];
  }
  else if (NR == 2) {
    nC = split($0,a);
    printf("  node [shape=doublecircle];")

    for (i=1; i<=nC; i++)
      if (a[i] > 0.0) 
        printf(" %d",i-1);
    printf("\n  node [shape=circle];\n");     
  } else if (NR > 2 && NR <= nState+1) {
    nC = split($0,a);
    for (i=1; i<=nC; i++)
      if (a[i] > 0.0)
        printf("  %d -> %d [ label = %1.3f ];\n",NR-3,i-1,a[i]);
  }
}
END{
  printf("}");
}' $1
