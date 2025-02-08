library(nhanesA)
# nhanesTables('EXAM', 2011) # useful for viewing tables

# define function to save data file
write_data <- function(table, file_name) {
  fname <- paste0("../data/", file_name)
  write.table(table, file=fname, quote=FALSE, sep='\t', row.names=FALSE)
}

# demographics data
demo_g <- nhanes('DEMO_G')
write_data(demo_g, 'DEMO_G_demographics.tsv')

# perio exam data
perio_g  <- nhanes('OHXPER_G')
write_data(perio_g, 'OHXPER_G_perio.tsv')

# dentition exam data
dent_g <- nhanes('OHXDEN_G')
write_data(dent_g, 'OHXDEN_G_dentition.tsv')

# oral health recommendation exam data
rec_g <- nhanes('OHXREF_G')
write_data(rec_g, 'OHXREF_G_recommendation.tsv')

# oral healh questionnaire data
ohq_g <- nhanes('OHQ_G')
write_data(ohq_g, 'OHQ_G_oral_health_questionnaire.tsv')

# Rx questionnaire data
rx_g <- nhanes('RXQ_RX_G')
write_data(rx_g, 'RXQ_RX_G_rx_medications.tsv')

# cigarette use questionnaire data
cig_g <- nhanes('SMQ_G')
write_data(cig_g, 'SMQ_G_cigarette_use.tsv')

# smoking - tobacco use questionnaire data
tobacco_g <- nhanes('SMQRTU_G')
write_data(tobacco_g, 'SMQRTU_G_smoking-recent_tobacco_use.tsv')

  
# cognitive functioning questionnaire data
cfq_g <- nhanes('CFQ_G')
write_data(cfq_g, 'CFQ_G_cognitive_functioning.tsv')