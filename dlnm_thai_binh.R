library(dlnm) ; library(readxl) ; library(mgcv) ; library(splines) ; library(tsModel)
vietnam <- read_excel("C:\\Users\\james\\OneDrive\\Documents\\Vietnam_Project\\100k_anglicised.xlsx",
                      col_names = TRUE)

thai_binh <- vietnam[vietnam$province == "Thái Bình",]
thai_binh <- thai_binh[thai_binh$year_month >= "2006-01-01",]
thai_binh <- na.omit(thai_binh)
thai_binh$time <- 1:nrow(thai_binh)
thai_binh$month <- format(thai_binh$year_month, "%B")

fqaic <- function(model) {
  loglik <- sum(dpois(model$y,model$fitted.values,log=TRUE))
  phi <- summary(model)$dispersion
  qaic <- -2*loglik + 2*summary(model)$df[3]*phi
  return(qaic)
}
aiclist <- list()
params <- list()
for (i in 1:8){
  for (j in 1:8){
    for (k in 1:40){
      vk <- equalknots(thai_binh$n_raining_days,nk=i)
      lk <- logknots(5,nk=j)
      cb <- crossbasis(thai_binh$n_raining_days,lag=5,argvar=list(fun="bs",degree=2,knots=vk),
                       arglag=list(knots=lk))
      m <- glm(Diarrhoea_cases~cb+ns(time,k)+month,family=quasipoisson(),thai_binh)
      aiclist[length(aiclist) + 1] <- fqaic(m)
      params[length(params) + 1] <- paste("i", i, "j", j, "k", k)
      print(paste("i", i, "j", j, "k", k))
    }   
  }
}

which.min(aiclist)
sort.list(aiclist, decreasing = TRUE)[5]
params[[2073]]
aiclist[[2073]]

vk <- equalknots(thai_binh$n_raining_days,nk=7)
lk <- logknots(4,nk=10)
cb <- crossbasis(thai_binh$n_raining_days,lag=5,argvar=list(fun="bs",degree=2,knots=vk),
                 arglag=list(knots=lk))
m <- glm(Diarrhoea_cases~cb+ns(time,33),family=quasipoisson(),thai_binh)

pred3dm <- crosspred(cb,m,at=0:29,cen=5.51) # median center - does it makes sense?
predslm <- crosspred(cb,m,by=0.2,bylag=1,cen=5.51)

plot(pred3dm,xlab="Number of raining days",zlab="RR",zlim=c(0.5, 3),xlim=c(0,29),
     ltheta=170,phi=15,theta = 25, lphi=30,main="GLM qAIC")
plot(predslm,"overall",ylab="RR",xlab="Number of raining days",xlim=c(0, 29),
     ylim=c(0.5,3.5),lwd=1.5,main="GLM qAIC")
# plot(predslgam1,var=29,xlab="Lag (days)",ylab="RR",ylim=c(0.9,1.4),lwd=1.5,
#      main="GAM with default penalties")

plot(pred3dm, "contour", xlab = "Number of raining days", key.title = title("RR"),
     plot.title = title("Contour plot GLM qAIC", xlab = "Number of raining days", ylab = "Lag"))


################################################################################
# GAM WITH DEFAULT PENALTIES

# DEFINE THE CROSS-BASIS
# NB: df IN argvar SET TO 9, AS INTERCEPT IS EXCLUDED AUTOMATICALLY
# (FOR COMPATIBILITY WITH INTERNAL METHOD)
cb_rain <- crossbasis(thai_binh$n_raining_days,lag=5,argvar=list(fun="ps",df=10),
                      arglag=list(fun="ps",df=10))
summary(cb_rain)

# DEFINE THE PENALTY MATRICES
cb_rain_Pen <- cbPen(cb_rain)

# RUN THE GAM MODEL AND PREDICT (TAKES ~34sec IN A 2.4 GHz PC)

gam1 <- gam(Diarrhoea_cases~cb_rain+s(time, bs = "ps",k = 10) + month,family=quasipoisson(),thai_binh,
            paraPen=list(cb_rain=cb_rain_Pen), method='REML')
plot(gam1, se = TRUE)
pred3dgam1 <- crosspred(cb_rain,gam1,at=0:29,cen=5.51) # median center - does it makes sense?
predslgam1 <- crosspred(cb_rain,gam1,by=0.2,bylag=1,cen=5.51)

# CHECK CONVERGENCE, SMOOTHING PARAMETERS AND EDF
gam1$converged
gam1$sp
# sum(gam1$edf[2:91])
gam.check(gam1)

# PLOTS
plot(pred3dgam1,xlab="Number of raining days",zlab="RR",zlim=c(0.5, 3),xlim=c(0,29),
     ltheta=170,phi=15,theta = 25, lphi=30,main="GAM with default penalties")
