library(nhanesA)
# nhanesTables('EXAM', 2003) # useful for viewing tables

# define function to save data file
write_data <- function(table, file_name) {
  fname <- paste0("../data/2003-2004/", file_name)
  write.table(table, file=fname, quote=FALSE, sep='\t', row.names=FALSE)
}

# demographics data
demo_c <- nhanes('DEMO_C')
write_data(demo_c, 'DEMO_C_demographics.tsv')

# food security questionnaire data
fsq_c <- nhanes('FSQ_C')
write_data(fsq_c, 'FSQ_C_food-security_questionnaire.tsv')

# diabetes questionnaire data
diq_c <- nhanes('DIQ_C')
write_data(diq_c, 'DIQ_C_diabetes_questionnaire.tsv')

# tobacco use questionnaire data
smq_c <- nhanes('SMQ_C')
write_data(smq_c, 'SMQ_C_tobacco-use_questionnaire.tsv')

# medical conditions questionnaire
mcq_c <- nhanes('MCQ_C')
write_data(mcq_c, 'MCQ_C_medical-conditions_questionnaire.tsv')

# Rx questionnaire data
rx_c <- nhanes('RXQ_RX_C')
write_data(rx_c, 'RXQ_RX_C_rx-medications_questionnaire.tsv')

# balance exam data
bax_c <- nhanes('BAX_C')
write_data(bax_c, 'BAX_C_balance_exam.tsv')

# balance questionnaire data
baq_c <- nhanes('BAQ_C')
write_data(baq_c, 'BAX_C_balance_questionnaire.tsv')

# oral health questionnaire data
ohq_c <- nhanes('OHQ_C')
write_data(ohq_c, 'OHQ_C_oral-health_questionnaire.tsv')

# dentition exam data
dent_c <- nhanes('OHXDEN_C')
write_data(dent_c, 'OHXDEN_C_dentition_exam.tsv')

# perio lower exam data
perio_lower_c  <- nhanes('OHXPRL_C')
write_data(perio_lower_c, 'OHXPRL_C_perio-lower_exam.tsv')

# perio upper exam data
perio_lower_c  <- nhanes('OHXPRU_C')
write_data(perio_lower_c, 'OHXPRU_C_perio-upper_exam.tsv')

