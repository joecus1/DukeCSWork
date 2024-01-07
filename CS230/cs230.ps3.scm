;;;
;;;cs230.ps3.scm
;;;
;;; For this problem set, when defining functions do not use types in 
;;; the lambda expressions. Instead, you should add a comment as to what 
;;; the type should be.

;;; Do not use (require racket/base) for this problem set.
;; ----- Useful functions -----

;; Define a predicate member? that returns #t if obj is a member of
;; lst and #f otherwise.

;; Contrast with the builtin member function, which returns the
;; sublist of lst starting with obj if obj is in the list.
(require racket/class)

(define member?
  (lambda (obj lst)
    (not (not (member obj lst)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;foldr and foldl are provided in scheme                                                                                                                                           
;;                                                                                                                                                                                 
;;(define accumulate                                                                                                                                                               
;; (lambda (initial op l)                                                                                                                                                          
;;    (cond ((null? l) initial)                                                                                                                                                    
;;      (else                                                                                                                                                                      
;;        (op (car l) (accumulate initial op (cdr l)))))))                                                                                                                         
;;                                                                                                                                                                                 
;;Note: (accumulate  '() cons '(1 2 3 4)) => '(1 2 3 4)
;;(define foldr (lambda (op init lst) (accumulate init op lst)))                                         
;;Note: (foldr cons '() '(1 2 3 4)) => '(1 2 3 4)                                                                              
;;Whereas: (foldl cons '() '(1 2 3 4) => '(4 3 2 1)  
;; ------ Data type definitions -----

;; Directed graph class definitions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;(vertices <graph>) => list of vertices
;;(edges <graph>) => list of edges 
;;
(defclass <graph> ()
  (vertices :initarg :vertices :accessor vertices) 
  (edges :initarg :edges :accessor edges))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;(name <vertex>) => the name of the vertex
;;ex: (name (make-vertex 'a)) => a
;;
(defclass <vertex> ()
  (name :initarg :name :accessor name))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;(start <directed-edge>) => first vertex of directed-edge
;;ex: (start (v1 v2)) => v1
;;(finish <directed-edge>) => second vertex of directed-edge
;;ex: (finish (v1 v2)) => v2
;;
(defclass <directed-edge> ()
  (start :initarg :start :accessor start)
  (finish :initarg :finish :accessor finish))

(define make-vertex
  (lambda (name)
    (make <vertex> :name name)))

(define make-edge
  (lambda (a b) ;a <vertex> b <vertex>
    (make <directed-edge> :start a :finish b)))

;; Two vertices are considered equal if their names are equal

(define equal-vertex?
  (lambda (v1 v2)
    (eq? (name v1) (name v2))))

;; lookup-vertex takes a name and a list of vertices, and finds a vertex
;; with that name.  Useful when you have the name of a vertex and need
;; the vertex itself.

(define lookup-vertex
  (lambda (vname vlist)
    (cond ((null? vlist) #f)
          ((equal? vname (name (first vlist))) (first vlist)) ;replaced car with first
          (else (lookup-vertex vname (rest vlist)))))) ;replaced cdr with rest

;; make-graph takes two lists whose atoms are symbols, one of the form
;;   (v1 v2 v3 ...) 
;; which becomes the list of vertices and the other of the form
;;   ((u1 u2) (u3 u4) ...) 
;; which becomes the list of edges.

(define make-graph
  (lambda (v-names e-list)
    (let* ((v (map make-vertex v-names))
           (create-edge 
              (lambda (name1 name2)
                (make-edge (lookup-vertex name1 v)
                           (lookup-vertex name2 v)))))
        (make <graph>
              :vertices v        
              :edges (map create-edge
                          (map first e-list)
                          (map second e-list))))))

;; Convert a list of vertices to a list of names of vertices

(define name-vertices
  (lambda (vlist)
    (map name vlist)))

;;;Same as standard member function but works with vertices
(define member-vertices 
  (lambda (a lat) 
    (cond ((null? lat) #f) 
          ((equal-vertex? a (car lat)) lat) 
          (else (member-vertices a (cdr lat))))))

;; Find the set difference of two sets represented as lists.  That is,
;; return a list consisting of everything in list1 that is not in
;; list2

(define set-diff-vertices
  (lambda (list1 list2)
    (cond ((null? list1) '()) 
          ((member-vertices (car list1) list2) (set-diff-vertices (cdr list1) list2))
          (#t (cons (car list1) (set-diff-vertices (cdr list1) list2))))))

;; Take the union of two sets represented as lists -- no duplicates

(define union
  (lambda (list1 list2)
    (cond ((null? list1) list2) 
          ((member (car list1) list2) (union (cdr list1) list2))
          (else (cons (car list1) (union (cdr list1) list2))))))
          

;; Take the intersection of two sets represented as lists 

(define intersection
  (lambda (list1 list2)
    (cond ((null? list1) '()) 
          ((member (car list1) list2) 
             (cons (car list1) (intersection (cdr list1) list2)))
          (else (intersection (cdr list1) list2)))))

;;; ----- TESTING EXAMPLES -----

;; ----- Problem 1 -----

(define exit?
  (lambda (e v)
    (if (equal-vertex? (start e) v)
        #t
        #f)))

(define (filter1 f lst)
  (foldr (lambda (x lst2)
           (if (f x)
               (cons x lst2)
               lst2))
         '()
         lst))

;(define filter1
;    (lambda (f lst)
;      (cond ((null? lst) '())
;            ((f (car lst)) (cons (car lst) (filter1 f (cdr lst))))
;            (else (filter1 f (cdr lst))))))

(define exits
  (lambda (v G)
    (map finish (filter1 (lambda (tmp)
                           (exit? tmp v))
                         (edges G)))))

(define g1 (make-graph '(a b c d e) 
		       '((a b) (a c) (b c) (b e) (c d) (d b))))

(display "P1:T1\n")
(name-vertices (exits (lookup-vertex 'b (vertices g1)) g1))
;(c e)
(display "P1:T2\n")
(name-vertices (exits (lookup-vertex 'e (vertices g1)) g1))
;()

; exits on first of list
; ? next of list is in exits
; return true if next of list is null
; return false if not in list
; recursive call

(define verify-path
  (lambda (g lst)
    (cond ((null? lst) #t)
          ((null? (cdr lst)) #t)
          ((null? (intersection (list (car (cdr lst))) (exits (car lst) g))) #f)
          (else (verify-path g (cdr lst))))))

(display "P1:T3\n")
(verify-path g1 
   (map (lambda (x) (lookup-vertex x (vertices g1))) '(a b c d b e)))
;#t
(display "P1:T4\n")
(verify-path g1 
   (map (lambda (x) (lookup-vertex x (vertices g1))) '(a b c d e)))
;#f
    
  
;; ----- Problem 2 -----
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;(label <labeled-edge>) => label of labeled-edge
;;ex: (label (make-labeled-edge a b l)) => l
;;
(defclass <labeled-edge> (<directed-edge>)
  (label :initarg :label :accessor label))

(define make-labeled-edge
  (lambda (a b l) ;a <vertex> b <vertex> l <obj>
    (make <labeled-edge> :start a :finish b :label l)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;(start-state <automaton>) => start-state of automaton
;;(final-states <automaton>) => list of final-states of automaton
;;    
(defclass <automaton> (<graph>)
  (start-state :initarg :start-state :accessor start-state)
  (final-states :initarg :final-states :accessor final-states)) ;start-state <symbol> final-states <list>
;;note: all accessors that apply to graph apply to automaton
  
;; make-automaton takes four parameters.  
;; The first is a list of symbols of the form (v1 v2 v3 ...) which 
;;   becomes the list of vertices.
;; The second is a list of triples of the form 
;;   ((u1 u2 l1) (u3 u4 l2) ...) which becomes the list of labeled
;;   edges (with the u's symbols which represent vertices and the l's 
;;   objects which become the labels).
;; The third is a single symbol for the start state.
;; The fourth is a list of symbols that represent final states.

(define make-automaton
  (lambda (v-names e-list s-state f-states) ;v-names <list>, e-list <list>, s-state <symbol>, f-states <list>
    (let* ((v (map make-vertex v-names))
           (create-labeled-edge 
              (lambda (name1 name2 label)
                (make-labeled-edge (lookup-vertex name1 v) 
                                   (lookup-vertex name2 v) 
                                   label))))
      (make <automaton>
            :vertices v
            :edges (map create-labeled-edge
                        (map first e-list)
                        (map second e-list)
                        (map third e-list))
            :start-state s-state
            :final-states f-states))))

(define dfa1
  (make-automaton '(a b c) 
	    '((a a 0) (a b 1) (b a 1) (b c 0) (c b 0) (c c 1))
            'a '(a)))

;;; ----- Problem 3 -----

; filter edges to be ones that have same label and start point
; if length of that is greater than 1 return #f
; if length is 0 return false
; return finish


(define has-label?
  (lambda (edge lab)
    (if (equal? (label edge) lab)
        #t
        #f)))

(define labeled
  (lambda (lab automaton)
    (filter1 (lambda (tmp)
               (has-label? tmp lab))
             (edges automaton))))

(define exits2
  (lambda (v es)
    (map finish (filter1 (lambda (tmp)
                           (exit? tmp v))
                         es))))
 

(define step-dfa
  (lambda (automaton state symbol)
    (if (not (lookup-vertex state (vertices automaton)))
        #f
        (let ((lst (exits2 (lookup-vertex state (vertices automaton)) (labeled symbol automaton))))
          (cond ((null? lst) #f)
                ((not (null? (cdr lst))) #f)
                (else (name (car lst))))))))


(display "P3: T1\n")
 (step-dfa dfa1 'c 1)
;c
(display "P3: T2\n")
 (step-dfa dfa1 'd 0)
;#f
(display "P3: T3\n")
 (step-dfa dfa1 'a 0)
;a
(display "P3: T4\n")
 (step-dfa dfa1 'a 1)
;b
(display "P3: T5\n")
 (step-dfa dfa1 'a 2)
;#f

(define bad-dfa
    (make-automaton '(a b c)
                    '((a a 0) (a b 0) (b a 1) (b c 0) (c b 0) (c c 1))
                    'a
                    '(a)))

(display "P3: T6\n")
(step-dfa bad-dfa 'a 0)
;#f


;; ----- Problem 4 -----


; get start state
; if out of tokens return false
; on last token
; call step-dfa using first token of list
; if false return false

(define helper-dfa
  (lambda (automaton state symbols)
    (cond ((null? symbols) (member? state (final-states automaton)))
          ((not (step-dfa automaton state (car symbols))) #f)
          (else (helper-dfa automaton (step-dfa automaton state (car symbols)) (cdr symbols))))))

(define simulate-dfa
  (lambda (automaton symbols)
    (helper-dfa automaton (start-state automaton) symbols)))


(define integer->binary
  (lambda (n)
    (cond ((eq? n 0) '())
	  (else (append (integer->binary (quotient n 2)) 
                        (list (if (even? n) 0 1)))))))

(display "P4: T1\n")
(simulate-dfa dfa1 '(1 0 0 1))
;#t
(display "P4: T2\n")
(simulate-dfa dfa1 '(1 0 1 1))
;#f
(display "P4: T3\n")
(simulate-dfa dfa1 (integer->binary 12))
;#t
(display "P4: T4\n")
(simulate-dfa dfa1 (integer->binary 10))
;#f

;; ----- Problem 5 -----

(define nfa1
  (make-automaton '(a b c d e)
	    '((a a 0) (a a 1) (a b 1) (a c 0) (b d 1) (c e 0)
	      (d d 0) (d d 1) (e e 0) (e e 1))
	    'a
	    '(d e)))

(define step-nfa-helper
  (lambda (automaton state symbol)
    (if (not (lookup-vertex state (vertices automaton)))
        #f
        (let ((lst (exits2 (lookup-vertex state (vertices automaton)) (labeled symbol automaton))))
          (cond ((null? lst) #f)
                (else (map name lst)))))))

(define (remove-duplicate lst)
  (if (null? lst) '()
      (cons (car lst)
            (remove-duplicate (filter1 (lambda (x)
                                         (not (equal? x (car lst)))) 
                                    (cdr lst))))))

(define step-nfa
  (lambda (automaton states symbol)
    (let ((lst (foldr (lambda (state lst)
             (cond ((not (step-nfa-helper automaton state symbol)) (append '() lst))
                   (else (append (step-nfa-helper automaton state symbol) lst))))
           '() states)))
      (if (null? lst)
          #f
          (remove-duplicate lst)))))

; Testing step-nfa
(display "P5: T1\n")
 (step-nfa dfa1 '(c) 1)
;(c)
(display "P5: T2\n")
 (step-nfa dfa1 '(d) 0)
;#f
(display "P5: T3\n")
 (step-nfa dfa1 '(a) 0)
;(a)
(display "P5: T4\n")
 (step-nfa dfa1 '(a) 1)
;(b)
(display "P5: T5\n")
 (step-nfa dfa1 '(a) 2)
;#f
(display "P5: T6\n")
(step-nfa nfa1 '(a c) 0)
;(a c e)
(display "P5: T7\n")
(step-nfa nfa1 '(a d) 1)
;(a b d)


(define helper-nfa
  (lambda (automaton states symbols)
    (cond ((null? symbols) (if (null? (intersection states (final-states automaton)))
                               #f
                               #t))
          ((not (step-nfa automaton states (car symbols))) #f)
          (else (helper-nfa automaton (step-nfa automaton states (car symbols)) (cdr symbols))))))

(define simulate-nfa
  (lambda (automaton symbols)
    (helper-nfa automaton (list (start-state automaton)) symbols)))

(display "P5: T8\n")
(simulate-nfa dfa1 '(1 0 0 1))
;#t
(display "P5: T9\n")
(simulate-nfa dfa1 '(1 0 1 1))
;#f
(display "P5: T10\n")
(simulate-nfa dfa1 (integer->binary 12))
;#t
(display "P5: T11\n")
(simulate-nfa dfa1 (integer->binary 10))
;#f
(display "P5: T12\n")
(simulate-nfa nfa1 '(0))
;#f
(display "P5: T13\n")
(simulate-nfa nfa1 '(0 0))
;#t
(display "P5: T14\n")
(simulate-nfa nfa1 '(1 1 1))
;#t
(display "P5: T15\n")
(simulate-nfa nfa1 '(0 1 1))
;#t
(display "P5: T16\n")
(simulate-nfa nfa1 '(0 1))
;#f

;; ----- Problem 6 -----

(define g2 (make-graph '(a b c) '((a b) (b a) (a c) (c a) (b c))))
(define g3 (make-graph '(a b c d) '((a b) (b c) (a c) (c b) (d b))))
(define g4 (make-graph '(a b c d) '((a b) (a c) (b a) (c a) (a d) (b c) (c b))))

; start
; get exits start
; add start to visited
; call function recursively on

(define filter-mult
  (lambda (lst toRemove)
    (if (or (null? toRemove) (null? lst))
        lst
        (filter-mult (filter1 (lambda (x)
                                (not (equals? x (car toRemove)))) lst)
                     (cdr toRemove)))))

(define exits-mult
  (lambda (starts g)
    (remove-duplicate (name-vertices (foldr (lambda (start lst)
             (append (exits (lookup-vertex start (vertices g)) g) lst)) '() starts)))))

(define path-helper
  (lambda (starts end g visited)
    (cond ((null? starts) #f)
          ((member? end starts) #t)
          (else (path-helper (exits-mult (filter-mult starts visited) g) end g (append starts visited))))))

(define path?
  (lambda (start end g)
    (path-helper (list start) end g '())))
    

(display "P6: T1\n")
(path? 'a 'e g1)
;#t
(display "P6: T2\n")
 (path? 'd 'a g1)
;#f
(display "P6: T3\n")
 (path? 'a 'c g2)
;#t
(display "P6: T4\n")
 (path? 'c 'b g2)
;#t
(display "P6: T5\n")
 (path? 'd 'd g3)
;#t
(display "P6: T6\n")
 (path? 'a 'd g3)
;#f
(display "P6: T7\n")
 (path? 'b 'd g4)
;#t

;; ----- Problem 7 -----

(defclass <vertex+parent> (<vertex>)
  (parent :initarg :parent :accessor parent))

(define make-vertex+parent
  (lambda (v p) ;v <vertex>, p <obj>                                                                                                                                               
    (make <vertex+parent> :name (name v) :parent p)))

(define exits-mult-vp
  (lambda (starts g)
    (remove-duplicate (foldr (lambda (start lst)
             (append (map
                      (lambda (x)
                        (make-vertex+parent x start))
                      (exits start g))
                     lst)) '() starts))))

(define filter-mult-vp
  (lambda (lst toRemove)
    (if (or (null? toRemove) (null? lst))
        lst
        (filter-mult-vp (filter1 (lambda (x)
                                (not (equals? (name x) (name (car toRemove))))) lst)
                     (cdr toRemove)))))

(define expand-path
  (lambda (v origin)
    (if (equals? (name v) origin)
        (list v)
        (append (expand-path (parent v) origin) (list v)))))


(define find-path-helper
  (lambda (starts end g visited origin)
    (cond ((null? starts) #f)
          ((member? end (name-vertices starts)) (expand-path (lookup-vertex end starts) origin))
          (else (find-path-helper (exits-mult-vp (filter-mult-vp starts visited) g) end g (append starts visited) origin)))))


(define find-path
  (lambda (start end g)
    (if (not (path? start end g))
        #f
        (find-path-helper (list (lookup-vertex start (vertices g))) end g '() start))))
        

(display "P7: T1\n")
(name-vertices (find-path 'a 'e g1))
; (a b e)
(display "P7: T2\n")
 (find-path 'd 'a  g1)
; #f
(display "P7: T3\n")
 (name-vertices (find-path 'a 'c g2))
; (a c) or (a b c)
(display "P7: T4\n")
 (name-vertices (find-path 'c 'b g2))
; (c a b)
(display "P7: T5\n")
 (name-vertices (find-path 'd 'd g3))
; (d)
(display "P7: T6\n")
 (find-path 'a 'd g3)
; #f
(display "P7: T7\n")
 (name-vertices (find-path 'b 'd g4))
; (b a d)

; ----- Extra Credit -----

(define has-label?
  (lambda (edge lab)
    (if (equal? (label edge) lab)
        #t
        #f)))

(define labeled2
  (lambda (lab edges)
    (filter1 (lambda (tmp)
               (has-label? tmp lab))
             edges)))

(define has-start?
  (lambda (edge s)
    (if (equal-vertex? (start edge) s)
        #t
        #f)))

(define same-start
  (lambda (s edges)
    (filter1 (lambda (tmp)
               (has-start? tmp s))
             edges)))

(define deterministic?
  (lambda (edges)
    (if (null? edges)
        #t
        (let ((s (start (car edges)))
              (lab (label (car edges))))
          (if (null? (same-start s (labeled2 lab (cdr edges))))
              (deterministic? (cdr edges))
              #f)))))
      

(define make-dfa
  (lambda (v-names e-list s-state f-states) ;v-names <list>, e-list <list>, s-state <symbol>, f-states <list>
    (let* ((v (map make-vertex v-names))
           (create-labeled-edge 
              (lambda (name1 name2 label)
                (make-labeled-edge (lookup-vertex name1 v) 
                                   (lookup-vertex name2 v) 
                                   label))))
      (if (deterministic? (map create-labeled-edge
                               (map first e-list)
                               (map second e-list)
                               (map third e-list)))
          (make <automaton>
                :vertices v
                :edges (map create-labeled-edge
                            (map first e-list)
                            (map second e-list)
                            (map third e-list))
                :start-state s-state
                :final-states f-states)
          #f))))


(display "EC: T1\n")
(make-dfa '(a b c) 
          '((a a 0) (a b 1) (b a 1) (b c 0) (c b 0) (c c 1))
          'a '(a))
; automaton


(display "EC: T2\n")
(make-dfa '(a b c)
          '((a a 0) (a b 0) (b a 1) (b c 0) (c b 0) (c c 1))
          'a
          '(a))
;#f

  
