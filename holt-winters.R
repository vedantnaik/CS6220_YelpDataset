data<-read.csv("year_all_month_review_count_4bEjOyTaDG24SY5TxsaUNQ.csv")
data<-ts(data[,2],start = c(2005,1), end =  c(2012,1),frequency = 12)
# simple exponential - models level
fit <- HoltWinters(data, beta=FALSE, gamma=FALSE)
# double exponential - models level and trend
fit <- HoltWinters(data, gamma=FALSE)
# triple exponential - models level, trend, and seasonal components
fit <- HoltWinters(data)

# predictive accuracy
library(forecast)
accuracy(fit)

# predict next three future values
library(forecast)
#forecast(fit, 12)
par(mfrow=c(2,2))
plot(forecast(fit, 24))
data<-read.csv("year_all_month_review_count_4bEjOyTaDG24SY5TxsaUNQ.csv")
data<-ts(data[,2],start = c(2005,1), end =  c(2014,1),frequency = 12)
plot(data)