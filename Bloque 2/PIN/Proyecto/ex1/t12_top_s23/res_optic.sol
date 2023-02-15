Number of literals: 486
Constructing lookup tables: [10%] [20%] [30%] [40%] [50%] [60%] [70%] [80%] [90%] [100%]
Post filtering unreachable actions:  [10%] [20%] [30%] [40%] [50%] [60%] [70%] [80%] [90%] [100%]
[01;34mNo analytic limits found, not considering limit effects of goal-only operators[00m
Initial heuristic = 19.000, admissible cost estimate 0.000
b (17.000 | 0.000)b (14.000 | 0.001)b (11.000 | 0.002)b (10.000 | 0.004)b (8.000 | 0.006)b (7.000 | 0.008)b (6.000 | 0.009)b (5.000 | 0.009)b (4.000 | 0.010)b (1.000 | 0.011)(G)
; No metric specified - using makespan

; Plan found with metric 0.012
; States evaluated so far: 136
; States pruned based on pre-heuristic cost lower bound: 0
; Time 1.04
0.000: (unstack t12 c6 a2 s23 l2 n1 n0)  [0.001]
0.001: (placeinrail l2 l1 a2 t12 r2)  [0.001]
0.002: (transport r2 t12 l2 l1)  [0.001]
0.002: (unstack c8 t4 a2 s21 l2 n2 n1)  [0.001]
0.003: (pickfromrail r2 l1 l2 t12 a1)  [0.001]
0.003: (stackoncontainer_regular c8 c6 a2 s23 l2 n0 n1 n3)  [0.001]
0.004: (unstack t4 s21 a2 s21 l2 n1 n0)  [0.001]
0.005: (placeinrail l2 l1 a2 t4 r2)  [0.001]
0.006: (stackoncontainer_target t12 c11 a1 s13 l1 n1 n2 n3)  [0.001]
0.006: (transport r2 t4 l2 l1)  [0.001]
0.006: (unstack c2 t3 a2 s22 l2 n3 n2)  [0.001]
0.007: (stackoncontainer_regular c2 s21 a2 s21 l2 n0 n1 n3)  [0.001]
0.007: (pickfromrail r2 l1 l2 t4 a1)  [0.001]
0.008: (unstack t3 c5 a2 s22 l2 n2 n1)  [0.001]
0.009: (placeinrail l2 l1 a2 t3 r2)  [0.001]
0.010: (stackoncontainer_target t4 t7 a1 s11 l1 n2 n3 n3)  [0.001]
0.010: (transport r2 t3 l2 l1)  [0.001]
0.011: (pickfromrail r2 l1 l2 t3 a1)  [0.001]
0.012: (stackoncontainer_target t3 c10 a1 s12 l1 n2 n3 n3)  [0.001]