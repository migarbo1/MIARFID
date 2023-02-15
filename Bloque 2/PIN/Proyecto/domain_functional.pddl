;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; El port esportiu de València :D
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain puerto)
	(:requirements :strips :equality :typing :durative-actions :fluents :duration-inequalities)
	(:types 
		location container stack rail arm - object
	)
	(:predicates
		(cinta ?r - rail ?x - location ?y - location)
		(at ?s - (either stack arm rail container) ?l - location)

		(free ?a - (either arm rail))
		(holding ?a - arm ?c - container)

		(top ?c - (either container stack) ?s - stack)
		(in  ?c - container ?r - rail)
		(on ?c - container ?x - (either container stack))
		(clear ?c - (either container stack))

		(is_target ?c - container)
		(is_regular ?c - container)

		(available ?t - (either container stack) ?l - location)
	)
	(:functions
		(actual_height ?s - stack)
		(max_height ?l - location)
		(weight ?c - container) ;; in tons: 10 for regular and 30 for target (mimics empty and full)
		(speed ?r - rail)
		(length ?r - rail)
		(wear ?r - rail)
	)

	;;;;;;;;;;;
	;;ACTIONS;;
	;;;;;;;;;;;	
	
	(:durative-action stackOnContainer_regular
		:parameters (
			?t - container
			?c - (either container stack)
			?a - arm 
			?s - stack
			?l - location
		)
		:duration (= 
			?duration 
			(-(* 5 (- (+ (max_height ?l) 1) (actual_height ?s))) (* 0.05 (weight ?t))) ;;arm takes 5 min to stack max height top, 10 to next, 15 to last... we substract the weight bonification: when stacking, the greater the weight, the faster the action
		)
		:condition (and 
			;;location: everything in the same part of the port
			(over all (at ?a ?l))
			(over all (at ?s ?l))

			(at start (holding ?a ?t))
			(at start (top ?c ?s))
			
			;;height: max containers per location 
			(at start (> (max_height ?l) (actual_height ?s)))
			
			(over all (is_regular ?t))
		)
		:effect (and 
			;;delete previous state
			(at end (not (top ?c ?s)))
			(at end (not (holding ?a ?t)))
			(at end (not (clear ?c)))
			

			;;set new state
			(at end (top ?t ?s))
			(at end (on ?t ?c))
			(at end (clear ?t))
			(at end (free ?a))

			(at start (not(available ?c ?l)))
			(at end (available ?t ?l))

			;;counter
			(at end (increase (actual_height ?s) 1))

		)
	)
	(:durative-action stackOnContainer_target
		:parameters (
			?t - container
			?c - (either container stack)
			?a - arm 
			?s - stack
			?l - location
		)
		:duration (= 
			?duration 
			(-(* 5 (- (+ (max_height ?l) 1) (actual_height ?s))) (* 0.05 (weight ?t))) 
		)
		:condition (and 
			;;location: everything in the same part of the port
			(over all (at ?a ?l))
			(over all (at ?s ?l))

			(at start (holding ?a ?t))
			(at start (top ?c ?s))

			;;height: max containers per location 
			(at start (> (max_height ?l) (actual_height ?s)))

			(over all (is_target ?t))
		)
		:effect (and 
			;;delete previous state
			(at end (not (top ?c ?s)))
			(at end (not (holding ?a ?t)))
			(at end (not (clear ?c)))

			;;set new state
			(at end (top ?t ?s))
			(at end (on ?t ?c))
			(at end (clear ?t))
			(at end (free ?a))

			(at end (available ?t ?l)) ;;action

			;;counter
			(at end (increase (actual_height ?s) 1))

		)
	)
	;;unstack
	(:durative-action unstack
		:parameters (
			?t - container
			?c - (either container stack)
			?a - arm 
			?s - stack
			?l - location
		)
		:duration (= 
			?duration 
			(+(* 5 (- (+ (max_height ?l) 1) (actual_height ?s))) (* 0.05 (weight ?t)))
		)
		:condition (and
			;;location: everything in the same part of the port
			(over all (at ?a ?l))
			(over all (at ?s ?l))

			;;scenario: remove container from top of the other
			(at start (top ?t ?s))
			(at start (on ?t ?c))
			(at start (free ?a))

		)
		:effect (and 
			;;delete previous state
			(at start (not (top ?t ?s)))
			(at start (not (on ?t ?c)))
			(at start (not (clear ?t)))
			(at start (not (free ?a)))
			(at start (not (available ?t ?l)))

			;;set new state
			(at end (top ?c ?s))
			(at end (clear ?c))
			(at end (available ?c ?l))
			(at end (holding ?a ?t)) ;;we force the arm to lift the container to its max height		

			;;counter
			(at end (decrease (actual_height ?s) 1))
		)
	)


	;;placeInRail
	(:durative-action placeInRail
		:parameters (
			?l ?dest - location
			?a - arm
			?c - container
			?r - rail
		)
		:duration (= 
			?duration 
			(- 20 (* 0.05 (weight ?c)))
		)
		:condition (and
			;;location: everything in the same part of the port
			(over all (at ?a ?l))

			;;scenario
			(at start (holding ?a ?c))
			(at start (free ?r))
			(over all (cinta ?r ?l ?dest))
		)
		:effect (and
			;;delete previous state
			(at end (not (holding ?a ?c)))
			(at end (not (free ?r)))
			;;set new state
			(at end (in ?c ?r))
			(at end (free ?a))
		)
	)

	;;pickFromRail
	(:durative-action pickFromRail
		:parameters (
			?r - rail
			?l ?ori - location
			?c - container
			?a - arm
		)
		:duration (= 
			?duration 
			(+ 20 (* 0.05 (weight ?c)))
		)
		:condition (and
		
			(over all (at ?c ?l))
			(at start (in ?c ?r))
			(over all (cinta ?r ?ori ?l))
			(at start (free ?a))
		)
		:effect (and
			;;delete previous state
			(at start (not (in ?c ?r)))
			(at end (not (free ?a)))
			
			;;set new state
			(at end (holding ?a ?c))
			(at end (free ?r))
		)
	)

	;;transport
	(:durative-action transport_slow ;;polivalent xd
		:parameters (
			?r - rail
			?c - container
			?ori ?dest - location
		)
		:duration (= 
			?duration 
			(+(/ (length ?r) (speed ?r)) (* 0.05 (weight ?c)))
		)
		:condition (and 
			(over all (in ?c ?r))
			(over all (cinta ?r ?ori ?dest))
			(at start (at ?c ?ori))
		)
		:effect (and
			(at start (not (at ?c ?ori)))
			(at end (at ?c ?dest))
			(at end (increase (wear ?r) 5))
		)

	)
	
	;;transport
	(:durative-action transport_fast ;;polivalent xd
		:parameters (
			?r - rail
			?c - container
			?ori ?dest - location
		)
		:duration (= 
			?duration 
			(+(/ (length ?r) (* (speed ?r) 2)) (* 0.05 (weight ?c)))
		)
		:condition (and 
			(over all (in ?c ?r))
			(over all (cinta ?r ?ori ?dest))
			(at start (at ?c ?ori))
		)
		:effect (and
			(at start (not (at ?c ?ori)))
			(at end (at ?c ?dest))
			(at end (increase (wear ?r) 10))
		)

	)
	
)
