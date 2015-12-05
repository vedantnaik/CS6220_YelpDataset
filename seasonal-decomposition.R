require(forecast)
data<-read.csv("resources\\year_all_month_review_count_4bEjOyTaDG24SY5TxsaUNQ.csv")
data<-ts(data[,2],start = c(2005,1),frequency = 12)

par(mfrow=c(2, 2))

# Seasonal decomposition
fit <- stl(data, s.window="period")
plot(fit, main="Seasonal decomposition")