library(nhanesA)
# nhanesTables('EXAM', 2011) # useful for viewing tables

demo_g <- nhanes('DEMO_G')     # demographics
perio_g  <- nhanes('OHXPER_G') # perio exam
dent_g <- nhanes('OHXDEN_G')   # dentition exam
rec_g <- nhanes('OHXREF_G')    # oral health recommendation exam
ohq_g <- nhanes('OHQ_G')       # oral healh questionnaire
rx_g <- nhanes('RXQ_RX_G')     # Rx questionnaire
cig_g <- nhanes('SMQ_G')       # cigarette use questionnaire
cfq_g <- nhanes('CFQ_G')       # cognitive functioning questionnaire