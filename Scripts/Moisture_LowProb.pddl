(define (problem MoistureProblem) (:domain farmmoisture)

(:objects 
 moist_high moist_low moist_ambient -moisture
 m_high m_low m_none -moist_sensor
)

(:init
    (isMoist moist_high)
    (isMoistSensHigh m_high)
    (isDry moist_low)
    (isMoistSensLow m_low)
    
)

(:goal (on_valve m_high)
)
)