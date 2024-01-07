(require racket/base)
(require racket/stream)

;; PROBLEM 1

(define cart
  (lambda (A B)
    (if (null? A)
        A
        (append (map (lambda (x) (list (car A) x)) B) (cart (cdr A) B)))))

; Test Cases

(display "P1:T1\n")
(cart '(A B) '(1 2 3 4 5))
; ((A 1) (A 2) (A 3) (A 4) (A 5) (B 1) (B 2) (B 3) (B 4) (B 5))

(display "P1:T2\n")
(cart '() '(1 2 3))
; ()

(display "P1:T3\n")
(cart '(1 2 3) '())
; ()

(display "P1:T4\n")
(cart '(1 2 3 4 5) '(1))
; ((1 1) (2 1) (3 1) (4 1) (5 1))

;; PROBLEM 2

(define fcn-helper
  (lambda (S)
    (if (null? (cdr S))
        #t
        (and (not (equal? (caar S) (car (cadr S)))) fcn-helper (cdr S)))))

(define fcn?
  (lambda (S)
    (if (null? S)
        #t
        (and (fcn-helper S) (fcn? (cdr S))))))

; Test Cases

(display "P2:T1\n")
(fcn? '((1 1) (2 1) (3 1) (4 1) (5 1)))
; #t

(display "P2:T2\n")
(fcn? '((1 1) (2 2) (3 3) (4 3) (5 5)))
; #t

(display "P2:T3\n")
(fcn? '((1 1) (2 2) (3 3) (4 4) (4 5)))
; #f

(display "P2:T4\n")
(fcn? '())
; #t

;; PROBLEM 3

(define remove-duplicates
  (lambda (l)
    (if (null? l)
        l
        (cons (car l) (remove-duplicates (filter (lambda (x) (not (equal? x (car l)))) (cdr l)))))))

(define pi1
  (lambda (S)
    (remove-duplicates (make-pi1 S))))

(define make-pi1
  (lambda (S)
    (if (null? S)
        S
        (cons (caar S) (make-pi1 (cdr S))))))

; Test Cases

(display "P3:T1\n")
(pi1 '((1 1) (2 1) (3 1) (4 1) (5 1)))
; (1 2 3 4 5)

(display "P3:T2\n")
(pi1 '((A 1) (A 2) (A 3) (A 4) (A 5) (B 1) (B 2) (B 3) (B 4) (B 5)))
; (A B)

(display "P3:T3\n")
(pi1 '())
; ()

(define pi2
  (lambda (S)
    (remove-duplicates (make-pi2 S))))

(define make-pi2
  (lambda (S)
    (if (null? S)
        S
        (cons (cadr (car S)) (make-pi2 (cdr S))))))

; Test Cases

(display "P3:T4\n")
(pi2 '((1 1) (2 1) (3 1) (4 1) (5 1)))
; (1)

(display "P3:T5\n")
(pi2 '((A 1) (A 2) (A 3) (A 4) (A 5) (B 1) (B 2) (B 3) (B 4) (B 5)))
; (1 2 3 4 5)

(display "P3:T6\n")
(pi2 '())
; ()

;; PROBLEM 4

(define diag
  (lambda (A)
    (if (null? A)
        A
        (cons (list (car A) (car A)) (diag (cdr A))))))

; Test Cases

(display "P4:T1\n")
(diag '(1 2 3 4 5))
; ((1 1) (2 2) (3 3) (4 4) (5 5))

(display "P4:T2\n")
(diag '())
; ()

;; PROBLEM 5

(define diag?
  (lambda (D)
    (if (null? D)
        #t
        (and (equal? (caar D) (car (cdar D))) (diag? (cdr D))))))

; Test Cases

(display "P5:T1\n")
(diag? '((1 1) (2 2) (3 3) (4 4) (5 5)))
; #t

(display "P5:T2\n")
(diag? '((1 1) (2 2) (3 3) (4 3) (5 5)))
; #f

(display "P5:T3\n")
(diag? '())
; #t

;; PROBLEM 6

(define diag-inv
  (lambda (Delta)
    (if (null? Delta)
        Delta
        (cons (caar Delta) (diag-inv (cdr Delta))))))

; Test Cases

(display "P6:T1\n")
(diag-inv '((1 1) (2 2) (3 3) (4 4) (5 5)))
; (1 2 3 4 5)

(display "P6:T2\n")
(diag-inv '())
; ()

(display "P6:T3\n")
(diag-inv '((3 3) (5 5)))
; (3 5)

;; PROBLEM 7

(define powerset
  (lambda (A)
    (if (null? A)
        (list A)
        (let ((plst (powerset (cdr A))))
          (append plst (map (lambda (x) (cons (car A) x)) plst))))))

; Test Cases

(display "P7:T1\n")
(powerset '(0 1 2))
; (() (2) (1) (1 2) (0) (0 2) (0 1) (0 1 2))

(display "P7:T2\n")
(powerset '())
; (())

(display "P7:T3\n")
(powerset '(1))
; (() (1))

(display "P7:T4\n")
(powerset '(1 2))
; (() (2) (1) (1 2))

;; STREAMS

(define ones (stream-cons 1 ones))

(define add-streams 
  (lambda ((a <stream>) (b <stream>))
    (cond ((stream-empty? a) b)
          ((stream-empty? b) a)
          (else (stream-cons (+ (stream-first a) (stream-first b))
                                (add-streams (stream-rest a) (stream-rest b)))))))

(define integers (stream-cons 1 (add-streams ones integers)))

(define stream->listn
  (lambda ((s <stream>) (n <integer>))
    (cond ((or (zero? n) (stream-empty? s)) '())
          (else (cons (stream-first s)
                      (stream->listn (stream-rest s) (- n 1)))))))

(define twos (stream-cons 2 twos))

(define evens (stream-cons 2 (add-streams twos evens)))

(define odds (stream-cons 1 (add-streams twos odds)))

;; PROBLEM II-1

(define stream-ref1
  (lambda (s dex)
    (if (zero? dex)
        (stream-first s)
        (stream-ref1 (stream-rest s) (- dex 1)))))

(define cart-infinite
  (lambda (A B)
    (if (or (stream-empty? A) (stream-empty? B))
        '()
        (letrec ((iter
                  (lambda (l dex1 dex2)
                    (if (equal? l dex1)
                        (stream-cons (list (stream-ref1 A dex1) (stream-ref1 B dex2))
                                     (iter (+ l 1) 0 (+ l 1)))
                        (stream-cons (list (stream-ref1 A dex1) (stream-ref1 B dex2))
                                     (iter l (+ dex1 1) (- dex2 1)))))))
          (iter 0 0 0)))))

; Test Cases

(display "PII-1:T1\n")
(stream->listn (cart-infinite integers integers) 10)
; ((1 1) (1 2) (2 1) (1 3) (2 2) (3 1) (1 4) (2 3) (3 2) (4 1))

(display "PII-1:T2\n")
(stream->listn (cart-infinite evens evens) 10)
; ((2 2) (2 4) (4 2) (2 6) (4 4) (6 2) (2 8) (4 6) (6 4) (8 2))

(display "PII-1:T3\n")
(cart-infinite '() integers)
; ()

(display "PII-1:T4\n")
(cart-infinite integers '())
; ()

;; PROBLEM II-3

(define remove-duplicates-infinite
  (lambda (s)
    (if (stream-empty? s)
        s
        (stream-cons (stream-first s)
                     (remove-duplicates-infinite
                      (stream-filter (lambda (x) (not (equal? (stream-first s) x)))
                                     (stream-rest s)))))))

(define pi1-infinite
  (lambda (S)
    (remove-duplicates-infinite (make-pi1-infinite S))))

(define make-pi1-infinite
  (lambda (S)
    (if (stream-empty? S)
        S
        (stream-cons (car (stream-first S)) (make-pi1-infinite (stream-rest S))))))

(define pi2-infinite
  (lambda (S)
    (remove-duplicates-infinite (make-pi2-infinite S))))

(define make-pi2-infinite
  (lambda (S)
    (if (stream-empty? S)
        S
        (stream-cons (cadr (stream-first S)) (make-pi2-infinite (stream-rest S))))))

; Test Cases

(display "PII-3:T1\n")
(stream->listn (pi1-infinite (cart-infinite integers integers)) 10)
; (1 2 3 4 5 6 7 8 9 10)

(display "PII-3:T2\n")
(stream->listn (pi1-infinite (cart-infinite odds evens)) 10)
; (1 3 5 7 9 11 13 15 17 19)

(display "PII-3:T3\n")
(stream->listn (pi2-infinite (cart-infinite odds evens)) 10)
; (2 4 6 8 10 12 14 16 18 20)

(display "PII-3:T4\n")
(stream->listn (pi1-infinite (cart-infinite '() integers)) 10)
; ()

(display "PII-3:T5\n")
(stream->listn (pi2-infinite (cart-infinite '() integers)) 10)
; ()

;; PROBLEM II-4

(define diag-infinite
  (lambda (A)
    (if (stream-empty? A)
        A
        (stream-cons (list (stream-first A) (stream-first A)) (diag-infinite (stream-rest A))))))

; Test Cases

(display "PII-4:T1\n")
(stream->listn (diag-infinite integers) 10)
; ((1 1) (2 2) (3 3) (4 4) (5 5) (6 6) (7 7) (8 8) (9 9) (10 10))

(display "PII-4:T2\n")
(diag-infinite '())
; ()

;; PROBLEM II-6

(define diag-inv-infinite
  (lambda (Delta)
    (if (stream-empty? Delta)
        Delta
        (stream-cons (car (stream-first Delta)) (diag-inv-infinite (stream-rest Delta))))))

; Test Cases

(display "PII-6:T1\n")
(stream->listn (diag-inv-infinite (diag-infinite integers)) 10)
; (1 2 3 4 5 6 7 8 9 10)

(display "PII-6:T2\n")
(diag-inv-infinite '())
; ()
