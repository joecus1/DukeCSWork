;;; Go to Language, Choose Language, Other Languages, Swindle, Full Swindle
;;; This may have to be done in cs230-graphics.scm as well
;;; cs230.ps1.scm


(require racket/base) ;;This allows the type system to work.
(require (file "cs230-graphics.scm")) ;;Pull in the definitions for the drawing window and stuff. Assumes the file is in the same directory. 

;; Here are the procedures you will modify in the problem set
(define side
  (lambda ((length <real>) (heading <real>) (level <integer>))
    (if (zero? level)
        (drawto heading length)
        (let ((len/3 (/ length 3))
              (lvl-1 (- level 1)))
          (side len/3 heading lvl-1)
          (side len/3 (- heading PI/3) lvl-1)
          (side len/3 (+ heading PI/3) lvl-1)
          (side len/3 heading lvl-1)))))

(define snowflake:0
  (lambda ((length <real>) (level <integer>))
    (side length 0.0 level)
    (side length (* 2 PI/3) level)
    (side length (- (* 2 PI/3)) level)))

;; Problem 1
(define flip-side
  (lambda ((length <real>) (heading <real>) (level <integer>))
    (if (zero? level)
        (drawto heading length)
        (let ((sublen (/ (/ length 2) (sqrt 2)))
              (lvl-1 (- level 1)))
          (flip-side sublen (- heading PI/4) lvl-1)
          (flip-side (* sublen 2) (+ heading PI/4) lvl-1)
          (flip-side sublen (- heading PI/4) lvl-1)))))

(define pentagon-snowflake:1
  (lambda ((length <real>) (level <integer>))
    (flip-side length 0.0 level)
    (flip-side length (- PI (* PI 0.6)) level)
    (flip-side length (* 2 (- PI (* PI 0.6))) level)
    (flip-side length (- (* 2 (- PI (* PI 0.6)))) level)
    (flip-side length (- (- PI (* PI 0.6))) level)))

;; Problem 2
(define pentagon-snowflake:2
  (lambda ((length <real>) (level <integer>) (generator <function>))
    (generator length 0.0 level)
    (generator length (- PI (* PI 0.6)) level)
    (generator length (* 2 (- PI (* PI 0.6))) level)
    (generator length (- (* 2 (- PI (* PI 0.6)))) level)
    (generator length (- (- PI (* PI 0.6))) level)))

(define snowflake:2
  (lambda ((length <real>) (level <integer>) (generator <function>))
    (generator length 0.0 level)
    (generator length (* 2 PI/3) level)
    (generator length (- (* 2 PI/3)) level)))

;; Problem 3
(define snowflake-inv
  (lambda ((length <real>) (level <integer>) (generator <function>) (inverter <function>))
    (generator length 0.0 level inverter)
    (generator length (* 2 PI/3) level inverter)
    (generator length (- (* 2 PI/3)) level inverter)))

(define side-inv
  (lambda ((length <real>) (heading <real>) (level <integer>) (inverter <function>))
    (if (zero? level)
        (drawto heading length)
        (let ((len/3 (/ length 3))
              (lvl-1 (- level 1)))
          (if (positive? (inverter level))
              (begin (side-inv len/3 heading lvl-1 inverter)
                     (side-inv len/3 (- heading PI/3) lvl-1 inverter)
                     (side-inv len/3 (+ heading PI/3) lvl-1 inverter)
                     (side-inv len/3 heading lvl-1 inverter))
              (begin (side-inv len/3 heading lvl-1 inverter)
                     (side-inv len/3 (+ heading PI/3) lvl-1 inverter)
                     (side-inv len/3 (- heading PI/3) lvl-1 inverter)
                     (side-inv len/3 heading lvl-1 inverter)))))))

;; Problem 4
(define snowflake-length
  (lambda ((length <real>) (level <integer>) (generator <function>) (inverter <function>))
    (+ (generator length 0.0 level inverter)
    (generator length (* 2 PI/3) level inverter)
    (generator length (- (* 2 PI/3)) level inverter))))

(define side-length
  (lambda ((length <real>) (heading <real>) (level <integer>) (inverter <function>))
    (if (zero? level)
        length
        (let ((len/3 (/ length 3))
              (lvl-1 (- level 1)))
          (if (positive? (inverter level))
              (+ (side-length len/3 heading lvl-1 inverter)
                     (side-length len/3 (- heading PI/3) lvl-1 inverter)
                     (side-length len/3 (+ heading PI/3) lvl-1 inverter)
                     (side-length len/3 heading lvl-1 inverter))
              (+ (side-length len/3 heading lvl-1 inverter)
                     (side-length len/3 (+ heading PI/3) lvl-1 inverter)
                     (side-length len/3 (- heading PI/3) lvl-1 inverter)
                     (side-length len/3 heading lvl-1 inverter)))))))

;; Make the graphics window visible, and put the pen somewhere useful
(init-graphics 640 480)
(clear)
(moveto 100 100)

;; Problem 4- Expected 711.111111111112
(snowflake-length 100.0 3 side-length 
                  (lambda ((level <integer>)) 1))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
