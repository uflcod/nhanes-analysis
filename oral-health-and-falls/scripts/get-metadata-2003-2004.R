library(nhanesA)
# info about nhanesA variables
# NHANES data are available in 5 categories
# - Demographics (DEMO)
# - Dietary (DIET)
# - Examination (EXAM)
# - Laboratory (LAB)
# - Questionnaire (Q)

# # info about nhanesA usage
# - https://cran.r-project.org/web/packages/nhanesA/vignettes/Introducing_nhanesA.html
# - https://cran.r-project.org/web/packages/nhanesA/nhanesA.pdf
# - library: https://ehsanx.github.io/SPPH504007SurveyData/docs/importing-nhanes-to-r.html

# Using Survey Weights with nhanesA
# - https://cran.r-project.org/web/packages/nhanesA/vignettes/UsingSurveyWeights.html

# nhanesTables('Q', 2003, namesonly=TRUE) # lists all questionnaires
# nhanesTables('EXAM', 2003) # lists exam metadata
# page(nhanesTables('EXAM', 2003), method="print") # prints output to separate tab

# define function to save metadata file
write_metadata <- function(meta_vars, file_name) {
  fname <- paste0("../data/2003-2004/metadata/", file_name)
  write.table(meta_vars, file=fname, quote=FALSE, sep='\t', row.names=FALSE)
}

# define function to write metadata value mappings
write_meta_values <- function(nh_table, meta_vars) {
  # get codes from the metadata variable
  codes <- nhanesTranslate(nh_table, meta_vars$Variable.Name)
  
  # save each code to file
  for (n in names(codes)) {
    # create subdirectory for variables
    output_dir <- paste0("../data/2003-2004/metadata/metadata_values/", nh_table, "/")
    
    # check if directory extists
    if (!dir.exists(output_dir)) {
      dir.create(output_dir)
    } 
    
    # fname <- paste0("../data/2003-2004/metadata/metadata_values/", nh_table, "_", n, ".tsv")
    fname <- paste0(output_dir, n, ".tsv")
    write.table(codes[[n]], file = fname, quote=FALSE, sep='\t', row.names=FALSE)
  }
}

# save demographics metadata
demo_c_vars <- nhanesTableVars('DEMO', 'DEMO_C')
write_metadata(demo_c_vars, 'DEMO_C_demographics_meta.tsv')
write_meta_values('DEMO_C', demo_c_vars)

# food security questionnaire metadata
fsq_c_vars <- nhanesTableVars('Q', 'FSQ_C')
write_metadata(fsq_c_vars, 'FSQ_C_food-security_questionnaire_meta.tsv')
write_meta_values('FSQ_C', fsq_vars)

# diabetes questionnaire metadata
diq_c_vars <- nhanesTableVars('Q', 'DIQ_C')
write_metadata(diq_c_vars, 'DIQ_C_diabetes_questionnaire_meta.tsv')
write_meta_values('DIQ_C', diq_c_vars)

# tobacco use questionnaire metadata
smq_c_vars <- nhanesTableVars('Q', 'SMQ_C')
write_metadata(smq_c_vars, 'SMQ_C_tobacco-use_questionnaire_meta.tsv')
write_meta_values('SMQ_C', smq_c_vars)

# medical conditions questionnaire
mcq_c_vars <- nhanesTableVars('Q', 'MCQ_C')
write_metadata(mcq_c_vars, 'MCQ_C_medical-conditions_questionnaire_meta.tsv')
write_meta_values('MCQ_C', mcq_c_vars)

# Rx questionnaire metadata
rx_c_vars <- nhanesTableVars('Q', 'RXQ_RX_C')
write_metadata(rx_c_vars, 'RXQ_RX_C_medications_questionnaire_meta.tsv')
write_meta_values('RXQ_RX_C', rx_c_vars)

# balance exam data
bax_c_vars <- nhanesTableVars('EXAM', 'BAX_C')
write_metadata(bax_c_vars, 'BAX_C_balance_exam_meta.tsv')
write_meta_values('BAX_C', bax_c_vars)

# balance questionnaire metadata
baq_c_vars <- nhanesTableVars('Q', 'BAQ_C')
write_metadata(baq_c_vars, 'BAQ_C_balance_questionnaire_meta.tsv')
write_meta_values('BAQ_C', baq_c_vars)

# oral health questionnaire metadata
ohq_c_vars <- nhanesTableVars('Q', 'OHQ_C')
write_metadata(ohq_c_vars, 'OHQ_C_oral-health_questionnaire_meta.tsv')
write_meta_values('OHQ_C', ohq_c_vars)

# dentition exam metadata
dent_c_vars <- nhanesTableVars('EXAM', 'OHXDEN_C')
write_metadata(dent_c_vars, 'OHXDEN_C_dentition_exam_meta.tsv')
write_meta_values('OHXDEN_C', dent_c_vars)

# perio lower exam data
perio_lower_c_vars  <- nhanesTableVars('EXAM', 'OHXPRL_C')
write_metadata(perio_lower_c_vars, 'OHXPRL_C_perio-lower_exam_meta.tsv')
write_meta_values('OHXPRL_C', perio_lower_c_vars)

# perio upper exam data
perio_lower_c_vars  <- nhanesTableVars('EXAM', 'OHXPRU_C')
write_metadata(perio_lower_c_vars, 'OHXPRU_C_perio-upper_exam_meta.tsv')
write_meta_values('OHXPRU_C', perio_lower_c_vars)
