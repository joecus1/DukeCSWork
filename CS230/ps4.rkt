(require racket/base)
(require racket/stream)
(require racket/set)
;;; See http://docs.racket-lang.org/reference/streams.html?q=stream#%28tech._stream%29
; 
; A stream is a kind of sequence that supports functional iteration via stream-first and stream-rest.
; The stream-cons special form constructs a lazy stream.

  
(define ones  (stream-cons 1 ones))

(define add-streams 
  (lambda ((a <stream>) (b <stream>))
    (cond ((stream-empty? a) b)
          ((stream-empty? b) a)
          (else (stream-cons (+ (stream-first a) (stream-first b))
                                (add-streams (stream-rest a) (stream-rest b)))))))

(define scale-stream
  (lambda ((s <stream>) (factor <number>))
    (stream-map (lambda (x) (* x factor)) s)))

(define print-crlf 
  (lambda ()
    (printf "
")))

(define print-stream 
  (lambda ((s <stream>) (n <integer>))
    (cond ((zero? n) (printf "..."))
          (else  (print (stream-first s))
                 (printf " ")
                 (print-stream (stream-rest s) (- n 1))))))

;(print-stream ones 10)
;(print-stream (add-streams ones ones) 10)
(define integers (stream-cons 1 (add-streams ones integers)))
;(print-stream integers 100)

;; this is just like print-stream which is how I wrote it
(define stream->listn
  (lambda ((s <stream>) (n <integer>))
    (cond ((or (zero? n) (stream-empty? s)) '())
          (else (cons (stream-first s)
                      (stream->listn (stream-rest s) (- n 1)))))))

(stream->listn integers 20)

(define mul-streams 
  (lambda ((a <stream>) (b <stream>))
    (cond ((stream-empty? a) b)
          ((stream-empty? b) a)
          (else (stream-cons (* (stream-first a) (stream-first b))
                                (mul-streams (stream-rest a) (stream-rest b)))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(print-crlf)
(print-crlf)
(define squares (mul-streams integers integers))
(print-stream squares 10)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Factorial
(define factorial 
  (lambda (n)
    (if (< n 2) 1
        (* n (factorial (- n 1))))))

(define fact (mul-streams integers  (stream-cons 1 fact)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Fibonacci numbers

(define fibonacci
  (lambda ((n <integer>))
    (if (< n 2)
        n
        (+ (fibonacci (- n 1))
           (fibonacci (- n 2))))))

(define fibs
  (stream-cons 0
               (stream-cons 1
                            (add-streams fibs (stream-rest fibs)))))


;; Triangular Numbers
(define triangular
  (stream-cons 3
               (add-streams triangular (add-streams ones (add-streams ones integers)))))
(print-crlf)
(stream->listn triangular 20)

;; Hexagonal Numbers
;; (1s * 5) + n 4s

(define hexagonal
  (stream-cons 6
               (add-streams hexagonal (add-streams (scale-stream ones 5) (scale-stream integers 4)))))
(stream->listn hexagonal 20)

;; Triangular-hexagonal

(define triangular-and-hexagonal hexagonal)
(stream->listn triangular-and-hexagonal 20)

;; 10, 21, 36, 55
;; Triangular not hexagonal
(define triangular-not-hexagonal
  (stream-cons 10
               (add-streams triangular-not-hexagonal
                            (add-streams (scale-stream ones 7)
                                         (scale-stream integers 4)))))

(stream->listn triangular-not-hexagonal 20)


;; Halting stuff
(define prog
  (lambda (x <integer>)
    (if (one-safe? prog)
        (run-forever)
        x)))

(define func
  (lambda (x <integer>)
    x))

(define func2
  (lambda (x <integer>)
    (if (Equiv? func func2)
        (not func)
        func)))


(last (stream->listn fibs 21))
(fibonacci 20)

;; Pentagonal numbers for test
;; 1s * 4 + is * 3

(define pentagonal
  (stream-cons 5
               (add-streams pentagonal (add-streams (scale-stream ones 4) (scale-stream integers 3)))))

(stream->listn pentagonal 20)


(define prog
  (lambda (a b)
    (if (circle-safe? prog)
        (run-forever)
        'halted)))

(define graph-infinite
  (lambda ((f <function>) (X <stream>))
    (if (stream-empty? X)
        '()
        (stream-cons (list (stream-first X) (f (stream-first X)))
                     (graph-infinite f (stream-rest X))))))
