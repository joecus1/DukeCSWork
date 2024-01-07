(require racket/base)

(define reverse1
  (lambda ((l <list>))
    (if (null? l)
        '()
        (append (reverse1 (cdr l)) (list (car l))))))

(reverse1 '())
;; ()
(reverse1 '(1))
;; (1)
(reverse1 '(1 2 3 4 5))
;; (5 4 3 2 1)
(reverse1 '(1 (2 3) 4 5))
;; (5 4 (2 3) 1)

(define reverse-tail
  (lambda ((l <list>))
    (letrec ((iter
              (lambda ((lst <list>) (result <list>))
                (if (null? lst)
                    result
                    (iter (cdr lst) (append (list (car lst)) result))
                    )
                )
              ))
      (iter l '())
     )
    )
  )

(reverse-tail '())
;; ()
(reverse-tail '(1))
;; (1)
(reverse-tail '(1 2 3 4 5))
;; (5 4 3 2 1)
(reverse-tail '(1 (2 3) 4 5))
;; (5 4 (2 3) 1)