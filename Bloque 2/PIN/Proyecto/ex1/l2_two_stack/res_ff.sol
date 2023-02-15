
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

Cueing down from goal distance:   14 into depth [1]
                                  11            [1][2]
                                  10            [1][2]
                                   9            [1][2][3][4][5]
                                   8            [1][2][3][4][5][6][7]
                                   7            [1]
                                   6            [1][2]
                                   5            [1][2][3][4][5][6]
                                   4            [1]
                                   3            [1]
                                   2            [1]
                                   1            [1]
                                   0            

ff: found legal plan as follows

step    0: UNSTACK C11 S13 A1 S13 L1 N1 N0
        1: UNSTACK C6 C8 A2 S21 L2 N3 N2
        2: STACKONCONTAINER_REGULAR C11 C10 A1 S12 L1 N2 N3 N4
        3: PLACEINRAIL L2 L1 A2 C6 R2
        4: TRANSPORT R2 C6 L2 L1
        5: UNSTACK C8 T4 A2 S21 L2 N2 N1
        6: PICKFROMRAIL R2 L1 L2 C6 A1
        7: PLACEINRAIL L1 L2 A1 C6 R1
        8: TRANSPORT R1 C6 L1 L2
        9: PLACEINRAIL L2 L1 A2 C8 R2
       10: PICKFROMRAIL R1 L2 L1 C6 A1
       11: STACKONCONTAINER_REGULAR C6 C11 A1 S12 L1 N3 N4 N4
       12: TRANSPORT R2 C8 L2 L1
       13: PICKFROMRAIL R2 L1 L2 C8 A1
       14: UNSTACK T4 S21 A2 S21 L2 N1 N0
       15: PLACEINRAIL L1 L2 A1 C8 R1
       16: PLACEINRAIL L2 L1 A2 T4 R2
       17: TRANSPORT R2 T4 L2 L1
       18: UNSTACK C2 T3 A2 S22 L2 N3 N2
       19: STACKONCONTAINER_REGULAR C2 S21 A2 S21 L2 N0 N1 N3
       20: PICKFROMRAIL R2 L1 L2 T4 A1
       21: TRANSPORT R1 C8 L1 L2
       22: PICKFROMRAIL R1 L2 L1 C8 A2
       23: STACKONCONTAINER_REGULAR C8 C2 A2 S21 L2 N1 N2 N3
       24: UNSTACK T3 C5 A2 S22 L2 N2 N1
       25: PLACEINRAIL L2 L1 A2 T3 R2
       26: TRANSPORT R2 T3 L2 L1
       27: STACKONCONTAINER_TARGET T4 T7 A1 S11 L1 N2 N3 N4
       28: PICKFROMRAIL R2 L1 L2 T3 A1
       29: STACKONCONTAINER_TARGET T3 T4 A1 S11 L1 N3 N4 N4
     

time spent:    0.00 seconds instantiating 26510 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 404 facts and 6424 actions
               0.00 seconds creating final representation with 397 relevant facts, 0 relevant fluents
               0.02 seconds computing LNF
               0.00 seconds building connectivity graph
               0.08 seconds searching, evaluating 384 states, to a max depth of 7
               0.10 seconds total time

