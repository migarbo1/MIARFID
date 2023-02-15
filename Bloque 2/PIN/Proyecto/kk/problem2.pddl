(define (problem p1)
    (:domain puerto)
    (:objects
		;;loc 1
		l1 - location
		a1 - arm
		r1 - rail

		s11 - stack
		t7 - target
		c1 - regular
		
		s12 - stack
		c10 - regular 
		c9 - regular
            
		s13 - stack
		c11 - regular 

		;;loc 2
		l2 - location
		a2 - arm
		r2 - rail

		s21 - stack
		c8 - regular
		t4 - target
		
		s22 - stack
		c2 - regular
		t3 - target
		c5 - regular
            
		s23 - stack
		c6 - regular

		n0 - num
		n1 - num
		n2 - num
		n3 - num
		n4 - num
	)
	(:init
		(next n0 n1)
		(next n1 n2)
		(next n2 n3)
		(next n3 n4)

		;;Location 1
		;;containers at location
		(at t7 l1)
		(at c1 l1)
		(at c10 l1)
		(at c9 l1)
		(at c11 l1)

		;;stacks at location
		(at s11 l1)
		(at s12 l1)
		(at s13 l1)

		;;arm at location
		(at a1 l1)

		;;rail at location
		(at r1 l1)

		;;count for rails
		(actual s11 n2)
		(actual s12 n2)
		(actual s13 n1)

		;;max height for location 1
		(max_height l1 n2)

		;;free rail1
		(free r1)

		;;free arm1
		(free a1)

		;;orientation rail1
		(to r1 l2)

		;;container states location 1
		(available t7)
		(clear t7)
		(top t7 s11)
		(in t7 s11)
		(on t7 c1)
		(in c1 s11)
		(on c1 s11)

		(clear c10)
		(top c10 s12)
		(in c10 s12)
		(on c10 c9)
		(in c9 s12)
		(on c9 s12)

		(clear c11)
		(top c11 s13)
		(in c11 s13)
		(on c11 s13)

		;;containers identity
		(is_target t7)
		(is_regular c1)
		(is_regular c10)
		(is_regular c9)	
		(is_regular c11)

;		;Location 2
		;;containers at location 2
		(at c8 l2)
		(at t4 l2)
		(at c2 l2)
		(at t3 l2)
		(at c5 l2)
		(at c6 l2)

		;;stacks at location
		(at s21 l2)
		(at s22 l2)
		(at s23 l2)

		;;arm at location
		(at a2 l2)

		;;rail at location
		(at r2 l2)

		;;count for rails
		(actual s21 n2)
		(actual s22 n3)
		(actual s23 n1)

		;;max height for location 1
		(max_height l2 n3)

		;;free rail1
		(free r2)

		;;free arm1
		(free a2)

		;;orientation rail1
		(to r2 l1)

		;;container states location 1
		(clear c8)
		(top c8 s21)
		(in c8 s21)
		(on c8 t4)
		(in t4 s21)
		(on t4 s21)

		(clear c2)
		(top c2 s22)
		(in c2 s22)
		(on c2 t3)
		(in t3 s22)
		(on t3 c5)
		(in c5 s22)
		(on c5 s22)

		(clear c6)
		(top c6 s23)
		(in c6 s23)
		(on c6 s23)

		;;containers identity
		(is_target t4)
		(is_target t3)
		(is_regular c8)
		(is_regular c2)
		(is_regular c5)	
		(is_regular c6)

	)
	(:goal (and
		(at t7 l1)
		(at t4 l1)
		(at t3 l1)
		(available t7)
		(available t4)
		(available t3)

		;;avoid letting containers in the rail
		(free r1)
		(free r2)

		;;avoid letting containers at hand
		(free a1)
		(free a2)
	))
)
