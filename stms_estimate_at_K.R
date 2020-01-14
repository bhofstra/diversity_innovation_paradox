require("stm")
require("parallel")
require(gtools)
require(stringr)

input_name <- "data/proquest_dtm_full.rda"
root <- sub("\\..*", "", input_name)
load(input_name)

args = commandArgs(trailingOnly=TRUE)
print(args)

filename <- mixedsort(Sys.glob(paste(root, "_", args[1], "_model_iter_*.rda", sep="")))
if (length(filename) == 0) {
    i <- 0
} else {
    if (length(filename) != 1) {
        filename <- filename[length(filename)]
    }
    i <- as.numeric(str_match(filename, paste(root, "_", args[1], "_model_iter_(.*?).rda", sep=""))[, 2])
}
print(i)

while (TRUE) {
    print(paste("Iteration #", toString(i)))
    filename <- paste(root, "_", args[1], "_model_iter_", toString(i), ".rda", sep="")
    if (file.exists(filename)) {
        print("Load")
        flush.console()
        load(filename)
    } else if (i == 0) {
        print("Init")
        flush.console()
        mod <- stm(documents=proq.dtm$documents,
                   vocab=proq.dtm$vocab,
                   data=proq.dtm$meta,
                   K = as.numeric(args[1]),
                   prevalence=~thesisyear,
                   emtol=0.000015,
                   init.type="Spectral",
                   ngroups=1,
                   ncores=8,
                   max.em.its=0)
        mod$convergence$its <- 0
        save(mod, file=filename)
    } else {
        print("Normal")
        flush.console()
        mod <- stm(documents=proq.dtm$documents,
                   vocab=proq.dtm$vocab,
                   data=proq.dtm$meta,
                   K = as.numeric(args[1]),
                   prevalence=~thesisyear,
                   emtol=0.000015,
                   init.type="Custom",
                   model=mod,
                   ngroups=1,
                   ncores=8,
                   max.em.its=i)
        
        save(mod, file=filename)
    }
    i <- i + 1
}
