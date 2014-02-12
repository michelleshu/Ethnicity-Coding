args <- commandArgs(trailingOnly = TRUE)
hh   <- paste(unlist(args),collapse=' ')
listoptions  <- unlist(strsplit(hh,'--'))[-1]
options.args <- sapply(listoptions,function(x){
	     unlist(strsplit(x, ' '))[-1]
             })
options.names <- sapply(listoptions,function(x){
  	      option <-  unlist(strsplit(x, ' '))[1]
	      })
names(options.args) <- unlist(options.names)

source("Preprocessing.r")
Preprocessing(args[2])

source("Evaluation.r")
Evaluation(args[3])
