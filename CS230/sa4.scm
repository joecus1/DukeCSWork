(require racket/base)

(define true-for-all-pairs?
  (lambda ((func <function>) (l <list>))
    (cond ((zero? (length l)) #t)
          ((= 1 (length l)) #t)
          ((= 2 (length l))
           (if (func (car l) (car (cdr l))) #t #f))
          (else
           (if (func (car l) (car (cdr l)))
               (true-for-all-pairs? func (cdr l))
               #f)))))

(true-for-all-pairs? equal? '(a b c c d))
;; #f
(true-for-all-pairs? equal? '(a a a a a))
;; #t
(true-for-all-pairs? < '(20 16 5 8 6))
;; #f
(true-for-all-pairs? < '(3 7 19 22 43))
;; #t