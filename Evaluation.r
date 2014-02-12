Evaluation <- function(f) {
data  <- read.csv(file = f,head = TRUE,sep = ",")
write.table(data$SURNAME,file = "Evaluation.dat",row.names = FALSE,col.names = FALSE)
}