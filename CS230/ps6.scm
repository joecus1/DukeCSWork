(require racket/base)

;; ----------
;; Question 3
;; ----------

(define helper
  (lambda (emission k switchPr p1 p2 oldUnbiasPr oldBiasPr)
    (let* ((e (car emission))
           (unbiasPr (if (zero? e)
                         (max (* oldUnbiasPr (- 1 switchPr) p1)
                              (* oldBiasPr switchPr p1))
                         (max (* oldUnbiasPr (- 1 switchPr) (- 1 p1))
                              (* oldBiasPr switchPr (- 1 p1)))))
           (biasPr (if (zero? e)
                       (max (* oldUnbiasPr switchPr p2)
                            (* oldBiasPr (- 1 switchPr) p2))
                       (max (* oldUnbiasPr switchPr (- 1 p2))
                            (* oldBiasPr (- 1 switchPr) (- 1 p2))))))
      (cond ((= 1 k) unbiasPr)
            ((null? (cdr emission)) (max unbiasPr biasPr))
            (else (helper (cdr emission) (- k 1) switchPr p1 p2 unbiasPr biasPr))))))

(define viterbiProb
  (lambda (emission k switchPr p1 p2)
    (let* ((e (car emission))
           (unbiasPr (if (zero? e)
                         (* 0.5 p1)
                         (* 0.5 (- 1 p1))))
           (biasPr (if (zero? e)
                       (* 0.5 p2)
                       (* 0.5 (- 1 p2)))))
      (cond ((= 1 k) unbiasPr)
            ((null? (cdr emission)) (max unbiasPr biasPr))
            (else (helper (cdr emission) (- k 1) switchPr p1 p2 unbiasPr biasPr))))))

;; Test Cases
(display "Test Case 1: (viterbiProb '(0 0 1 1 0 1) 5 0.45 0.5 0.65)\n")
(viterbiProb '(0 0 1 1 0 1) 5 0.45 0.5 0.65)
;; Expect: 0.0019770029296875004

(display "Test Case 2: (viterbiProb '(1 0 1 0) 2 0.45 0.5 0.65)\n")
(viterbiProb '(1 0 1 0) 2 0.45 0.5 0.65)
;; Expect: 0.06875

;; ----------
;; Question 5
;; ----------

(define find-best
  (lambda (unbiasPr biasPr)
    (if (> (car (cdr unbiasPr)) (car (cdr biasPr)))
        unbiasPr
        biasPr)))

(define find-unbias-pr
  (lambda (unbiasPr biasPr s p e switchPr)
    (if (zero? e)
        (find-best (list (append (car unbiasPr) (list s))
                         (* (car (cdr unbiasPr)) (- 1 switchPr) p))
                   (list (append (car biasPr) (list s))
                         (* (car (cdr biasPr)) switchPr p)))
        (find-best (list (append (car unbiasPr) (list s))
                         (* (car (cdr unbiasPr)) (- 1 switchPr) (- 1 p)))
                   (list (append (car biasPr) (list s))
                         (* (car (cdr biasPr)) switchPr (- 1 p)))))))

(define find-bias-pr
  (lambda (unbiasPr biasPr s p e switchPr)
    (if (zero? e)
        (find-best (list (append (car unbiasPr) (list s))
                         (* (car (cdr unbiasPr)) switchPr p))
                   (list (append (car biasPr) (list s))
                         (* (car (cdr biasPr)) (- 1 switchPr) p)))
        (find-best (list (append (car unbiasPr) (list s))
                         (* (car (cdr unbiasPr)) switchPr (- 1 p)))
                   (list (append (car biasPr) (list s))
                         (* (car (cdr biasPr)) (- 1 switchPr) (- 1 p)))))))

(define helper2
  (lambda (emission switchPr s1 s2 p1 p2 oldUnbiasPr oldBiasPr)
    (let* ((e (car emission))
           (unbiasPr (find-unbias-pr oldUnbiasPr oldBiasPr s1 p1 e switchPr))
           (biasPr (find-bias-pr oldUnbiasPr oldBiasPr s2 p2 e switchPr)))
      (cond ((null? (cdr emission)) (find-best unbiasPr biasPr))
            (else (helper2 (cdr emission) switchPr s1 s2 p1 p2 unbiasPr biasPr))))))

(define viterbiPath
  (lambda (emission switchPr s1 s2 p1 p2)
    (let* ((e (car emission))
           (unbiasPr (list (list s1) (if (zero? e)
                                     (* 0.5 p1)
                                     (* 0.5 (- 1 p1)))))
           (biasPr (list (list s2) (if (zero? e)
                                   (* 0.5 p2)
                                   (* 0.5 (- 1 p2))))))
      (cond ((null? (cdr emission)) (find-best unbiasPr biasPr))
            (else (helper2 (cdr emission) switchPr s1 s2 p1 p2 unbiasPr biasPr))))))

            
    