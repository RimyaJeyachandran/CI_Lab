(defun fact2(n) 
  (if (= n 0) 1 (* n (fact2 (- n 1)))))

(defun fib2(n) 
  (cond ((= n 0) 0) 
        ((= n 1) 1) 
        ((> n 1) (+ (fib2 (- n 1)) (fib2 (- n 2))))))

(defun pali (str) 
  (equal str (reverse str)))

(defun AreaOfCircle() 
  (terpri) 
  (princ "Enter Radius: ") 
  (let* ((radius (read))
         (area (* 3.1416 radius radius)))
    (format t "Radius = ~F~%Area = ~F" radius area)))
