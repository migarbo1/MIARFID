;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;; El port esportiu de València :D
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain puerto)
	(:requirements :strips :equality :typing :fluents)
	(:types 
		location container stack rail arm num - object
	)
	(:predicates
		(next ?n1 - num ?n2 - num ?l - location)
		(at ?s - (either stack arm container rail) ?l - location)
		(empty ?s - stack)
		(actual ?s - stack ?n - num)

		(max_height ?l - location ?n - num)

		(free ?a - (either arm rail))
		(holding ?a - arm ?c - container)

		(transported ?c - container ?r - rail)
		(to ?r - rail ?l2 - location)

		(top ?c - container ?s - stack)
		(in ?c - container ?s - (either stack rail))
		(on ?c - container ?x - (either container stack))
		(clear ?c - container)

		(is_target ?c - container)
		(is_regular ?c - container)

		(available ?t - container)
	)
	;;	(:functions
	;;		(actual_height ?s - stack) ;ref: https://planning.wiki/ref/pddl21/domain
	;;		(max_height ?s - stack); ----^
	;;	)

	;;;;;;;;;;;
	;;ACTIONS;;
	;;;;;;;;;;;

	;;stack
	(:action stackOnEmpty
		:parameters (
			?c - container 
			?a - arm 
			?s - stack
			?l - location
			?current ?next ?max - num
		)
		:precondition (and 
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?c ?l)
			(at ?s ?l)

			;;scneario: no containers
			(holding ?a ?c)
			(empty ?s)

			;;height: max containers per location 
			(actual ?s ?current)
			(next ?current ?next ?l)
		)
		:effect (and 
			;;delete previous state
			(not (empty ?s))
			(not (holding ?a ?c))

			;;set new state
			(top ?c ?s)
			(in ?c ?s)
			(on ?c ?s)
			(clear ?c)
			(free ?a)
			(available ?c)

			;;counter
			(not (actual ?s ?current))
			(actual ?s ?next)

		)
	)
	(:action stackOnContainer_regular
		:parameters (
			?t - container
			?c - container
			?a - arm 
			?s - stack
			?l - location
			?current ?next ?max - num
		)
		:precondition (and 
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?t ?l)
			(at ?s ?l)

			;;scneario: >1 container
			(holding ?a ?t)
			(top ?c ?s)

			;;height: max containers per location 
			(actual ?s ?current)
			(next ?current ?next ?l)
			(is_regular ?c)
		)
		:effect (and 
			;;delete previous state
			(not (top ?c ?s))
			(not (holding ?a ?t))

			;;set new state
			(top ?t ?s)
			(in ?t ?s)
			(on ?t ?c)
			(clear ?t)
			(free ?a)

			(not(available ?c))

			;;counter
			(not (actual ?s ?current))
			(actual ?s ?next)

		)
	)
	(:action stackOnContainer_target
		:parameters (
			?t - container
			?c - container
			?a - arm 
			?s - stack
			?l - location
			?current ?next ?max - num
		)
		:precondition (and 
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?t ?l)
			(at ?s ?l)

			;;scneario: >1 container
			(holding ?a ?t)
			(top ?c ?s)

			;;height: max containers per location 
			(actual ?s ?current)
			(next ?current ?next ?l)
			(is_target ?t)
		)
		:effect (and 
			;;delete previous state
			(not (top ?c ?s))
			(not (holding ?a ?t))

			;;set new state
			(top ?t ?s)
			(in ?t ?s)
			(on ?t ?c)
			(clear ?t)
			(free ?a)

			(available ?t) ;;action

			;;counter
			(not (actual ?s ?current))
			(actual ?s ?next)

		)
	)
	;;unstack
	(:action unstack
		:parameters (
			?t ?c - container
			?a - arm 
			?s - stack
			?l - location
			?current ?prev - num
		)
		:precondition (and
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?c ?l)
			(at ?t ?l)
			(at ?s ?l)

			;;scenario: remove container from top of the other
			(top ?t ?s)
			(in ?t ?s)
			(on ?t ?c)
			(clear ?t)
			(free ?a)

			;;height: pointers to set the count 
			(actual ?s ?current)
			(next ?prev ?current ?l)
		)
		:effect (and 
			;;delete previous state
			(not (top ?t ?s))
			(not (in ?t ?s))
			(not (on ?t ?c))
			(not (clear ?t))
			(not (free ?a))
			(not (available ?t))

			;;set new state
			(top ?c ?s)
			(clear ?c)
			(available ?c)
			(holding ?a ?t)		

			;;counter
			(not (actual ?s ?current))
			(actual ?s ?prev)
		)
	)
	(:action unstackToFree
		:parameters (
			?t - container
			?a - arm 
			?s - stack
			?l - location
			?current ?prev - num
		)
		:precondition (and
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?t ?l)
			(at ?s ?l)

			;;scenario: remove last container from stack
			(top ?t ?s)
			(in ?t ?s)
			(on ?t ?s)
			(clear ?t)
			(free ?a)

			;;height: pointers to set the count 
			(actual ?s ?current)
			(next ?prev ?current ?l)
		)
		:effect (and 
			;;delete previous state
			(not (top ?t ?s))
			(not (in ?t ?s))
			(not (on ?t ?s))
			(not (clear ?t))
			(not (free ?a))
			(not (available ?t))

			;;set new state
			(empty ?s)
			(holding ?a ?t)

			;;counter
			(not (actual ?s ?current))
			(actual ?s ?prev)
		)
	)

	;;placeInRail
	(:action placeInRail
		:parameters (
			?l - location
			?a - arm
			?c - container
			?r - rail
		)
		:precondition (and
			;;location: everything in the same part of the port
			(at ?a ?l)
			(at ?c ?l)
			(at ?r ?l)

			;;scenario
			(holding ?a ?c)
			(free ?r)
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
			?l - location
			?c - container
			?a - arm
		)
		:precondition (and
			(in ?c ?r)
			(to ?r ?l)
			(transported ?c ?r)
			(at ?a ?l)
			(free ?a)
		)
		:effect (and
			;;delete previous state
			(not (in ?c ?r))
			(not (transported ?c ?r))
			(not (free ?a))
			
			;;set new state
			;;(at ?c ?l) ho fa el trasport
			(holding ?a ?c)
			(free ?r)
		)
	)

	;;transport
	(:action transport ;;polivalent xd
		:parameters (
			?r - rail
			?c - container
			?lsrc - location
			?ldst - location
		)

		:precondition (and 
			;;(at ?c ?lsrc)
			(at ?r ?lsrc)
			(to ?r ?ldst)
			(in ?c ?r)
		)
		:effect (and
			;;delete previous state
			(not (at ?c ?lsrc))
			
			;;set new state
			(at ?c ?ldst)
			(transported ?c ?r) ;;since, for the first problem, this is inmediate
		)

	)
	
)
