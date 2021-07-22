(define (domain farmtemp)

    (:requirements
        :strips
        :typing
        :negative-preconditions
    )
    (:types temperature -object
    temp_sensor -object
    )
    
    (:predicates
    (isTempHigh ?th -temperature)
    (isTempLow ?tl -temperature)
    (isTempSensHigh ?h -temp_sensor)
    (isTempSensLow ?l -temp_sensor)
    (on_cooler ?oc -temp_sensor)
    (off_cooler ?xc -temp_sensor)
    )
    
    (:action SwitchONCooler
        :parameters (?th -temperature ?h ?oc -temp_sensor)
        :precondition (and (isTempHigh ?th) (isTempSensHigh ?h))
        :effect (on_cooler ?oc)
    )
    
    (:action SwitchOFFCooler
        :parameters (?tl -temperature ?xc ?l -temp_sensor)
        :precondition (and (isTempLow ?tl) (isTempSensLow ?l))
        :effect (off_cooler ?xc)
    )
)