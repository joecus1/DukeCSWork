; The congregation will be seated:
(require racket/base)     ; it's fun to use types, so we will
(require racket/stream)   ; it's cool to use streams, so we will

(define add-streams 
  (lambda ((a <stream>) (b <stream>))
    (cond ((stream-empty? a) b)
          ((stream-empty? b) a)
          (else (stream-cons (+ (stream-first a) (stream-first b))
                             (add-streams (stream-rest a) (stream-rest b)))))))

;;; Read the fine manual, open your hymnal, 
;;; See http://docs.racket-lang.org/reference/streams.html?q=stream#%28tech._stream%29

; The benediction and welcoming prayer:
(define ones  (stream-cons 1 ones))

;(print-stream (add-streams ones ones) 10)
(define integers (stream-cons 1 (add-streams ones integers)))
;(print-stream integers 100)

;; Here is the sermon. All rise and praise the mighty lambda
;;
;; There is no special sauce here; 
;; this is just like print-stream (which is how I wrote it...)
(define stream->listn
  (lambda ((s <stream>) (n <integer>))
    (cond ((or (zero? n) (stream-empty? s)) '())
          (else (cons (stream-first s)
                      (stream->listn (stream-rest s) (- n 1)))))))

;; Lift up your hearts  and sing with me now:
(stream->listn integers 20)

;; And so say we all.

(define add-series
  (lambda ((s1 <stream>) (s2 <stream>))
    (add-streams s1 s2)))

(define smul-series
  (lambda ((c <number>) (s <stream>))
    (cond ((stream-empty? s) '())
          (else (stream-cons (* (stream-first s) c)
                             (smul-series c (stream-rest s)))))))

(define mul-series
  (lambda ((s1 <stream>) (s2 <stream>))
    (cond ((stream-empty? s1) '())
          ((stream-empty? s2) '())
          (else (stream-cons (* (stream-first s1) (stream-first s2))
                             (add-series (smul-series (stream-first s2) (stream-rest s1)) (mul-series s1 (stream-rest s2))))))))

;; Test Case
(define ones (stream-cons 1 ones))

(define test (mul-series ones ones))

(stream->listn test 10)
;; Expected: (1 2 3 4 5 6 7 8 9 10)

