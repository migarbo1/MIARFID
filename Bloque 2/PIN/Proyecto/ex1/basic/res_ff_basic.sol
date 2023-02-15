
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
                                   7            [1][2][3]
                                   6            [1][2]
                                   5            [1][2][3]
                                   4            [1]
                                   3            [1]
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
        7: STACKONCONTAINER_REGULAR C2 C11 A1 S13 L1 N1 N2 N3
        8: PLACEINRAIL L2 L1 A2 T4 R2
        9: TRANSPORT R2 T4 L2 L1
       10: PICKFROMRAIL R2 L1 L2 T4 A1
       11: UNSTACK T3 C5 A2 S22 L2 N2 N1
       12: PLACEINRAIL L2 L1 A2 T3 R2
       13: TRANSPORT R2 T3 L2 L1
       14: STACKONCONTAINER_TARGET T4 C2 A1 S13 L1 N2 N3 N3
       15: PICKFROMRAIL R2 L1 L2 T3 A1
       16: STACKONCONTAINER_TARGET T3 C10 A1 S12 L1 N2 N3 N3
     

time spent:    0.00 seconds instantiating 27038 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 442 facts and 6820 actions
               0.00 seconds creating final representation with 434 relevant facts, 0 relevant fluents
               0.02 seconds computing LNF
               0.00 seconds building connectivity graph
               0.02 seconds searching, evaluating 43 states, to a max depth of 3
               0.04 seconds total time

