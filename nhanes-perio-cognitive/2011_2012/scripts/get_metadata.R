library(nhanesA)
# nhanesTables('EXAM', 2011) # useful for viewing tables

# define function to save metadata file
write_metadata <- function(meta_vars, file_name) {
  fname <- paste0("../metadata/", file_name)
  write.table(meta_vars, file=fname, quote=FALSE, sep='\t', row.names=FALSE)
}

# define function to write metadata value mappings
write_meta_values <- function(nh_table, meta_vars) {
  # get codes from the metadata variable
  codes <- nhanesTranslate(nh_table, meta_vars$Variable.Name)
  
  # save each code to file
  for (n in names(codes)) {
    fname <- paste0("../metadata/metadata_values/", n, ".tsv")
    write.table(codes[[n]], file = fname, quote=FALSE, sep='\t', row.names=FALSE)
  }
}

# save demographics metadata
demo_vars <- nhanesTableVars('DEMO', 'DEMO_G')
write_metadata(demo_vars, 'demo_meta.tsv')
write_meta_values('DEMO_G', demo_vars)

# save perio metadata
perio_vars  <- nhanesTableVars('EXAM', 'OHXPER_G')
write_metadata(perio_vars, 'perio_meta.tsv')
write_meta_values('OHXPER_G', perio_vars)
  
# save dentition metadata
dent_vars <- nhanesTableVars('EXAM', 'OHXDEN_G')
write_metadata(dent_vars, 'dentition_meta.tsv')
write_meta_values('OHXDEN_G', dent_vars)

# save Oral Health - Recommendation of Care metadata
rec_vars <- nhanesTableVars('EXAM', 'OHXREF_G')
write_metadata(rec_vars, 'recommendation_meta.tsv')
write_meta_values('OHXREF_G', rec_vars)

# save Oral Health questionnaire metadata
ohq_vars <- nhanesTableVars('Q', 'OHQ_G')
write_metadata(ohq_vars, 'oral_health_questionnaire_meta.tsv')
write_meta_values('OHQ_G', ohq_vars)

# save perscription medication data
rx_vars <- nhanesTableVars('Q', 'RXQ_RX_G')
write_metadata(rx_vars, 'rx_meta.tsv')
write_meta_values('RXQ_RX_G', rx_vars)

# save Smoking - Cigarette Use metadata
cig_vars <- nhanesTableVars('Q', 'SMQ_G')
write_metadata(cig_vars, 'cigarette_meta.tsv')
write_meta_values('SMQ_G', cig_vars)

# save Smoking - Recent Tobacco Use (SMQRTU_G) 
tobacco_vars <-  nhanesTableVars('Q', 'SMQRTU_G')
write_metadata(tobacco_vars, 'tobacco_meta.tsv')
write_meta_values('SMQRTU_G', tobacco_vars)

# save Cognitive Functioning (CFQ_G) metadata
cfq_vars <- nhanesTableVars('Q', 'CFQ_G')
write_metadata(cfq_vars, 'cognitive_functioning_meta.tsv')
write_meta_values('CFQ_G', cfq_vars)
