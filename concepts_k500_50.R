
# Required packages thus far
rm(list = ls()) # Start with empty environment
require(dplyr)
#require(foreach)
require(tidyverse)
require(reshape2)
require(tidyr)
require(stm)
require(quanteda)
require(psych)
require(parallel)


#------------------------------------------------------------------------------------------


###########################
# 1. EXTRACT CONCEPTS from STM
###########################

# This will load an object name "mod" (see stms_estimate_at_K.R)
load("/yourpath/proquest_dtm_full_500_model_iter_20.rda")


frexconcepts <- labelTopics(mod, topics = 1:500, n = 500, frexweight = 0.50)
rm(mod)
save(frexconcepts, file = "/yourpath/frexconcepts_k500_050.rda")

