(define (domain farmlight)

    (:requirements
        :strips
        :typing
        :negative-preconditions
    )
    (:types luminance -object
    light_sensor -object
    )
    
    (:predicates
    (isBright ?lh -luminance)
    (isDark ?ll -luminance)
    (isLightSensHigh ?hi -light_sensor)
    (isLightSensLow ?lo -light_sensor)
    (on_light ?ol -light_sensor)
    (off_light ?xl -light_sensor)
    )
    
    (:action SwitchOFFLight
        :parameters (?lh -luminance ?hi ?xl -light_sensor)
        :precondition (and (isBright ?lh) (isLightSensHigh ?hi))
        :effect (off_light ?xl)
    )
    
    (:action SwitchONLight
        :parameters (?ll -luminance ?ol ?lo -light_sensor)
        :precondition (and (isDark ?ll) (isLightSensLow ?lo))
        :effect (on_light ?ol)
    )
)