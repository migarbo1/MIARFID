Number of literals: 442
Constructing lookup tables: [10%] [20%] [30%] [40%] [50%] [60%] [70%] [80%] [90%] [100%]
Post filtering unreachable actions:  [10%] [20%] [30%] [40%] [50%] [60%] [70%] [80%] [90%] [100%]
[01;34mNo analytic limits found, not considering limit effects of goal-only operators[00m
Initial heuristic = 13.000, admissible cost estimate 0.000
b (12.000 | 0.000)b (11.000 | 0.002)b (10.000 | 0.003)b (9.000 | 0.005)b (7.000 | 0.008)b (6.000 | 0.012)
Resorting to best-first search
Running WA* with W = 5.000, not restarting with goal states
b (11.000 | 0.000)b (10.000 | 0.001)b (9.000 | 0.003)b (7.000 | 0.004)b (6.000 | 0.006)b (5.000 | 0.007)b (4.000 | 0.008)b (4.000 | 0.007)b (3.000 | 0.008)b (1.000 | 0.009)(G)
; No metric specified - using makespan

; Plan found with metric 0.010
; States evaluated so far: 513
; States pruned based on pre-heuristic cost lower bound: 0
; Time 2.86
0.000: (unstack c8 t4 a2 s21 l2 n2 n1)  [0.001]
0.000: (unstack t7 c1 a1 s11 l1 n2 n1)  [0.001]
0.001: (stackoncontainer_target t7 c11 a1 s13 l1 n1 n2 n3)  [0.001]
0.001: (stackoncontainer_regular c8 c6 a2 s23 l2 n1 n2 n3)  [0.001]
0.002: (unstack c10 c9 a1 s12 l1 n2 n1)  [0.001]
0.002: (unstack t4 s21 a2 s21 l2 n1 n0)  [0.001]
0.003: (stackoncontainer_regular c10 c1 a1 s11 l1 n1 n2 n3)  [0.001]
0.003: (placeinrail l2 l1 a2 t4 r2)  [0.001]
0.004: (unstack c2 t3 a2 s22 l2 n3 n2)  [0.001]
0.004: (unstack c10 c1 a1 s11 l1 n2 n1)  [0.001]
0.005: (transport r2 t4 l2 l1)  [0.001]
0.005: (stackoncontainer_regular c2 s21 a2 s21 l2 n0 n1 n3)  [0.001]
0.005: (stackoncontainer_regular c10 c9 a1 s12 l1 n1 n2 n3)  [0.001]
0.006: (pickfromrail r2 l1 l2 t4 a1)  [0.001]
0.006: (unstack t3 c5 a2 s22 l2 n2 n1)  [0.001]
0.007: (placeinrail l2 l1 a2 t3 r2)  [0.001]
0.007: (stackoncontainer_target t4 c1 a1 s11 l1 n1 n2 n3)  [0.001]
0.008: (transport r2 t3 l2 l1)  [0.001]
0.009: (pickfromrail r2 l1 l2 t3 a1)  [0.001]
0.010: (stackoncontainer_target t3 t4 a1 s11 l1 n2 n3 n3)  [0.001]