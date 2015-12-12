require(forecast)
data<-read.csv("resources\\year_all_review_count_zt1TpTuJ6y9n551sw9TaEg.csv")
data<-ts(data[,2],start = c(2007,1),frequency = 12)

par(mfrow=c(2, 2))

# Seasonal decomposition
fit <- stl(data, s.window="period")
plot(fit, main="Seasonal decomposition")