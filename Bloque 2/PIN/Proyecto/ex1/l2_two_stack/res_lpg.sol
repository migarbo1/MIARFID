

NUMERIC_THREATS_MODE: 0

; Command line: /home/miguel/Documentos/PIN/PLANIFICADORES/PLANIFICADOR LPG/lpg-td -o domain.pddl -f problem.pddl -n 2   


Parsing domain file:  domain 'PUERTO' defined ... done.
Parsing problem file:  problem 'P1' defined ... done.



Modality: Incremental Planner

Number of actions             :    9064
Number of conditional actions :       0
Number of facts               :     440


Analyzing Planning Problem:
	Temporal Planning Problem: NO
	Numeric Planning Problem: NO
	Problem with Timed Initial Literals: NO
	Problem with Derived Predicates: NO

Evaluation function weights:
     Action duration 0.00; Action cost 1.00


Computing mutex... done

Preprocessing total time: 0.39 seconds

Searching ('.' = every 50 search steps):
. solution found: 
 first_solution_cpu_time: 0.70 
Solution number: 1
Total time:      0.70
Search time:     0.31
Actions:         28
Duration:        25.000
Plan quality:    28.000 
Total Num Flips: 60
     Plan file:       plan_problem.pddl_1.SOL Restart using stored plan
........... search limit exceeded. Restart using stored plan
............. search limit exceeded. Restart using null plan
. solution found: 

Plan computed:
   Time: (ACTION) [action Duration; action Cost]
 0.0000: (UNSTACK C8 T4 A2 S21 L2 N2 N1) [D:1.00; C:1.00]
 1.0000: (STACKONCONTAINER_REGULAR C8 C6 A2 S23 L2 N1 N2 N3) [D:1.00; C:1.00]
 2.0000: (UNSTACK T4 S21 A2 S21 L2 N1 N0) [D:1.00; C:1.00]
 3.0000: (PLACEINRAIL L2 L1 A2 T4 R2) [D:1.00; C:1.00]
 4.0000: (TRANSPORT R2 T4 L2 L1) [D:1.00; C:1.00]
 4.0000: (UNSTACK C2 T3 A2 S22 L2 N3 N2) [D:1.00; C:1.00]
 5.0000: (PICKFROMRAIL R2 L1 L2 T4 A1) [D:1.00; C:1.00]
 5.0000: (STACKONCONTAINER_REGULAR C2 C8 A2 S23 L2 N2 N3 N3) [D:1.00; C:1.00]
 6.0000: (UNSTACK T3 C5 A2 S22 L2 N2 N1) [D:1.00; C:1.00]
 6.0000: (STACKONCONTAINER_TARGET T4 C11 A1 S13 L1 N1 N2 N3) [D:1.00; C:1.00]
 7.0000: (PLACEINRAIL L2 L1 A2 T3 R2) [D:1.00; C:1.00]
 8.0000: (TRANSPORT R2 T3 L2 L1) [D:1.00; C:1.00]
 9.0000: (PICKFROMRAIL R2 L1 L2 T3 A1) [D:1.00; C:1.00]
 10.0000: (STACKONCONTAINER_TARGET T3 T4 A1 S13 L1 N2 N3 N3) [D:1.00; C:1.00]


Solution number: 2
Total time:      23.04
Search time:     22.65
Actions:         14
Duration:        11.000
Plan quality:    14.000 
Total Num Flips: 1389
     Plan file:       plan_problem.pddl_2.SOL

