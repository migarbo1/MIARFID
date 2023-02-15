

NUMERIC_THREATS_MODE: 0

; Command line: /home/miguel/Documentos/PIN/PLANIFICADORES/PLANIFICADOR LPG/lpg-td -o domain.pddl -f problem.pddl -n 2   


Parsing domain file:  domain 'PUERTO' defined ... done.
Parsing problem file:  problem 'P1' defined ... done.



Modality: Incremental Planner

Number of actions             :   10464
Number of conditional actions :       0
Number of facts               :     484


Analyzing Planning Problem:
	Temporal Planning Problem: NO
	Numeric Planning Problem: NO
	Problem with Timed Initial Literals: NO
	Problem with Derived Predicates: NO

Evaluation function weights:
     Action duration 0.00; Action cost 1.00


Computing mutex... done

Preprocessing total time: 0.47 seconds

Searching ('.' = every 50 search steps):
........... search limit exceeded. Restart using null plan
............. search limit exceeded. Restart using null plan
............... search limit exceeded. Restart using null plan
.................. search limit exceeded. Restart using null plan
..................... search limit exceeded. Restart using null plan
........................ search limit exceeded. Restart using null plan
............................ search limit exceeded. Restart using null plan
..... solution found: 
 first_solution_cpu_time: 133.35 
Solution number: 1
Total time:      133.35
Search time:     132.88
Actions:         65
Duration:        60.000
Plan quality:    65.000 
Total Num Flips: 6863
     Plan file:       plan_problem.pddl_1.SOL Restart using stored plan
........... search limit exceeded.

Searching ('.' = every 50 search steps):
. solution found: 

Plan computed:
   Time: (ACTION) [action Duration; action Cost]
 0.0000: (UNSTACK C8 T4 A2 S21 L2 N2 N1) [D:1.00; C:1.00]
 1.0000: (PLACEINRAIL L2 L1 A2 C8 R2) [D:1.00; C:1.00]
 2.0000: (TRANSPORT R2 C8 L2 L1) [D:1.00; C:1.00]
 2.0000: (UNSTACK T4 S21 A2 S21 L2 N1 N0) [D:1.00; C:1.00]
 3.0000: (PICKFROMRAIL R2 L1 L2 C8 A1) [D:1.00; C:1.00]
 4.0000: (PLACEINRAIL L2 L1 A2 T4 R2) [D:1.00; C:1.00]
 4.0000: (STACKONCONTAINER_REGULAR C8 C10 A1 S12 L1 N2 N3 N3) [D:1.00; C:1.00]
 5.0000: (TRANSPORT R2 T4 L2 L1) [D:1.00; C:1.00]
 5.0000: (UNSTACK C2 T3 A2 S22 L2 N3 N2) [D:1.00; C:1.00]
 6.0000: (PICKFROMRAIL R2 L1 L2 T4 A1) [D:1.00; C:1.00]
 6.0000: (STACKONCONTAINER_REGULAR C2 S21 A2 S21 L2 N0 N1 N3) [D:1.00; C:1.00]
 7.0000: (UNSTACK T3 C5 A2 S22 L2 N2 N1) [D:1.00; C:1.00]
 7.0000: (STACKONCONTAINER_TARGET T4 T7 A1 S11 L1 N2 N3 N3) [D:1.00; C:1.00]
 8.0000: (PLACEINRAIL L2 L1 A2 T3 R2) [D:1.00; C:1.00]
 8.0000: (UNSTACK T4 T7 A1 S11 L1 N3 N2) [D:1.00; C:1.00]
 9.0000: (TRANSPORT R2 T3 L2 L1) [D:1.00; C:1.00]
 9.0000: (STACKONCONTAINER_TARGET T4 C11 A1 S13 L1 N1 N2 N3) [D:1.00; C:1.00]
 9.0000: (UNSTACK T12 C6 A2 S23 L2 N1 N0) [D:1.00; C:1.00]
 10.0000: (PICKFROMRAIL R2 L1 L2 T3 A1) [D:1.00; C:1.00]
 11.0000: (STACKONCONTAINER_TARGET T3 T7 A1 S11 L1 N2 N3 N3) [D:1.00; C:1.00]
 11.0000: (PLACEINRAIL L2 L1 A2 T12 R2) [D:1.00; C:1.00]
 12.0000: (TRANSPORT R2 T12 L2 L1) [D:1.00; C:1.00]
 13.0000: (PICKFROMRAIL R2 L1 L2 T12 A1) [D:1.00; C:1.00]
 14.0000: (STACKONCONTAINER_TARGET T12 T3 A1 S11 L1 N3 N4 N3) [D:1.00; C:1.00]


Solution number: 2
Total time:      174.33
Search time:     173.86
Actions:         24
Duration:        15.000
Plan quality:    24.000 
Total Num Flips: 7536
     Plan file:       plan_problem.pddl_2.SOL

