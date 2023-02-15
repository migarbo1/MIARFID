(define (problem strips-sat-x-1)
    (:domain puerto)
    (:objects
        ;;loc 1
        c7 - target
        c1 - regular
        stack11 - stack

        c10 - regular
        c9 - regular
        stack12 - stack

        c11 - regular
        stack13 - stack

        arm1 - arm
        rail_asc - ascendent
        location1 - location

        ;;loc 2
        c8 - regular
        c4 - target
        stack21 - stack

        c2 - regular
        c3 - target
        c5 - regular
        stack22 - stack

        c6 - regular
        stack23 - stack

        arm2 - arm
        rail_desc - descendent
        location2 - location

		n0 - num
		n1 - num
		n2 - num
    )
    (:init
        ;;;;set max height for stacks
        ;;(= (max_height stack11) 2)
        ;;(= (max_height stack12) 2)
        ;;(= (max_height stack13) 2)

        ;;(= (max_height stack21) 3)
        ;;(= (max_height stack22) 3)
        ;;(= (max_height stack23) 3)

		;;	Dos opcions
		;;	Amb predicat tope
		;;		Definim els màxims
		;; 			(max location1 n2)
		;; 			(max location2 n3)
		;;		Definim la altura actual
		;;			(actual location1 n0)
		;;			(actual location2 n0)
		;;		Definim el ordre dels numeros
		;;			(next n0 n1)
		;;			(next n1 n2)
		;;			(next n2 n3)

        ;;define initial state for location 1
        (top c7 stack11)
        (in c7 stack11)
        (on c7 c1)
        (in c1 stack11)
        (on c1 stack11)
        (at stack11 location1)
        (full stack11)

        (top c10 stack12)
        (in c10 stack12)
        (on c10 c9)
        (in c9 stack12)
        (on c9 stack12)
        (at stack12 location1)
        (full stack12)

        (top c11 stack13)
        (in c11 stack13)
        (on c11 stack13)
        (at stack13 location1)

        (free arm1)
        (free rail_asc)
        (at arm1 location1)
        ;;doubt: don't know if this really helps, but seems easier to check
        (at c7 location1)
        (at c1 location1)
        (at c10 location1)
        (at c9 location1)
        (at c11 location1)
        
        ;;define initial state for location 2
        (top c8 stack21)
        (in c8 stack21)
        (on c8 c4)
        (in c4 stack21)
        (on c4 stack21)
        (blocked c4)
        (at stack21 location2)

        (top c2 stack22)
        (in c2 stack22)
        (on c2 c3)
        (in c3 stack22)
        (on c3 c5)
        (blocked c3)
        (in c5 stack22)
        (on c5 stack22)
        (at stack22 location2)
        (full stack22)

        (top c6 stack23)
        (in c6 stack23)
        (on c6 stack23)
        (at stack23 location2)

        (free arm2)
        (at arm2 location2)

        (free rail_desc)
        ;;doubt: don't know if this really helps, but seems easier to check
        (at c8 location2)
        (at c4 location2)
        (at c2 location2)
        (at c3 location2)
        (at c5 location2)
        (at c6 location2)
        
    )
    (:goal (and
            (at c7 location1)
            (at c4 location1)
            (at c3 location1)
            (available c7)
            (available c4)
            (available c1)
        )
    )
)
