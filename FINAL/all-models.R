# all - models
require(forecast)

args <- commandArgs(trailingOnly = TRUE)
business_id <- args[1]
start_year <- as.numeric(args[2])
data_ylim <- as.numeric(args[3])

grainedview_start_year = 2010
end_year_training = 2013
end_year_ts = 2015

filename = paste("resources\\businesses\\",business_id,"\\",business_id, "_cartridge.csv", sep="")
data<-read.csv(filename)
oridata<-read.csv(filename)

par(mfrow = c(2,1))
holtdata<-ts(data[,2],start = c(start_year,1), end = c(end_year_training,1),frequency = 12)
autoarimadata<-ts(data[,2],start = c(start_year,1), end = c(end_year_training,1),frequency = 12)
oridata <- ts(oridata[,2],start = c(start_year,1),frequency = 12)

## auto arima

ARIMAfit <- auto.arima((autoarimadata), approximation=FALSE,trace=FALSE)
autoarima_pred <-  forecast(ARIMAfit, h=12)


#acf(autoarima_pred$residuals)
#pacf(autoarima_pred$residuals)
jpeg(paste("resources\\businesses\\",business_id,"\\",business_id,"_autoarima_plot.jpg",sep=""))
plot(autoarima_pred,type="l",xlim=c(grainedview_start_year,end_year_ts),ylim=c(1,data_ylim),xlab = "Year",ylab = business_id)
lines(10^(autoarima_pred$pred),col="blue")
lines(10^(autoarima_pred$pred+2*autoarima_pred$se),col="orange")
lines(10^(autoarima_pred$pred-2*autoarima_pred$se),col="orange")
lines(oridata, col ="orange")
dev.off()

## holt winters


holtdata <- window(holtdata, start=start_year, end=end_year_training)
additivefit <- hw(holtdata,seasonal="additive", damped = TRUE)
multifit <- hw(holtdata,seasonal="multiplicative", damped = TRUE)


#acf(additivefit$residuals)
#pacf(additivefit$residuals)

jpeg(paste("resources\\businesses\\",business_id,"\\",business_id,"_holtwinters_plot.jpg",sep=""))
plot(multifit,ylab=business_id,
     plot.conf=FALSE, fcol="white", xlab="Year", ylim=c(1,data_ylim), xlim=c(grainedview_start_year,end_year_ts))
lines(fitted(additivefit), col="red", lty=2)
lines(fitted(multifit), col="green", lty=2)
lines(additivefit$mean, col="red")
lines(multifit$mean, col="green")
lines(oridata, col ="orange")
print(accuracy(multifit, oridata))
print(accuracy(additivefit, oridata))

#acf(multifit$residuals)
#pacf(multifit$residuals)

#dev.copy(business_id)
dev.off()