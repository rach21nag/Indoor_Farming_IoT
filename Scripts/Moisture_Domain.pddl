(define (domain farmmoisture)

    (:requirements
        :strips
        :typing
        :negative-preconditions
    )
    (:types moisture -object
    moist_sensor -object
    )
    
    (:predicates
    (isMoist ?m -moisture)
    (isDry ?nm -moisture)
    (isMoistSensHigh ?mh -moist_sensor)
    (isMoistSensLow ?ml -moist_sensor)
    (on_valve ?ov -moist_sensor)
    (off_valve ?xv -moist_sensor)
    )
    
    (:action SwitchONValve
        :parameters (?nm -moisture ?ml ?ov -moist_sensor)
        :precondition (and (isDry ?nm) (isMoistSensLow ?ml))
        :effect (on_valve ?ov)
    )
    
    (:action SwitchOFFValve
        :parameters (?m -moisture ?mh ?xv -moist_sensor)
        :precondition (and (isMoist ?m) (isMoistSensHigh ?mh))
        :effect (off_valve ?xv)
    )
)