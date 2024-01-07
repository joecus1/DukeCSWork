(require racket/base)

;; my function
(define multiply
  (lambda ((a <number>) (b <integer>))
    (letrec ((iter
              (lambda ((c <number>) (d <integer>) (result <number>))
                (cond ((zero? d) result)
                      ((odd? d)
                       (iter (+ c c) (quotient d 2) (+ result c)))
                      (else
                       (iter (+ c c) (quotient d 2) result))))))
      (iter a b 0))))
 