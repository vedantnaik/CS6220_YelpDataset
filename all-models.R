# all - models


start_year = 2005
grainedview_start_year = 2012
end_year_training = 2013
end_year_ts = 2015
data_ylim = 20
filename = "table_amaze_2.csv"
data<-read.csv(filename)
oridata<-read.csv(filename)

par(mfrow = c(3,3))
holtdata<-ts(data[,2],start = c(start_year,1), end = c(end_year_training,1),frequency = 12)
autoarimadata<-ts(data[,2],start = c(start_year,1), end = c(end_year_training,1),frequency = 12)
oridata <- ts(oridata[,2],start = c(start_year,1),frequency = 12)

## auto arima

ARIMAfit <- auto.arima((autoarimadata), approximation=FALSE,trace=FALSE)
autoarima_pred <-  forecast(ARIMAfit, h=12)


acf(autoarima_pred$residuals)
pacf(autoarima_pred$residuals)
plot(autoarima_pred,type="l",xlim=c(grainedview_start_year,end_year_ts),ylim=c(1,data_ylim),xlab = "Year",ylab = "4bEjOyTaDG24SY5TxsaUNQ")
lines(10^(autoarima_pred$pred),col="blue")
lines(10^(autoarima_pred$pred+2*autoarima_pred$se),col="orange")
lines(10^(autoarima_pred$pred-2*autoarima_pred$se),col="orange")
lines(oridata, col ="orange")


## holt winters


holtdata <- window(holtdata, start=start_year, end=end_year_training)
additivefit <- hw(holtdata,seasonal="additive", damped = TRUE)
multifit <- hw(holtdata,seasonal="multiplicative")


acf(additivefit$residuals)
pacf(additivefit$residuals)

plot(multifit,ylab="4bEjOyTaDG24SY5TxsaUNQ",
     plot.conf=FALSE, fcol="white", xlab="Year", ylim=c(1,data_ylim), xlim=c(grainedview_start_year,end_year_ts))
lines(fitted(additivefit), col="red", lty=2)
lines(fitted(multifit), col="green", lty=2)
lines(additivefit$mean, type="o", col="red")
lines(multifit$mean, col="green")
lines(oridata, col ="orange")
print(accuracy(multifit, oridata))
print(accuracy(additivefit, oridata))

acf(multifit$residuals)
pacf(multifit$residuals)
