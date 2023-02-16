library(nhanesA)
# nhanesTables('EXAM', 2011) # useful for viewing tables

demo_vars <- nhanesTableVars('DEMO', 'DEMO_G').    # demographics
perio_vars  <- nhanesTableVars('EXAM', 'OHXPER_G') # perio exam
dent_vars <- nhanesTableVars('EXAM', 'OHXDEN_G').  # dentition exam
rec_vars <- nhanesTableVars('EXAM', 'OHXREF_G').   # oral health recommendation exam
ohq_vars <- nhanesTableVars('Q', 'OHQ_G')          # oral healh questionnaire
rx_vars <- nhanesTableVars('Q', 'RXQ_RX_G').       # Rx questionnaire
cig_vars <- nhanesTableVars('Q', 'SMQ_G').         # cigarette use questionnaire
cfq_vars <- nhanesTableVars('Q', 'CFQ_G').         # cognitive functioning questionnaire
