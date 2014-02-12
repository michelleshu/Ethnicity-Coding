Preprocessing <- function(f) {
data  <- read.csv(file = f,head = TRUE,sep = ",")
index <- !is.na(data$RA.Confidence.Level)
data  <- data[index,]
write.table(data$SURNAME,file = "Names.dat",row.names = FALSE,col.names = FALSE)
write.table(data$TRIBE.ETHNIC.GROUP,file = "Ethnicity.dat",row.names = FALSE,col.names = FALSE)
write.table(data$RA.Confidence.Level,file = "Confidence.dat",row.names = FALSE,col.names = FALSE)
}