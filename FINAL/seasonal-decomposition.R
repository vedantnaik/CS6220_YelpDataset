require(forecast)


args <- commandArgs(trailingOnly = TRUE)
bid <- args[1]

dataFile <- paste("resources\\businesses\\",bid,"\\",bid,"_cartridge.csv",sep="")
data<-read.csv(dataFile)
data<-ts(data[,2],start = c(2004,1),frequency = 12)

par(mfrow=c(2, 2))

# Seasonal decomposition
fit <- stl(data, s.window="period")

jpeg(paste("resources\\businesses\\",bid,"\\",bid,"_seasonal_plot.jpg",sep=""))
plot(fit, main="Seasonal decomposition")
dev.off()