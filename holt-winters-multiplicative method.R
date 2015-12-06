#holt-winters-multiplicative method
require(forecast)
data<-read.csv("resources\\year_all_month_review_count_4bEjOyTaDG24SY5TxsaUNQ.csv")
oridata<-read.csv("resources\\year_all_month_review_count_4bEjOyTaDG24SY5TxsaUNQ.csv")

par(mfrow=c(2, 2))
data<-ts(data[,2],start = c(2005,1), end = c(2012,1),frequency = 12)
oridata <- ts(oridata[,2],start = c(2005,1),frequency = 12)

data <- window(data, start=2005, end=2012)
fit1 <- hw(data,seasonal="additive")
fit2 <- hw(data,seasonal="multiplicative")

plot(fit2,ylab="Review count : 4bEjOyTaDG24SY5TxsaUNQ",
     plot.conf=FALSE, fcol="white", xlab="Year")
#lines(fitted(fit1), col="red", lty=2)
lines(fitted(fit2), col="green", lty=2)
#lines(fit1$mean, type="o", col="red")
lines(fit2$mean, col="green")
#legend("topleft",lty=1, pch=1, col=1:3, 
#       c("data","Holt Winters' Additive","Holt Winters' Multiplicative"))
lines(oridata, col ="orange")