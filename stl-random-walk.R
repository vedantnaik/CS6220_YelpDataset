#stl + random walk
require(forecast)
data<-read.csv("resources\\year_all_month_review_count_4bEjOyTaDG24SY5TxsaUNQ.csv")
oridata<-read.csv("resources\\year_all_month_review_count_4bEjOyTaDG24SY5TxsaUNQ.csv")

par(mfrow=c(2, 2))
data<-ts(data[,2],start = c(2005,1), end = c(2012,1),frequency = 12)
oridata <- ts(oridata[,2],start = c(2005,1),frequency = 12)
plot(oridata, main="Original Data")


fit <- stl(data, t.window=12, s.window="periodic", robust=TRUE)
eeadj <- seasadj(fit)
fcast <- forecast(fit, method="naive")
plot(fcast, ylab="New reviews")