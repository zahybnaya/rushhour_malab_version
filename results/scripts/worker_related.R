library(ggplot2)
library(plyr)
library(gridExtra)
library(Cairo)
library(reshape2)

####################################
# Activity plot for turkers
#######################################
setwd('~/gdrivezb9/rushhour/results/stage4/')
d=read.csv('trial_event_data.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=subset(d,d$assignmentid %in% c('3YW4XOSQKRTI0K0Z2YPDTDJVFABU1I','3M0BCWMB8W4W5M7WZVX3HDH1M3FBWL','3TS1AR6UQRM7SOIBWPBN8N9589Y7FV'))
d=subset(d, d$event != 'drag_start')

make_plot <- function (d){ 
  start_time = d[1,c('time')]
  one_hour = start_time + 60*60*1000
  two_hour = start_time + 120*60*1000
  g<-ggplot(d, aes(x=d$time, y=d$event)) + geom_point() + geom_vline(xintercept = one_hour,linetype=2) +
    ggtitle(d[1,c('subject')])+
    geom_vline(xintercept = two_hour, linetype=1) +
    annotate("text", x = one_hour, y = 3.5, label = "60m") +
    annotate("rect", xmin = one_hour-50, xmax = one_hour+50, ymin = 3.2, ymax = 3.8,alpha = .9) +
    annotate("text", x = two_hour, y = 3.5, label = "120m") + xlab('Time') +
    theme(axis.text.x=element_blank(),axis.ticks.x=element_blank())
  return(g)
}
d_worker = split(d, d$subject)
slplots=lapply(d_worker, make_plot)
do.call('grid.arrange',c(slplots, ncol = 2))

####################################
# Eligibility table for turkers
#######################################
setwd('~/gdrivezb9/rushhour/results/stage3/')
d=read.csv('trial_event_data.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=subset(d, d$event != 'drag_start')
wins=ddply(d, .(subject), function(x){return(length(unique(x[which(x$event=='win'),c('instance')])))})
names(wins)<-c('subject','solved')
surrenders=ddply(d, .(subject), function(x){return(length(unique(x[which(x$event=='surrender'),c('instance')])))})
names(surrenders)<-c('subject','surrendered')
fun<-function(x){
  df=data.frame(nrow(x[which(x$event=='BONUS_FAIL'),]),nrow(x[which(x$event=='BONUS_SUCCESS'),]))
  names(df)<-c('BONUS_FAIL','BONUS_SUCCESS')
  return(df)
}
bonuses=ddply(d, .(subject), fun)
commands=ddply(d, .(subject), function(x){return(paste('worker approve',x$assignmentid[1]))})
names(commands)<-c('subject','approve_command')
merge(merge(merge(bonuses,wins),surrenders),commands)

