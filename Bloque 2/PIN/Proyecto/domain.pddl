;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; El port esportiu de València :D
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain puertobase)
	(:requirements :strips :equality :typing :fluents)
	(:types 
		location container stack rail arm num - object
	)
	(:predicates
		(cinta ?r - rail ?x - location ?y - location)
		(next ?n1 - num ?n2 - num)
		(at ?s - (either stack arm rail container) ?l - location)
		(actual ?s - stack ?n - num)

		(max_height ?l - location ?n - num)

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
	;;	(:functions
	;;		(actual_height ?s - stack) ;ref: https://planning.wiki/ref/pddl21/domain
	;;		(max_height ?s - stack); ----^
	;;	)

	;;;;;;;;;;;
	;;ACTIONS;;
	;;;;;;;;;;;

	
	(:action stackOnContainer_regular
		:parameters (
			?t - container
			?c - (either container stack)
			?a - arm 
			?s - stack
			?l - location
			?current ?nxt ?max - num
		)
		:precondition (and 
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?s ?l)

			(holding ?a ?t)
			(top ?c ?s)

			;;height: max containers per location 
			(actual ?s ?current)
			(next ?current ?nxt)
			(max_height ?l ?max)
			(not (= ?max ?current))
			(is_regular ?t)
		)
		:effect (and 
			;;delete previous state
			(not (top ?c ?s))
			(not (holding ?a ?t))
			(not (clear ?c))

			;;set new state
			(top ?t ?s)
			(on ?t ?c)
			(clear ?t)
			(free ?a)

			(not(available ?c ?l))
			(available ?t ?l) ;;per consistencia

			;;counter
			(not (actual ?s ?current))
			(actual ?s ?nxt)

		)
	)
	(:action stackOnContainer_target
		:parameters (
			?t - container
			?c - (either container stack)
			?a - arm 
			?s - stack
			?l - location
			?current ?nxt ?max - num
		)
		:precondition (and 
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?s ?l)

			(holding ?a ?t)
			(top ?c ?s)

			;;height: max containers per location 
			(actual ?s ?current)
			(next ?current ?nxt)
			(max_height ?l ?max)
			(not (= ?max ?current))
			(is_target ?t)
		)
		:effect (and 
			;;delete previous state
			(not (top ?c ?s))
			(not (holding ?a ?t))
			(not (clear ?c))

			;;set new state
			(top ?t ?s)
			(on ?t ?c)
			(clear ?t)
			(free ?a)

			(available ?t ?l) ;;action

			;;counter
			(not (actual ?s ?current))
			(actual ?s ?nxt)

		)
	)
	;;unstack
	(:action unstack
		:parameters (
			?t - container
			?c - (either container stack)
			?a - arm 
			?s - stack
			?l - location
			?current ?prev - num
		)
		:precondition (and
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?s ?l)

			;;scenario: remove container from top of the other
			(top ?t ?s)
			(on ?t ?c)
			(free ?a)

			;;height: pointers to set the count 
			(actual ?s ?current)
			(next ?prev ?current)
		)
		:effect (and 
			;;delete previous state
			(not (top ?t ?s))
			(not (on ?t ?c))
			(not (clear ?t))
			(not (free ?a))
			(not (available ?t ?l))

			;;set new state
			(top ?c ?s)
			(clear ?c)
			(available ?c ?l)
			(holding ?a ?t)		

			;;counter
			(not (actual ?s ?current))
			(actual ?s ?prev)
		)
	)


	;;placeInRail
	(:action placeInRail
		:parameters (
			?l ?dest - location
			?a - arm
			?c - container
			?r - rail
		)
		:precondition (and
			;;location: everything in the same part of the port
			(at ?a ?l)

			;;scenario
			(holding ?a ?c)
			(free ?r)
			(cinta ?r ?l ?dest)
		)
		:effect (and
			;;delete previous state
			(not (holding ?a ?c))
			(not (free ?r))
			;;set new state
			(in ?c ?r)
			(free ?a)
		)
	)

	;;pickFromRail
	(:action pickFromRail
		:parameters (
			?r - rail
			?l ?ori - location
			?c - container
			?a - arm
		)
		:precondition (and
			;;(transported ?c ?l)
			(at ?c ?l)
			(in ?c ?r)
			(cinta ?r ?ori ?l)
			(free ?a)
		)
		:effect (and
			;;delete previous state
			(not (in ?c ?r))
			(not (free ?a))
			
			;;set new state
			(holding ?a ?c)
			(free ?r)
		)
	)

	;;transport
	(:action transport ;;polivalent xd
		:parameters (
			?r - rail
			?c - container
			?ori ?dest - location
		)

		:precondition (and 
			(in ?c ?r)
			(cinta ?r ?ori ?dest)
			(at ?c ?ori)
		)
		:effect (and
			(not (at ?c ?ori))
			(at ?c ?dest)
		)

	)
	
)
