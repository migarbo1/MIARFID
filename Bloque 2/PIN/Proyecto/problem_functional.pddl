(define (problem p1)
    (:domain puerto)
    (:objects
		;;loc 1
		l1 - location
		a1 - arm
		r1 - rail

		s11 - stack
		t7 - container
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
		t4 - container
		
		s22 - stack
		c2 - container
		t3 - container
		c5 - container
            
		s23 - stack
		c6 - container

	)
	(:init
		;;functions
		(= (speed r1) 2)
		(= (speed r2) 2)

		(= (length r1) 20)
		(= (length r2) 20)

		(= (weight c1) 10)
		(= (weight c2) 10)
		(= (weight t3) 30)
		(= (weight t4) 30)
		(= (weight c5) 10)
		(= (weight c6) 10)
		(= (weight t7) 10)
		(= (weight c8) 10)
		(= (weight c9) 10)
		(= (weight c10) 10)
		(= (weight c11) 10)


		;;Max height
		(= (max_height l1) 3)
		(= (max_height l2) 3)

		;;stacks at location
		(at s11 l1)
		(at s12 l1)
		(at s13 l1)

		;;arm at location
		(at a1 l1)
		(cinta r1 l1 l2)

		;;count for rails
		(= (actual_height s11) 2)
		(= (actual_height s12) 2)
		(= (actual_height s13) 1)

		;;rail wear
		(= (wear r1) 0)
		(= (wear r2) 0)

		;;free rail1
		(free r1)

		;;free arm1
		(free a1)

		;;container states location 1
		(available t7 l1)
		(clear t7)
		(top t7 s11)
		(on t7 c1)
		(on c1 s11)
		(at t7 l1)
		(at c1 l1)

		(available c10 l1)
		(clear c10)
		(top c10 s12)
		(on c10 c9)
		(on c9 s12)
		(at c10 l1)
		(at c9 l1)

		(available c11 l1)
		(clear c11)
		(top c11 s13)
		(on c11 s13)
		(at c11 l1)

		;;containers identity
		(is_target t7)
		(is_regular c1)
		(is_regular c10)
		(is_regular c9)	
		(is_regular c11)

;		;Location 2

		;;stacks at location
		(at s21 l2)
		(at s22 l2)
		(at s23 l2)

		;;arm at location
		(at a2 l2)
		(cinta r2 l2 l1)

		;;count for rails
		(= (actual_height s21) 2)
		(= (actual_height s22) 3)
		(= (actual_height s23) 1)

		;;free rail1
		(free r2)

		;;free arm1
		(free a2)

		;;container states location 2
		(available c8 l2)
		(clear c8)
		(top c8 s21)
		(on c8 t4)
		(on t4 s21)
		(at c8 l2)
		(at t4 l2)

		(available c2 l2)
		(clear c2)
		(top c2 s22)
		(on c2 t3)
		(on t3 c5)
		(on c5 s22)
		(at c2 l2)
		(at t3 l2)
		(at c5 l2)

		(available c6 l2)
		(clear c6)
		(top c6 s23)
		(on c6 s23)
		(at c6 l2)

		;;containers identity
		(is_target t4)
		(is_target t3)
		(is_regular c8)
		(is_regular c2)
		(is_regular c5)	
		(is_regular c6)

	)
	(:goal (and
		(available t7 l1)
		(available t4 l1)
		(available t3 l1)
	))
	(:metric minimize (+ (total-time) (+ (wear r1) (wear r2))))
)
