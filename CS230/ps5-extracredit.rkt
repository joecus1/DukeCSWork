(require racket/base)

;; Part A

(define plug-root
  (lambda ((root <integer>) (poly <lst>))
    (if (null? poly)
        0
        (+ (* (car poly) (expt root (- (length  poly) 1))) (plug-root root (cdr poly))))))

(define check-roots
  (lambda ((roots  <lst>) (poly <lst>))
    (cond ((null? roots) '())
          ((zero? (plug-root (car roots) poly))
           (cons (car roots) (check-roots (cdr roots) poly)))
          (else (check-roots (cdr roots) poly)))))

(define factors
  (lambda ((iter <integer>) (x  <integer>))
    (cond ((> iter  x)  '())
          ((zero? (modulo x iter)) (cons iter (cons (- 0 iter) (factors (+ 1 iter) x))))
          (else (factors (+ 1 iter) x)))))

(define get-last
  (lambda ((poly <iter>))
    (cond ((null? poly) 0)
          ((zero? (get-last (cdr poly))) (car poly))
          (else (get-last (cdr poly))))))

(define p
  (lambda ((poly <lst>))
    (check-roots
     (cons 0 (cons 1 (cons -1 (factors 2 (abs (get-last (car (cdr poly))))))))
     (cons 1 (car (cdr poly))))))

(define safe?
  (lambda ((f <fcn>) (a <arg>))
    (let ((d (lambda (x) (f a) p)))
      (Poly-check? d))))




;; Part B
(define safe?
  (lambda ((f <fcn>) (a <arg>))
    (let ((d (lambda (x) (f a) 0)))
      (expr=zero? d))))