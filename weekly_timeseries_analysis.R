library(forecast)
orig_data <- read.csv("D:\\CS6220-DM\\CS6220_YelpDataset\\resources\\4bEjOyTaDG24SY5TxsaUNQ_smoothed_data.csv")
ts_data <- ts(orig_data[,3], start=c(2007, 52), end=c(2014,1), frequency=53)
fit.arima <- auto.arima(ts_data, approximation = FALSE, trace = FALSE)
fore_val <- forecast(fit.arima, h=53)
plot(fore_val)

# fore_val <- forecast(fit.arima, h=53)
# plot(fore_val)

# 4bEjOyTaDG24SY5TxsaUNQ_smoothed_data.csv
# Fit model is ARIMA(0,1,1)(0,0,1)[53]

# 2e2e7WgqU1BnpxmQL5jbfw_smoothed_data.csv
# fit.arima <- auto.arima(ts_data, approximation = FALSE, trace = FALSE)
# Fit model is ARIMA(1,1,2)(1,0,0)[53]
# fore_val <- forecast(fit.arima, h=53)