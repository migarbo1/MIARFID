
ff: parsing domain file
domain 'PUERTO' defined
 ... done.
ff: parsing problem file
problem 'P1' defined
 ... done.


no metric specified. plan length assumed.

checking for cyclic := effects --- OK.

ff: search configuration is EHC, if that fails then  best-first on 1*g(s) + 5*h(s) where
    metric is  plan length

Cueing down from goal distance:   12 into depth [1]
                                   9            [1][2]
                                   8            [1][2]
                                   7            [1][2][3][4]
                                   6            [1]
                                   5            [1][2][3][4][5][6][7][8][9][10]
                                   4            [1]
                                   3            [1][2][3][4][5][6][7][8] --- pruning stopped --- [1][2][3]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: UNSTACK C8 T4 A2 S21 L2 N2 N1
        1: STACKONCONTAINER_REGULAR C8 C6 A2 S23 L2 N1 N2 N3
        2: UNSTACK C2 T3 A2 S22 L2 N3 N2
        3: PLACEINRAIL L2 L1 A2 C2 R2
        4: TRANSPORT R2 C2 L2 L1
        5: PICKFROMRAIL R2 L1 L2 C2 A1
        6: UNSTACK T4 S21 A2 S21 L2 N1 N0
        7: PLACEINRAIL L2 L1 A2 T4 R2
        8: TRANSPORT R2 T4 L2 L1
        9: PLACEINRAIL L1 L2 A1 C2 R1
       10: PICKFROMRAIL R2 L1 L2 T4 A2
       11: STACKONCONTAINER_TARGET T4 T3 A2 S22 L2 N2 N3 N3
       12: TRANSPORT R1 C2 L1 L2
       13: PICKFROMRAIL R1 L2 L1 C2 A2
       14: STACKONCONTAINER_REGULAR C2 C8 A2 S23 L2 N2 N3 N3
       15: UNSTACK T4 T3 A2 S22 L2 N3 N2
       16: PLACEINRAIL L2 L1 A2 T4 R2
       17: PICKFROMRAIL R2 L1 L2 T4 A1
       18: UNSTACK T3 C5 A2 S22 L2 N2 N1
       19: PLACEINRAIL L2 L1 A2 T3 R2
       20: TRANSPORT R2 T3 L2 L1
       21: STACKONCONTAINER_TARGET T4 C11 A1 S13 L1 N1 N2 N2
       22: UNSTACK C10 C9 A1 S12 L1 N2 N1
       23: PLACEINRAIL L1 L2 A1 C10 R1
       24: PICKFROMRAIL R2 L1 L2 T3 A1
       25: STACKONCONTAINER_TARGET T3 C9 A1 S12 L1 N1 N2 N2
     

time spent:    0.00 seconds instantiating 31526 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 439 facts and 5698 actions
               0.00 seconds creating final representation with 431 relevant facts, 0 relevant fluents
               0.02 seconds computing LNF
               0.00 seconds building connectivity graph
               0.06 seconds searching, evaluating 288 states, to a max depth of 10
               0.08 seconds total time