plot(predslgam1,"overall",ylab="RR",xlab="Number of raining days",xlim=c(0, 29),
     ylim=c(0.5,3.5),lwd=1.5,main="GAM with default penalties")
# plot(predslgam1,var=29,xlab="Lag (days)",ylab="RR",ylim=c(0.9,1.4),lwd=1.5,
#      main="GAM with default penalties")

plot(pred3dgam1, "contour", xlab = "Number of raining days", key.title = title("RR"),
     plot.title = title("Contour plot", xlab = "Number of raining days", ylab = "Lag"))


################################################################################
# GAM WITH DEFAULT PENALTIES AND MULTIPLE CBS - not good!

# DEFINE THE CROSS-BASIS
# NB: df IN argvar SET TO 9, AS INTERCEPT IS EXCLUDED AUTOMATICALLY
# (FOR COMPATIBILITY WITH INTERNAL METHOD)
cb_rain <- crossbasis(thai_binh$n_raining_days,lag=5,argvar=list(fun="ps",df=10),
                      arglag=list(fun="ps",df=10))
summary(cb_rain)

cb_flu <- crossbasis(thai_binh$Influenza_rates, lag = 5, argvar = list(fun = "ps", df = 10),
                     arglag = list(fun = "ps", df = 10))
summary(cb_flu)

# DEFINE THE PENALTY MATRICES
cb_rain_Pen <- cbPen(cb_rain)
cb_flu_Pen <- cbPen(cb_flu)

# RUN THE GAM MODEL AND PREDICT (TAKES ~34sec IN A 2.4 GHz PC)

gam2 <- gam(Diarrhoea_cases~cb_rain+cb_flu+s(time, bs = "ps", k = 10),family=quasipoisson(),thai_binh,
            paraPen=list(cb_rain = cb_rain_Pen, cb_flu = cb_flu_Pen), method='REML')
pred3dgam1 <- crosspred(cb_rain,gam2,at=0:29,cen=5.51) # median center - does it makes sense?
predslgam1 <- crosspred(cb_rain,gam2,by=0.2,bylag=1,cen=5.51)

# CHECK CONVERGENCE, SMOOTHING PARAMETERS AND EDF
gam2$converged
gam2$sp
sum(gam1$edf[2:91])
gam.check(gam2)

# PLOTS
plot(pred3dgam1,xlab="Number of raining days",zlab="RR",zlim=c(0.5, 3),xlim=c(0,29),
     ltheta=170,phi=15,theta = 25, lphi=30,main="GAM with default penalties")
plot(predslgam1,"overall",ylab="RR",xlab="Number of raining days",xlim=c(0, 29),
     ylim=c(0.5,3.5),lwd=1.5,main="GAM with default penalties")
# plot(predslgam1,var=29,xlab="Lag (days)",ylab="RR",ylim=c(0.9,1.4),lwd=1.5,
#      main="GAM with default penalties")

plot(pred3dgam1, "contour", xlab = "Number of raining days", key.title = title("RR"),
     plot.title = title("Contour plot", xlab = "Number of raining days", ylab = "Lag"))

################################################################################
# GLM WITH KNOTS SPECIFIED A PRIORI (GASPARRINI BMCmrm 2014)

# DEFINE THE CROSS-BASIS
vk <- equalknots(thai_binh$n_raining_days,nk=2)
lk <- logknots(5,nk=3)
cbglm1 <- crossbasis(thai_binh$n_raining_days, lag=5, argvar=list(fun="bs",degree=2,
                                                       knots=vk), arglag=list(knots=lk))
summary(cbglm1)

# RUN THE MODEL AND PREDICT
glm1 <- glm(Diarrhoea_cases~cbglm1+ns(time,3),family=quasipoisson(),thai_binh)
pred3dglm1 <- crosspred(cbglm1,glm1,at=0:29,cen=5.51)
predslglm1 <- crosspred(cbglm1,glm1,by=0.2,bylag=0.2,cen=5.51)
summary(glm1)
plot(glm1)


# PLOTS
plot(pred3dglm1,xlab="Number of raining days",zlab="RR",zlim=c(0.2, 1.8),xlim=c(0,29),
     ltheta=170,phi=15,theta = 25, lphi=30,main="GLM")
plot(predslglm1,"overall",ylab="RR",xlab="Number of raining days",xlim=c(0, 29),
     ylim=c(0.5,2.5),lwd=1.5,main="GLM")
# plot(predslgam1,var=29,xlab="Lag (days)",ylab="RR",ylim=c(0.9,1.4),lwd=1.5,
#      main="GAM with default penalties")

plot(pred3dglm1, "contour", xlab = "Number of raining days", key.title = title("RR"),
     plot.title = title("Contour plot (GLM)", xlab = "Number of raining days", ylab = "Lag"))
