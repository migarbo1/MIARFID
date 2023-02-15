(define (problem p1)
    (:domain puerto)
    (:objects
		;;loc 1
		l1 - location
		a1 - arm
		r1 - rail

		s11 - stack
		c7 - container
		c1 - container
		
		s12 - stack
		c10 - container
		c9 - container
            
		s13 - stack
		c11 - container

		;;loc 2
		l2 - location
		a2 - arm
		r2 - rail

		s21 - stack
		c8 - container
		c4 - container
		
		s22 - stack
		c2 - container
		c3 - container
		c5 - container
            
		s23 - stack
		c6 - container

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
		(at c7 l1)
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
		(available c7)
		(clear c7)
		(top c7 s11)
		(in c7 s11)
		(on c7 c1)
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
		(is_target c7)
		(is_regular c1)
		(is_regular c10)
		(is_regular c9)	
		(is_regular c11)

;		;Location 2
		;;containers at location 2
		(at c8 l2)
		(at c4 l2)
		(at c2 l2)
		(at c3 l2)
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
		(on c8 c4)
		(in c4 s21)
		(on c4 s21)

		(clear c2)
		(top c2 s22)
		(in c2 s22)
		(on c2 c3)
		(in c3 s22)
		(on c3 c5)
		(in c5 s22)
		(on c5 s22)

		(clear c6)
		(top c6 s23)
		(in c6 s23)
		(on c6 s23)

		;;containers identity
		(is_target c4)
		(is_target c3)
		(is_regular c8)
		(is_regular c2)
		(is_regular c5)	
		(is_regular c6)

	)
	(:goal (and
		(top c2 s23)
		(in c2 s23)
		(on c2 c6)
		(clear c2)
		(free a2)
	))
)
