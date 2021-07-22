(define (problem LightProblem) (:domain farmlight)

(:objects 
 light_high light_low light_ambient -luminance
 l_high l_low l_none -light_sensor
)

(:init
    (isBright light_high)
    (isLightSensHigh l_high)
    (isDark light_low)
    (isLightSensLow l_low)
    
)

(:goal (on_light l_high)  
       
)
)