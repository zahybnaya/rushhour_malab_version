library(ggplot2)
library(plyr)
library(gridExtra)
library(Cairo)
library(reshape2)

setwd("~/gdrivezb9/rushhour/results/pilot")
figpath<-'../../docs/ccn/figures'

paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
#sort by experiment design
lvls_e  = unique(paths[order(nchar(paths$instance),paths$instance),c('instance')])
#sort by solution length
lvls_sl = unique(paths[order(paths$optimal_length),c('instance')])
mean_sem <- function(x) {
  meanx=mean(x)
  sem=sd(x)/sqrt(length(x))
  return(data.frame("y"=meanx, "ymin"=meanx-sem/2, "ymax"=meanx+sem/2))
}

mean_sem_ <- function(x) {
  meanx=mean(x)
  sem=sd(x)/sqrt(length(x))
  return(data.frame("mean"=meanx, "sem"=sem/2))
}


######################################################## 
# Plot  Error ratio of models.
#######################################################
setwd("~/gdrivezb9/rushhour/results/lrta")
lrta=read.csv('lrta_phs.csv', header = TRUE)
alg_lvls=c('lrta0','lrta1','lrta2','lrta3','lrta4','lrta5','A*h:min_manhattan_distancef:0*(g+1)+1histop:<lambda>lapse:0slapse:0reca:100.0','A*h:min_manhattan_distancef:0*(g+1)+1.5histop:<lambda>lapse:0slapse:0reca:100.0','A*h:magsizef:0*(g+1)+1histop:<lambda>lapse:0slapse:0reca:100.0')
alg_lbl=c('lrta0','lrta1','lrta2','lrta3','lrta4','lrta5','manhat','1.5manhat','magsize')
lrta$instance <- factor(lrta$instance, levels = lvls_e, labels = 1:length(lvls_e))
lrta$alg <- factor(lrta$alg, levels = alg_lvls , labels = alg_lvls)

lrta=subset(lrta, step==1)
lrta$error_ratio = lrta$alg_path/lrta$optimal_path
lrta$learning_iters = lrta$learning_iters*lrta$h_weight
lrta$learning_iters = factor(lrta$learning_iters)
ggplot(lrta, aes(x=instance, y=error_ratio)) + geom_bar(stat = 'identity',position = 'dodge',aes(fill=alg),size=2) +
  ggtitle('Effect of learning on errors') 



######################################################## 
# Plot 33:   Error ratio of models.
#######################################################
setwd("~/gdrivezb9/rushhour/results/lrta")
lrta=read.csv('lrta_phs.csv', header = TRUE)
alg_lvls=c('lrta0','lrta1','lrta2','lrta3','lrta4','lrta5','A*h:min_manhattan_distancef:0*(g+1)+1histop:<lambda>lapse:0slapse:0reca:100.0','A*h:min_manhattan_distancef:0*(g+1)+1.5histop:<lambda>lapse:0slapse:0reca:100.0','A*h:magsizef:0*(g+1)+1histop:<lambda>lapse:0slapse:0reca:100.0')
alg_lbl=c('lrta0','lrta1','lrta2','lrta3','lrta4','lrta5','manhat','1.5manhat','magsize')
lrta$instance <- factor(lrta$instance, levels = lvls_e, labels = 1:length(lvls_e))
lrta$alg <- factor(lrta$alg, levels = alg_lvls , labels = alg_lvls)

lrta=subset(lrta, step==1)
lrta$error_ratio = lrta$alg_path/lrta$optimal_path
lrta$learning_iters = lrta$learning_iters*lrta$h_weight
lrta$learning_iters = factor(lrta$learning_iters)
ggplot(lrta, aes(x=instance, y=error_ratio)) + geom_bar(stat = 'identity',position = 'dodge',aes(fill=learning_iters),size=2) +
  scale_fill_grey(start = .8, end = .0) + theme_bw() + 
  ggtitle('Effect of learning on errors') 


########################################################### 
# Plot 34:   Scatter plot of average errors and algorithms
###########################################################
setwd("~/gdrivezb9/rushhour/results/pilot")
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$instance=factor(paths$instance, levels = lvls_e, labels = 1:length(lvls_e))
paths=subset(paths,paths$complete=='True')
paths$human_error_ratio = paths$human_length/paths$optimal_length
t1=aggregate(paths, by = list('instance'=paths$instance), FUN='sd')$human_error_ratio
t2=aggregate(paths, by = list('instance'=paths$instance), FUN='length')$human_error_ratio
sem=t1/sqrt(t2)
paths_ag=aggregate(paths, by = list('instance'=paths$instance), FUN='mean')
paths_ag=paths_ag[,c('instance','human_error_ratio')]
paths_ag$sem=sem
setwd("~/gdrivezb9/rushhour/results/lrta")
lrta=read.csv('lrta_phs.csv', header = TRUE)
alg_lvls=c('lrta0','lrta1','lrta2','lrta3','lrta4','lrta5','A*h:min_manhattan_distancef:0*(g+1)+1histop:<lambda>lapse:0slapse:0reca:100.0','A*h:min_manhattan_distancef:0*(g+1)+1.5histop:<lambda>lapse:0slapse:0reca:100.0','A*h:magsizef:0*(g+1)+1histop:<lambda>lapse:0slapse:0reca:100.0')
alg_lbl=c('lrta0','lrta1','lrta2','lrta3','lrta4','lrta5','manhat','1.5manhat','magsize')
lrta$instance <- factor(lrta$instance, levels = lvls_e, labels = 1:length(lvls_e))
lrta$alg <- factor(lrta$alg, levels = alg_lvls , labels = alg_lbl)
lrta=subset(lrta, step==1)
lrta$alg_error_ratio = lrta$alg_path/lrta$optimal_path
lrta$learning_iters = lrta$learning_iters*lrta$h_weight
lrta$learning_iters = factor(lrta$learning_iters)
d=merge(lrta,paths_ag, by = 'instance')
ggplot(d, aes(x=human_error_ratio, y=alg_error_ratio)) + geom_point(aes(color=alg),size=2) + 
  + geom_text(cor(d$human_error_ratio,d$alg_error_ratio, method = 'spearman'))+
  facet_grid(. ~ alg) + geom_abline(slope = 1) + scale_fill_grey(start = .8, end = .0) + 
  geom_errorbar(aes(ymin=alg_error_ratio-sem, ymax=alg_error_ratio+sem))+
  theme_bw() + ggtitle('Error ratio of alg/humans') + ylim(1,5)


########################################################### 
# Plot 34.1:   Scatter plot of average errors and algorithms (LRTA5)
###########################################################
setwd("~/gdrivezb9/rushhour/results/pilot")
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$instance=factor(paths$instance, levels = lvls_e, labels = 1:length(lvls_e))
paths=subset(paths,paths$complete=='True')
paths$human_error_ratio = paths$human_length/paths$optimal_length
paths_ag=aggregate(paths, by = list('instance'=paths$instance), FUN='mean')
paths_ag=paths_ag[,c('instance','human_error_ratio')]
setwd("~/gdrivezb9/rushhour/results/lrta")
lrta=read.csv('lrta.csv', header = TRUE)
lrta$instance <- factor(lrta$instance, levels = lvls_e, labels = 1:length(lvls_e))
lrta=subset(lrta, step==1)
lrta=subset(lrta, lrta$alg=='lrta5')
lrta$alg_error_ratio = lrta$alg_path/lrta$optimal_path
lrta$learning_iters = lrta$learning_iters*lrta$h_weight
lrta$learning_iters = factor(lrta$learning_iters)
d=merge(lrta,paths_ag, by = 'instance')

ggplot(d, aes(x=human_error_ratio, y=alg_error_ratio)) + geom_point(aes(color=learning_iters),size=2) +
  geom_abline(slope = 1) + scale_fill_grey(start = .8, end = .0) + theme_bw() + 
  ggtitle('Error ratio of alg/humans') 



####
#  Plot 29: Bar plot of which model explains difficulty better? (Pure H, manhattan, 0 heuristics.) 
#### 
setwd("~/gdrivezb9/rushhour/results/pilot")
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$instance=factor(paths$instance, levels = lvls_e, labels = 1:length(lvls_e))
paths=subset(paths,paths$complete=='True' & !(paths$instance %in% c('22','23','24')))

p1<-ggplot(paths, aes(x=paths$instance, y=paths$human_length)) + stat_summary(geom='bar',fun.y = 'mean') +
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2) +
  stat_summary(geom='bar', aes(y=paths$optimal_length+1), fun.y = 'mean', fill='black')
p3<-ggplot(paths, aes(x=paths$instance, y=paths$rt)) + stat_summary(geom='bar',fun.y = 'mean') +
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)

d=read.csv('rid.csv', header = TRUE, sep=',',stringsAsFactors=F)
d$instance=factor(d$puzzle, levels = lvls_e, labels = 1:length(lvls_e))

p2<-ggplot(d, aes(x=instance)) + stat_summary(aes(y=expanded), geom='bar', fun.y = 'mean') + 
  facet_grid(alg ~ . ,scales = 'free')+
  stat_summary(aes(y=expanded), geom='errorbar', fun.data = mean_sem, width=0.2) 
grid.arrange(p1,p2,ncol = 1)

########
## P30 : Scatter plots of Spearman corellations between expanded nodes and error_ratios
##########
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$instance=factor(paths$instance, levels = lvls_e, labels = 1:length(lvls_e))
paths=subset(paths,paths$complete=='True' & !(paths$instance %in% c('22','23','24')))
paths$optimal_length<-paths$optimal_length+1
rid=read.csv('rid.csv', header = TRUE, sep=',',stringsAsFactors=F)
rid$instance=factor(rid$puzzle, levels = lvls_e, labels = 1:length(lvls_e))
d=ddply(rid, .(instance,alg), function(x){return(mean(x$expanded))})
names(d)<-c('instance','alg','expanded')
d1=merge(d,paths,by = c('instance'))
d1$error_ratio=d1$human_length/d1$optimal_length
d1$error_n=d1$human_length-d1$optimal_length
s<-ddply(d1, .(subject, alg), function(x){return(cor(x$expanded, x$error_ratio, method = 'spearman'))} )
names(s)<-c('subject','alg','spearman')
dc<-dcast(s, subject ~ alg)
names(dc)<-c('subject', 'H','H+G','G')
p1<-ggplot(dc, aes(x=dc$H, y=dc$`H+G`)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ 
  geom_abline(slope = 1, intercept = 0) + xlab('heuristics only') + ylab(' heuristics + distance')
p2<-ggplot(dc, aes(x=dc$H, y=dc$G)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ geom_abline(slope = 1, intercept = 0)+
 geom_abline(slope = 1, intercept = 0) + xlab('heuristics only') + ylab(' distance only')
p3<-ggplot(dc, aes(x=dc$`H+G`, y=dc$G)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ geom_abline(slope = 1, intercept = 0)+
  geom_abline(slope = 1, intercept = 0) + xlab('heuristics + distance') + ylab(' distance only')
Cairo(file=paste(figpath,"/p30.png",sep=''), 
      type="png",
      units="px", 
      width=1124, 
      height=320,
      pointsize=12, 
      dpi=72*2)
grid.arrange(p1,p2,p3, ncol=3, top='Spearman coefficients of #expaned and error ratio')
dev.off()


########
## P31 : Scatter plots of Spearman corellations between expanded nodes and RT
##########
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$instance=factor(paths$instance, levels = lvls_e, labels = 1:length(lvls_e))
paths=subset(paths,paths$complete=='True' & !(paths$instance %in% c('22','23','24')))
paths$optimal_length<-paths$optimal_length+1
rid=read.csv('rid.csv', header = TRUE, sep=',',stringsAsFactors=F)
rid$instance=factor(rid$puzzle, levels = lvls_e, labels = 1:length(lvls_e))
d=ddply(rid, .(instance,alg), function(x){return(mean(x$expanded))})
names(d)<-c('instance','alg','expanded')
d1=merge(d,paths,by = c('instance'))
d1$error_ratio=d1$human_length/d1$optimal_length
d1$error_n=d1$human_length-d1$optimal_length
s<-ddply(d1, .(subject, alg), function(x){return(cor(x$expanded, x$rt, method = 'spearman'))} )
names(s)<-c('subject','alg','spearman')
dc<-dcast(s, subject ~ alg)
names(dc)<-c('subject', 'H','H+G','G')
p1<-ggplot(dc, aes(x=dc$H, y=dc$`H+G`)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ 
  geom_abline(slope = 1, intercept = 0) + xlab('heuristics only') + ylab(' heuristics + distance')
p2<-ggplot(dc, aes(x=dc$H, y=dc$G)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ geom_abline(slope = 1, intercept = 0)+
  geom_abline(slope = 1, intercept = 0) + xlab('heuristics only') + ylab(' distance only')
p3<-ggplot(dc, aes(x=dc$`H+G`, y=dc$G)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ geom_abline(slope = 1, intercept = 0)+
  geom_abline(slope = 1, intercept = 0) + xlab('heuristics + distance') + ylab(' distance only')
Cairo(file=paste(figpath,"/p31.png",sep=''), 
      type="png",
      units="px", 
      width=1124, 
      height=320,
      pointsize=12, 
      dpi=72*2)
grid.arrange(p1,p2,p3, ncol=3, top='Spearman coefficients of #expaned and Response times')
dev.off()



########
## P32 : Scatter plots of Spearman corellations between Solution lengths
##########
setwd("~/gdrivezb9/rushhour/results/pilot")
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$instance=factor(paths$instance, levels = lvls_e, labels = 1:length(lvls_e))
paths=subset(paths,paths$complete=='True' & !(paths$instance %in% c('22','23','24')))
paths$optimal_length<-paths$optimal_length+1
rid=read.csv('rid.csv', header = TRUE, sep=',',stringsAsFactors=F)
rid$instance=factor(rid$puzzle, levels = lvls_e, labels = 1:length(lvls_e))
d=ddply(rid, .(instance,alg), function(x){return(mean(x$path))})
names(d)<-c('instance','alg','path_length')
d1=merge(d,paths,by = c('instance'))
d1$error_ratio=d1$human_length/d1$optimal_length
d1$error_n=d1$human_length-d1$optimal_length
s<-ddply(d1, .(subject, alg), function(x){return(cor(x$path_length, x$human_length, method = 'spearman'))} )
names(s)<-c('subject','alg','spearman')
dc<-dcast(s, subject ~ alg)
names(dc)<-c('subject', 'H','H+G','G')
p1<-ggplot(dc, aes(x=dc$H, y=dc$`H+G`)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ 
  geom_abline(slope = 1, intercept = 0) + xlab('heuristics only') + ylab(' heuristics + distance')
p2<-ggplot(dc, aes(x=dc$H, y=dc$G)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ geom_abline(slope = 1, intercept = 0)+
  geom_abline(slope = 1, intercept = 0) + xlab('heuristics only') + ylab(' distance only')
p3<-ggplot(dc, aes(x=dc$`H+G`, y=dc$G)) + geom_point() + xlim(-1,1) + ylim(-1,1)+ geom_abline(slope = 1, intercept = 0)+
  geom_abline(slope = 1, intercept = 0) + xlab('heuristics + distance') + ylab(' distance only')
Cairo(file=paste(figpath,"/p31.png",sep=''), 
      type="png",
      units="px", 
      width=1124, 
      height=320,
      pointsize=12, 
      dpi=72*2)
grid.arrange(p1,p2,p3, ncol=3, top='Spearman coefficients of Solution lengths')
dev.off()



####
# Plot 26.X: bar plot of expaned nodes 
#####
setwd("~/gdrivezb9/rushhour/src/")
d=read.csv('data_456', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(d, aes(x=puzzle, y=expanded)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=generated)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=close)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=open)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)

########
## Plot 27.X: bar plot of expaned nodes (pure heuristics) 
###########
d=read.csv('data_456_pureh', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(d, aes(x=puzzle, y=expanded)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=generated)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=close)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=open)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
#solution length
ggplot(d, aes(x=puzzle, y=length)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)


###########
## No heuristics. 
########
## Plot 28.X: bar plot of expaned nodes (no heuristics) 
###########

###########
d=read.csv('data_456_0', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(d, aes(x=puzzle, y=expanded)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=generated)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=close)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)
ggplot(d, aes(x=puzzle, y=open)) + stat_summary(geom='bar', fun.y = 'mean') + 
  stat_summary(geom='errorbar', fun.data = mean_sem, width=0.2)




########
# TMP plot
#########
setwd("~/gdrivezb9/rushhour/results/pilot")
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths=subset(paths, complete=='True' & paths$instance %in% c('Jam-4','Jam-5','Jam-6'))
paths$instance=factor(paths$instance, levels = lvls_e, labels = 1:length(lvls_e))
g<-ggplot(paths, aes(x = paths$instance)) + 
  stat_summary(geom='bar', aes(y=paths$human_length), fun.y = 'mean', fill='wheat4')+
  stat_summary(geom='bar', aes(y=paths$optimal_length+1), fun.y = 'mean', fill='black')+
  stat_summary(geom='errorbar', aes(y=paths$human_length), fun.data = mean_sem, width=0.4)+
  xlab('puzzle') + ylab('#moves') + theme(text = element_text(size=20))
g


###
# Plot 1: Scatter plot of Human solution length, vs Optimal solution length, shape/color by instance.
###
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=subset(paths, paths$complete=='True')
d$instance=factor(d$instance, levels = lvls_sl)
ggplot(d, aes(x=d$optimal_length))+ geom_point(stroke=2,aes(y=d$human_length, shape=d$subject))+
  scale_shape_manual(values = 1:11, guide=FALSE)+
   xlab('Optimal solution') + ylab('Human solution')

########
## Plot 2: Bar Plot of instances optimal lengths.
#######
paths=read.csv('paths.fake.nodes.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=aggregate(paths, by = list(instance=paths$instance), FUN=mean)[,c('instance', 'optimal_length','nodes_expanded')]
d$instance=factor(d$instance, levels = lvls_e)
ggplot(d, aes(x = d$instance)) +geom_bar(stat="identity",aes(y = d$optimal_length)) + 
  ggtitle('Optimal solution lengths per instance')+ xlab('Instance') + ylab('Optimal length')


######
## Plot 2.1: Bar Plot of instances expanded nodes.
#######
paths=read.csv('paths.fake.nodes.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=aggregate(paths, by = list(instance=paths$instance), FUN=mean)[,c('instance', 'optimal_length','nodes_expanded')]
d$instance=factor(d$instance, levels = lvls_e)


######
## Plot 2.2: Bar Plot of instances human length.
#######
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths=subset(paths, complete=='True')
paths$instance=factor(paths$instance, levels = lvls_e, labels = 1:length(lvls_e))
g<-ggplot(paths, aes(x = paths$instance)) + 
  stat_summary(geom='bar', aes(y=paths$human_length), fun.y = 'mean', fill='wheat4')+
  stat_summary(geom='bar', aes(y=paths$optimal_length+1), fun.y = 'mean', fill='black')+
  stat_summary(geom='errorbar', aes(y=paths$human_length), fun.data = mean_sem, width=0.4)+
  xlab('puzzle') + ylab('#moves') + theme(text = element_text(size=20))
Cairo(file=paste(figpath,"/p2_2c.png",sep=''), 
      type="png",
      units="px", 
      width=1124, 
      height=320,
      pointsize=12*2, 
      dpi=72*2)
g
dev.off()

###
# Plot 3: scatter plot of response-time as move number, by subject
###
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(moves, aes(x=moves$move_number)) + geom_point(aes(y=moves$rt, color=subject)) +
  scale_color_manual(values=1:11, guide=FALSE)+
  ggtitle("Response Times") + xlab('move number') + ylab('Seconds') + ylim(0,90)


###
# Plot 3.1: scatter plot of response-time as move number, by subject
###
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
g<-ggplot(moves, aes(x=moves$move_number)) + geom_point(aes(y=moves$rt)) +
   xlab('move number') + ylab('Seconds') + ylim(0,90) +
  theme(text = element_text(size=18))
Cairo(file=paste(figpath,"/p3_1.png",sep=''), 
      type="png",
      units="px", 
      width=770, 
      height=350,
      pointsize=12*2, 
      dpi=72*2)
g
dev.off()


#######
#  Plot 3.2: Spearman correlations of RT
#########
require(plyr)
cor_move_rt <- function(xx)
{
  return(data.frame(COR = cor(xx$move_number, xx$rt, method = "spearman")))
}
cor_dist_rt <- function(xx)
{
  return(data.frame(COR = cor(xx$distance_to_goal, xx$rt, method = "spearman")))
}

d=ddply(moves, .(subject), cor_dist_rt)
d$type='distance to goal'
d1=ddply(moves, .(subject), cor_move_rt)
d1$type='move#'
d2=rbind(d,d1)
cors=ddply(d2,.(type), function(x){return(mean_sem(x$COR))})
cors$sem=(cors$ymax-cors$ymin)/2
ggplot(d2, aes(x=type, y=COR)) + stat_summary(geom = 'bar', fun.data = mean_sem) +
  stat_summary(geom = "errorbar", fun.data = mean_sem, width=0.22) 

###
# Plot 4: Bar plot of how many moves on each move number
###
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(moves, aes(x=moves$move_number, fill=instance)) + geom_bar() + ggtitle("occurences per move_number")

####
# Plot 5: Bar plot of number of (good, neutral, wrong) moves
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Same',ifelse(progress>0,'Closer','Further')))
ggplot(moves,aes(x=moves$category)) + geom_bar() + ggtitle('Moves Category') + xlab('Moving closer/same/further from solution')

####
# Plot 6: Line plot of progress of every solution path
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
plot6<-function(moves){
  title=strsplit(moves$instance[[2]],'-')[[1]][2]
  g<-ggplot(moves,aes(x=moves$move_number)) + geom_line(aes(color=paste(moves$subject, moves$trial_number),y=moves$distance_to_goal), size=0.5) +
    ggtitle(paste('puzzle ',title)) +xlab('move number') + ylab('distance from goal') +
    guides(color=guide_legend(title="path"))+theme(legend.position="none", axis.title.x=element_blank(),axis.title.y=element_blank())
  return(g)
}
moves_ins = split(moves, moves$instance)
slplots=lapply(moves_ins, plot6)
#slplots<-slplots[order(nchar(names(slplots)),names(slplots))]
slplots<-slplots[order(match(names(slplots),lvls_sl), names(slplots))]
#do.call('grid.arrange',c(slplots, ncol = 4, top = "Solution Progress"))
do.call('grid.arrange',c(slplots, ncol = 4))


####
# Plot 6.1: Line plot of progress of some solution path
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves, moves$instance %in% c('Jam-8', 'Jam-1', 'Jam-10','Jam-11','Jam-13','Jam-16'))
plot6<-function(moves){
  title=strsplit(moves$instance[[1]],'-')[[1]][2]
  g<-ggplot(moves,aes(x=moves$move_number)) + geom_line(aes(color=paste(moves$subject, moves$trial_number),y=moves$distance_to_goal), size=0.5) +
    ggtitle(paste('Puzzle-',title,sep = '')) +xlab('move#') + ylab('distance from goal') +
    guides(color=guide_legend(title="path"))+theme(legend.position="none", text = element_text(size = 12))+
    theme(axis.title = element_blank(), title = element_text(size=10))
  return(g)
}
moves_ins = split(moves, moves$instance)
moves_ins=moves_ins[c(1,6,3,2,4,5)]
slplots=lapply(moves_ins, plot6)
Cairo(file=paste(figpath,"/p6_1.png",sep=''), 
      type="png",
      units="px", 
      width=770, 
      height=350,
      pointsize=12*2, 
      dpi=72*2)
do.call('grid.arrange',c(slplots, ncol = 3))
dev.off()




####
# Plot 6.2: Line plot of progress of restarts
####
plot6<-function(moves){
  g<-ggplot(moves,aes(x=moves$move_number)) + geom_line(aes(color=paste(moves$subject, moves$trial_number, moves$instance),y=moves$distance_to_goal), size=1) +
    xlab('move#') + ylab('distance from goal') +
    guides(color=guide_legend(title="path"))+theme(legend.position="none", text = element_text(size = 12))
  return(g)
}
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$path<-paste(moves$subject,moves$instance,moves$trial_number,sep='_')
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$success<-with(paths, ifelse(paths$skipped,'skipped',ifelse(paths$complete,ifelse(paths$trial_number=='0','solved','restarted'),'NA')))
#restart
p=subset(paths,success=='restarted')
ps=paste(p$subject,p$instance,p$trial_number,sep='_')
moves=subset(moves, moves$path %in% ps)
moves_ins = split(moves, moves$instance)
d=data.frame('puzzle'=names(moves_ins), 'L'=sapply(moves_ins, nrow))
puz=subset(d, L>40)$puzzle
moves=subset(moves, moves$instance %in% puz)
moves_ins = split(moves, moves$instance)
slplots=lapply(moves_ins, plot6)
do.call('grid.arrange',c(slplots, ncol = 2))
plot6(moves)


####
# Plot 6.3: Line plot of progress of surrenders
####
plot6<-function(moves){
  g<-ggplot(moves,aes(x=moves$move_number)) + 
    geom_line(aes(color=paste(moves$subject, moves$trial_number, moves$instance),y=moves$distance_to_goal), size=1) +
    xlab('move#') + ylab('distance from goal') +
    guides(color=guide_legend(title="path"))+theme(legend.position="none", text = element_text(size = 12))
  return(g)
}
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$path<-paste(moves$subject,moves$instance,moves$trial_number,sep='_')
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$success<-with(paths, ifelse(paths$skipped,'skipped',ifelse(paths$complete,ifelse(paths$trial_number=='0','solved','restarted'),'NA')))
#restart
p=subset(paths,success=='skipped')
ps=paste(p$subject,p$instance,p$trial_number,sep='_')
moves=subset(moves, moves$path %in% ps)
plot6(moves)



####
# Plot 7: Bar plot of restrats/skipped/solved instance Status
#####
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$status<-factor(with(paths, ifelse(paths$skipped,'Surrender',ifelse(paths$complete,ifelse(paths$trial_number=='0','Solved','Restart'),'NA')))
                     ,levels = rev(c('Solved','Restart','Surrender')))
paths=subset(paths,status!= 'NA' & instance !='Jam-25')
paths$instance=factor(paths$instance, levels = lvls_e,labels = 1:length(lvls_e))
g<-ggplot(paths, aes(x=paths$instance, na.rm=T)) + geom_bar(aes(fill=status)) + xlab('Puzzle') + ylab('#Subejcts')+
  scale_y_continuous(breaks=1:length(unique(paths$subject)))+ 
  scale_fill_manual(values = c('darkred','darkorange','darkgreen'))+
  theme(legend.position = c(0.8,0.7), text = element_text(size=20))+
  theme(legend.text = element_text(size=14), legend.key.height = unit(0.4,'cm'),legend.key.width = unit(0.4,'cm') )
Cairo(file=paste(figpath,"/p7.png",sep=''), 
      type="png",
      units="px", 
      width=1124, 
      height=420,
      pointsize=12*2, 
      dpi=72*2)
g
dev.off()


####  
# Plot 8: Bar plot of #Moves Category Across Subjects
####  
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Same',ifelse(progress>0,'Closer','Further')))
d=aggregate(moves,by = list("category"=moves$category,"subject"=moves$subject), FUN = "length")
ggplot(d,aes(x=d$category, y=d$rt)) + stat_summary( fun.y="mean", geom="bar") + xlab('Moving closer/same/further from solution')+
  ylab("Count") + stat_summary(geom = "errorbar", position = "dodge", width=0.2, size=1,fun.data = mean_sem)


####  
# Plot 8.1: Bar plot of mean rt Category Across Subjects
####  
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Neutral',ifelse(progress>0,'Positive','Negative')))
d=moves
#d=aggregate(moves,by = list("category"=moves$category,"subject"=moves$subject), FUN = "mean")
ggplot(d,aes(x=d$category, y=d$rt)) + stat_summary( fun.y="mean", geom="bar") + xlab('Move category')+
  ylab("Seconds") + stat_summary(geom = "errorbar", position = "dodge", width=0.2, size=1,fun.data = mean_sem)+
  theme(text = element_text(size=18))


####  
# Plot 8.2: Bar plot of Average Mistakes per category, per instance  Across Subjects
####  
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Same',ifelse(progress>0,'Closer','Further')))
d=aggregate(moves,by = list("category"=moves$category,"subject"=moves$subject), FUN = "length")
ggplot(d,aes(x=d$instance, y=d$rt)) + stat_summary( fun.y="mean", geom="bar") + xlab('Moving closer/same/further from solution')+
  ylab("Count") + stat_summary(geom = "errorbar", position = "dodge", width=0.2, size=1,fun.data = mean_sem)





###
# Plot 9: Line plot of mean Response time vs move number per subject
###
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=aggregate(moves,by = list("subject"=moves$subject,"move_num"=moves$move_number), FUN = mean)
ggplot(d, aes(x=d$move_number,y=d$rt)) + stat_summary(fun.y = "mean", geom = "point", size=1) +stat_summary(fun.y = "mean", geom = "line" ) + 
  stat_summary(fun.data = mean_sem, geom = "errorbar" , color="blue", size=1, width=2) + 
  ggtitle('mean response time across subjects') + xlab('move#') + ylab('rt')



###
# Plot 10: Scatter plot of Human solution length, vs Optimal solution length aggregated by instance.
###
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=subset(paths, paths$complete=='True')
dm=aggregate(d, by = list('instance'=d$instance), FUN = mean)
ds=aggregate(d, by = list(d$instance), FUN = sd)
dl=aggregate(d, by = list(d$instance), FUN = length)
d=dm[,c('instance','optimal_length','human_length')]
d$sem=ds$human_length/sqrt(dl$human_length)
d$instance = factor(d$instance, levels = lvls_sl)
ggplot(d, aes(x=d$optimal_length , y=d$human_length))+ geom_point(stroke=2,aes(color=instance)) + 
  geom_errorbar(aes(ymin=d$human_length-(d$sem/2),ymax=d$human_length+(d$sem/2))) + 
  ggtitle('Solutions per instance') + xlab('Optimal solution') + ylab('Human solution')



###
# Plot 10.1: Scatter plot of Human solution length, vs Optimal solution length aggregated by instance.
###
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=subset(paths, paths$complete=='True')
dm=aggregate(d, by = list('instance'=d$instance), FUN = mean)
ds=aggregate(d, by = list(d$instance), FUN = sd)
dl=aggregate(d, by = list(d$instance), FUN = length)
d=dm[,c('instance','optimal_length','human_length')]
d$sem=ds$human_length/sqrt(dl$human_length)
d$instance = factor(d$instance, levels = lvls_sl)
ggplot(d, aes(x=d$optimal_length , y=d$human_length))+ geom_point(stroke=2) + 
  geom_errorbar(aes(ymin=d$human_length-(d$sem/2),ymax=d$human_length+(d$sem/2))) + 
   xlab('Optimal solution') + ylab('Human solution')



  
###
# Plot 11: line plot of raw bursts of response-time as move number 
##
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90 & moves$move_number < 40)
ggplot(moves, aes(x=moves$move_number)) + geom_line(aes(y=moves$rt, color=paste(subject,instance,trial_number)), show_guide=F) +
  ggtitle("response time bursts - raw") + xlab('move number') + ylab('Seconds') + ylim(0,90)



###
# Plot 12: Line plot of mean response-time by move number
##
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(moves, aes(x=moves$move_number, y=moves$rt)) +
  stat_summary(fun.y = 'mean', geom='line', size=2)+
  stat_summary(fun.y = 'mean', geom='point', size=3)+
  scale_alpha_discrete(aggregate(moves, by = list('move_number'=moves$move_number), FUN=length)$rt)+
  stat_summary(fun.data = mean_sem, geom='errorbar')+
  stat_summary(fun.data = function(x){data.frame(y=mean(x), label=length(x))} , geom='text' ,vjust=-1.5, hjust=1 , color='red', size=4)+
  ggtitle("response time bursts ") + xlab('move number') + ylab('Seconds') 

#####
# Plot 13:  histogram of rt 
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves, rt<60)
ggplot(moves, aes(x=moves$rt)) + geom_histogram(bins = 100)  + xlab("Seconds")



#####
# Plot 14:  histogram of rt  (median normalized)
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
med_rt = aggregate(moves, by = list('subject'=moves$subject), FUN=median)[,c('subject','rt')]
sd_rt = aggregate(moves, by = list('subject'=moves$subject), FUN=sd)[,c('subject','rt')]
names(med_rt)<-c('subject','med_rt')
names(sd_rt)<-c('subject','sd_rt')
d=merge(moves,med_rt)
d=merge(d,sd_rt)
d$norm_rt = (d$rt - d$med_rt)/d$sd_rt
ggplot(d, aes(x=d$norm_rt)) + geom_histogram(binwidth = 0.01) + ggtitle("Response times (normalized by median)") + xlab("Seconds")


#####
# Plot 15:  histogram of rt  (median normalized - zoom [-1 - 1])
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90)
med_rt = aggregate(moves, by = list('subject'=moves$subject), FUN=median)[,c('subject','rt')]
sd_rt = aggregate(moves, by = list('subject'=moves$subject), FUN=sd)[,c('subject','rt')]
names(med_rt)<-c('subject','med_rt')
names(sd_rt)<-c('subject','sd_rt')
d=merge(moves,med_rt)
d=merge(d,sd_rt)
d$norm_rt = (d$rt - d$med_rt)/d$sd_rt
d=subset(d, d$norm_rt < 1 )
ggplot(d, aes(x=d$norm_rt)) + geom_histogram(binwidth = 0.01) + ggtitle("Response times (normalized by median zoom [-1,1]) ") + xlab("Seconds")



####
# Plot 16: RT histograms per move category (good, neutral, wrong), trucncated (rt<15), with medians. 
####
moves=read.csv('moves.1.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Neutral',ifelse(progress>0,'Positive','Negative')))
moves= subset(moves, moves$rt < 15)
my_colors= c('blue','green','red')
ggplot() + 
  geom_density(data = subset(moves,category=='Negative'), aes(x=rt,fill='Negative'), alpha=0.3) + 
  geom_density(data = subset(moves,category=='Neutral'), aes(x=rt,fill='Neutral'), alpha=0.4) + 
  geom_density(data = subset(moves,category=='Positive'), aes(x=rt,fill="Positive"), alpha=0.2) + 
  scale_fill_manual(name="Move category", values=my_colors)+
  geom_density(data = subset(moves,category=='Negative'), aes(x=rt,fill='Negative'), alpha=0.0, size=0.5, color=my_colors[1], show.legend = F) + 
  geom_density(data = subset(moves,category=='Neutral'), aes(x=rt,fill='Neutral'), alpha=0.0, size=0.5, color=my_colors[2], show.legend = F) + 
  geom_density(data = subset(moves,category=='Positive'), aes(x=rt,fill="Positive"), alpha=0.0, size=0.5, color=my_colors[3], show.legend = F) + 
  
  #add means
  geom_vline(xintercept=mean(subset(moves,category=='Negative')$rt), color=my_colors[1], size=1, linetype=2)+
  geom_vline(xintercept=mean(subset(moves,category=='Neutral')$rt), color=my_colors[2], size=1, linetype=2)+
  geom_vline(xintercept=mean(subset(moves,category=='Positive')$rt), color=my_colors[3], size=1, linetype=2)+
    theme(legend.position=c(.8, .6), legend.title = element_text(size=12),legend.text = element_text(size=10), text = element_text(size=18))+
  guides(color='blue')+
  xlab("Seconds")


#####
# Plot 16.1: RT ECDF per move category (good, neutral, wrong) 
#####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Neutral',ifelse(progress>0,'Positive','Negative')))
sub='andra.log'
moves= subset(moves, moves$progress !='NA' & subject==sub)
moves=arrange(moves, subject, category, rt)
d=ddply(moves, .(subject, category), transform, ecdf=ecdf(rt)(rt))
mr=d[which(d$rt == max(d$rt)),]
d<-rbind(d,mr)
d[nrow(d),12]<-'Positive'
d<-rbind(d,mr)
d[nrow(d),12]<-'Negative'
d<-rbind(d,mr)
d[nrow(d),12]<-'Neutral'

g<-ggplot(d, aes(y=ecdf, x=rt)) + geom_line(aes(color=category), size=1) +
  xlab('Response time') + ylab('CDF')+
  theme(legend.position=c(.6, .5),
        legend.title = element_text(size=12),
        legend.text = element_text(size=10), 
        text = element_text(size=18), 
        legend.key.height = unit(0.2,'cm'))
Cairo(file=paste(figpath,"/p16_1.png",sep=''), 
      type="png",
      units="px", 
      width=470*1.2, 
      height=300,
      pointsize=12*2, 
      dpi=72*2)
g
dev.off()

####
# Plot 16.2: RT histograms per move category (good, neutral, wrong), trucncated (rt<15), with medians. 
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Neutral',ifelse(progress>0,'Positive','Negative')))
moves= subset(moves, category!='NA')
moves= subset(moves, moves$rt < 15)
bw=0.5
alp=1
sz=1
g<-ggplot() + 
  geom_freqpoly(data = moves, aes(x=rt,group=interaction(subject,category), color=category), binwidth=bw, size=sz, alpha=alp) +
  theme(legend.position=c(.8, .6), text = element_text(size=18))+
  theme(legend.title = element_text(size=12), legend.text = element_text(size=12),legend.key.height = unit(0.5,'cm'))+
  xlab("Seconds")
Cairo(file=paste(figpath,"/p16_2.png",sep=''), 
      type="png",
      units="px", 
      width=570, 
      height=300,
      pointsize=12*2, 
      dpi=72*2)
g
dev.off()


####
# Plot 16.3: bar plot of RT per move category (good, neutral, wrong) 
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Neutral',ifelse(progress>0,'Positive','Negative')))
moves= subset(moves, category!='NA')
d=ddply(moves, .(subject, category), function(x){return(mean_sem(x$rt))})
g<-ggplot(d, aes(x=d$category,y=d$y)) +  stat_summary(geom='bar', fun.y = 'mean')  + 
  stat_summary(geom='errorbar', fun.data = mean_sem, size=2, width=0.4)+  
  theme(text = element_text(size=18))+ xlab("category") + ylab("seconds") 
Cairo(file=paste(figpath,"/p16_3.png",sep=''), 
      type="png",
      units="px", 
      width=400*1.2, 
      height=300,
      pointsize=12*2, 
      dpi=72*2)
g
dev.off()


####
# Plot 17: Scatter plot of RT average across subjects, per instance, in relation to distance from goal.
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves, moves$rt<90)
ggplot(moves, aes(x=moves$distance_to_goal,y= moves$rt, group=instance)) + 
  stat_summary(fun.y = "mean", geom="point") + stat_summary(fun.data = mean_sem, geom="errorbar")


####
# Plot 18: Scatter plot of RT average across subjects, per instance, in relation to distance from goal.
# Normalized by subject median
#
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90)
med_rt = aggregate(moves, by = list('subject'=moves$subject), FUN=median)[,c('subject','rt')]
sd_rt = aggregate(moves, by = list('subject'=moves$subject), FUN=sd)[,c('subject','rt')]
names(med_rt)<-c('subject','med_rt')
names(sd_rt)<-c('subject','sd_rt')
d=merge(moves,med_rt)
d=merge(d,sd_rt)
d$norm_rt = (d$rt - d$med_rt)/d$sd_rt
ggplot(d, aes(x=d$distance_to_goal,y= d$norm_rt, group=instance)) + 
  stat_summary(fun.y = "mean", geom="point") + stat_summary(fun.data = mean_sem, geom="errorbar") + 
  ggtitle("RT vs. distance from goal") + xlab("Distance from goal") + ylab("Seconds")

######
# Plot 19: Boxplot with Kruskal Wallis test on rt per category
############
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=as.factor(with(moves, ifelse(progress==0, 'Same',ifelse(progress>0,'Closer','Further'))))
t=kruskal.test(rt ~ category, data = moves)
ggplot(data = moves, aes(x=category, y=rt)) + geom_boxplot() + 
  ggtitle('Kruskal-Wallis rank sum test - rt by category') + 
  annotate(geom = 'text',label='p-val= ~5.7e-10', x=2, y=95, size=9)

#####
# Plot 20: linear regression of log(rt) and distance from goal 
#######
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(moves, aes(x=distance_to_goal, y=log(rt)))  + geom_point() + 
  geom_smooth(method = 'lm', se=FALSE) + 
  annotate(geom = "text", label="intercept=0.82144, coefficient=0.01508(***)", x = 10, y=4.5) +
  ggtitle('linear regression log(rt)~distance_to_goal')

summary(lm(formula = log(moves$rt) ~ moves$distance_to_goal))


#####
# Plot 21:   linear regression of rt and distance from goal 
####
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(moves, aes(x=distance_to_goal, y=rt))  + geom_point() + 
  geom_smooth(method = 'lm', se=FALSE) + 
  annotate(geom = "text", label="intercept=3.4022, coefficient=0.1142(***)", x = 10, y=90)+
  ggtitle('linear regression rt~distance_to_goal')

summary(lm(formula = moves$rt ~ moves$distance_to_goal))



######
# Plot 22:  linear regression of rt and move_number 
#######
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(moves, aes(x=move_number, y=rt))  + geom_point() + 
  geom_smooth(method = 'lm', se=FALSE) + 
  annotate(geom = "text", label="intercept=5.9195, coefficient=-0.0984(***)", x = 15, y=90)+
  ggtitle('linear regression rt~move_num')
summary(lm(formula = moves$rt ~ moves$move_number))

###
# Plot 23:  linear regression of rt and move_number (without the first move)
######
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves, move_number>0)
ggplot(moves, aes(x=move_number, y=rt))  + geom_point() + 
  geom_smooth(method = 'lm', se=FALSE) + 
  annotate(geom = "text", label="intercept=5.9195, coefficient=0.01", x = 15, y=90, color='red') +
  ggtitle('linear regression rt~move_num (first move excluded)')
summary(lm(formula = moves$rt ~ moves$move_number))



###
# Plot 24 : Scatter plot of response time, vs Optimal solution length aggregated by instance.
###
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=subset(paths, paths$complete=='True')
dm=aggregate(d, by = list('instance'=d$instance), FUN = mean)
ds=aggregate(d, by = list(d$instance), FUN = sd)
dl=aggregate(d, by = list(d$instance), FUN = length)
d=dm[,c('instance','optimal_length','rt')]
d$sem=ds$rt/sqrt(dl$rt)
d$instance = factor(d$instance, levels = lvls_sl)
ggplot(d, aes(x=d$optimal_length , y=d$rt))+ geom_point(stroke=2,aes(color=instance)) + 
  geom_errorbar(aes(ymin=d$rt-(d$sem/2),ymax=d$rt+(d$sem/2))) + 
  ggtitle('RT per instance') + xlab('Optimal solution') + ylab('Seconds')



###
# Plot 25  : Scatter plot of response time, vs Distance from goal.
###
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
g<-ggplot(moves, aes(x=distance_to_goal , y=rt))+ geom_point() + 
   xlab('Distance from goal') + ylab('Seconds') + theme(text = element_text(size=18))

Cairo(file=paste(figpath,"/p25.png",sep=''), 
      type="png",
      units="px", 
      width=770, 
      height=350,
      pointsize=12*2, 
      dpi=72*2)
g
dev.off()


# Stat 1: Wilcox.test All rt unpaired (wrong)
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Neutral',ifelse(progress>0,'Positive','Negative')))
spl=split(moves, moves$category)
wilcox.test(spl$Positive$rt, spl$Negative$rt, alternative = 'less',paired = FALSE )
wilcox.test(spl$Positive$rt, spl$Neutral$rt, alternative = 'less',paired = FALSE )
wilcox.test(spl$Negative$rt, spl$Neutral$rt, alternative = 'less',paired = FALSE )

# Stat 2: Wilcox.test per subject (non-standard)
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Neutral',ifelse(progress>0,'Positive','Negative')))
moves=subset(moves, category!='NA')
func<-function(x){
  neg=subset(x,category=='Negative')$rt
  pos=subset(x,category=='Positive')$rt
  neu=subset(x,category=='Neutral')$rt
  return(wilcox.test(pos, neg, alternative = 'less',paired = FALSE)$p.value)
}
posneg=ddply(moves, .(subject), func)
names(posneg)<-c('subject','posneg')
func<-function(x){
  neg=subset(x,category=='Negative')$rt
  pos=subset(x,category=='Positive')$rt
  neu=subset(x,category=='Neutral')$rt
  return(wilcox.test(pos, neu, alternative = 'less',paired = FALSE)$p.value)
}
posneu=ddply(moves, .(subject), func)
names(posneu)<-c('subject','posneu')
func<-function(x){
  neg=subset(x,category=='Negative')$rt
  pos=subset(x,category=='Positive')$rt
  neu=subset(x,category=='Neutral')$rt
  return(wilcox.test(neg, neu, alternative = 'less',paired = FALSE)$p.value)
}
negneu=ddply(moves, .(subject), func)
names(negneu)<-c('subject','negneu')
d=merge(posneg,posneu,by='subject')
d=merge(d,negneu, by='subject')
  
###########
# Stat 3: Wilcox.test on every subjetc
###############
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Neutral',ifelse(progress>0,'Positive','Negative')))
d=ddply(moves, .(subject, category), function(x){return(median(x$rt))})
sp=split(d,d$category)
wilcox.test(sp$Positive$V1, sp$Negative$V1, alternative = 'two.sided',paired = TRUE)$p.value
wilcox.test(sp$Positive$V1, sp$Neutral$V1, alternative = 'two.sided',paired = TRUE)$p.value
wilcox.test(sp$Negative$V1, sp$Neutral$V1, alternative = 'two.sided',paired = TRUE)$p.value




##########
#  Stat 4:  spearman correlation per subject rt~move#
########## 
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
d=ddply(moves, .(subject), function(x){return(cor(x$rt, x$move_number,method = 'spearman'))})
mean_sem_(d$V1)

##########
#  Stat 5:  spearman correlation per subject rt~distance#
########## 
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves,distance_to_goal !='NA' & progress !='NA' )
d=ddply(moves, .(subject), function(x){return(cor(x$rt, x$distance_to_goal,method = 'spearman'))})
mean_sem_(d$V1)


##########
#  Stat 5.1:  Quadratic relationship of rt~distance#
########## 
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves,distance_to_goal !='NA' & progress !='NA')

d=ddply(moves,.(subject), function(x){return(summary(lm(x$rt ~ poly(x$distance_to_goal, 2, raw = T)))$adj.r.squared)})
mean_sem_(d$V1)


##########
#  Stat 6:  mean completed puzzles. 
#  Subjects completed on average X ± x puzzles (minimum of X, maximum of Y).
########## 
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths=subset(paths, complete=="True")
d=ddply(paths, .(subject), function(x){return(nrow(x))})
mean_sem_(d$V1)

##########
#  Stat 7:  Human vs optimal 
#  On average, subjects performed X\% more moves than the minimal solution.
########## 
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths=subset(paths, complete=='True')
d=ddply(paths, .(subject,instance), function(x){return(x$human_length/(x$optimal_length+1))})
d1=ddply(d, .(subject), function(x){return(mean(x$V1))})
mean_sem_(d$V1)



##########
#  Stat 8:  Optimal human solutions 
#  In total there were XX optimal solutions out of YY solution paths that our subjects tried.
########## 
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$path<-paste(paths$subject,paths$instance,paths$trial_number,sep='_')
length(unique(paths$path))
nrow(subset(paths, complete=='True' & human_length==optimal_length+1))

paths=subset(paths, complete=='True')
d=ddply(paths, .(subject,instance), function(x){return(x$human_length/x$optimal_length)})
d1=ddply(d, .(subject), function(x){return(mean(x$V1))})
mean_sem_(d$V1)

##########
#  Stat 9:  Surrender/Restart
#  Out of the 11 subjects, X surrendered and only two surrendered more than once. 
#  On average subjects surrendered after three trials. 
########## 
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$success<-with(paths, ifelse(paths$skipped,'skipped',ifelse(paths$complete,ifelse(paths$trial_number=='0','solved','restarted'),'NA')))
# Total subjects that skipped 
length(unique(subset(paths, success == 'skipped')$subject))
length(unique(subset(paths, success == 'restarted')$subject))


##########
#  Stat 9.1:  Surrender decisions.
#  When are they surrendering 
########## 
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$success<-with(paths, ifelse(paths$skipped,'skipped',ifelse(paths$complete,ifelse(paths$trial_number=='0','solved','restarted'),'NA')))
paths$path<-paste(paths$subject,paths$instance,paths$trial_number,sep='_')
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$path<-paste(moves$subject,moves$instance,moves$trial_number,sep='_')
s =subset(paths, success == 'skipped')
sm=subset(moves, moves$path %in% s$path) 
#check the trial_number in moves. Something is weird there. 
mx=ddply(moves, .(path), function(x){return(max(x$move_number))})
names(mx)<-c('path','move_number')
mn=ddply(moves, .(path), function(x){return(min(x$distance_to_goal))})
names(mn)<-c('path','min_dist')
k<-merge(mx,sm)
k<-merge(k,mn)
k$t<-k$distance_to_goal-k$min_dist
mean_sem_(k$t)



##########
#  Stat 9.2:  Restart decisions.
#  When are they restarting 
########## 
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$success<-with(paths, ifelse(paths$skipped,'skipped',ifelse(paths$complete,ifelse(paths$trial_number=='0','solved','restarted'),'NA')))
paths$path<-paste(paths$subject,paths$instance,paths$trial_number,sep='_')
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$path<-paste(moves$subject,moves$instance,moves$trial_number,sep='_')
s =subset(paths, success == 'restarted')
sm=subset(moves, moves$path %in% s$path) 
#check the trial_number in moves. Something is weird there. 
mx=ddply(moves, .(path), function(x){return(max(x$move_number))})
names(mx)<-c('path','move_number')
mn=ddply(moves, .(path), function(x){return(min(x$distance_to_goal))})
names(mn)<-c('path','min_dist')
k<-merge(mx,sm)
k<-merge(k,mn)
k$t<-k$distance_to_goal-k$min_dist
mean_sem_(k$t)




##########
#  Stat 9:  First move RT
########## 
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$path<-paste(moves$subject,moves$instance,moves$trial_number,sep='_')
d=ddply(moves, .(path), function(x){
  first=x[x$move_number==0,c('rt')]
  m = mean(x[x$move_number!=0,c('rt')])
  return(first/m)
})
x=d$V1
x=x[!is.na(x)]
mean_sem_(x)

##########
#  Stat 10: Move categories
########## 
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'neutral',ifelse(progress>0,'positive','negative')))
table(moves$category)
d=ddply(moves, .(subject, category), function(x){return (nrow((x)))})
ddply(d, .(category), function(x){return (mean_sem_(x$V1))})

d=ddply(moves, .(subject), function(x){return (data.frame(table(x$category)))})
d1=ddply(d, .(Var1), function(x){return (mean_sem_(x$Freq))})


######
## Stat 11: Bursts
######
avg_burst<-function(x){
  h=which(c('H',as.character(x$level),'H')=='H')
  return(mean(diff(h)))
}

library(combinat)
rand_burst<-function(x){
  l=as.character(x$level)
  pp=unique(permn(l))
  for (p in pp){
    h=which(c('H',p,'H')=='H')
    res=c(res,mean(diff(h)))
  }
  return(mean(res))
}

rand_burst<-function(x){
  res=c()
  l=as.character(x$level)
  for(i in 1:100){
    h=which(sample(c('H',l,'H'))=='H')
    res=c(res,mean(diff(h)))
  }
  #return(res)
  return(mean(res))
}

library(boot)
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$path<-paste(moves$subject,moves$instance,moves$trial_number,sep='_')
d=ddply(moves, .(path), function(x){return(mean(x$rt))})
names(d)<-c('path','rt_med')
moves=merge(moves,d)
moves$level = with(moves,ifelse(rt>rt_med,'H','L'))
ab=ddply(moves, .(path), avg_burst)
names(ab)<-c('path','ab')
rb=ddply(moves, .(path), rand_burst)
names(rb)<-c('path','rb')
k=merge(ab,rb)
k$diff=k$ab-k$rb
k$ratio=k$ab/k$rb
mean_sem_(k$ratio)
bk=boot(k$diff, statistic = function(x, indices){return(mean(x[indices]))}, R=100000)
plot(bk)
ggplot(k, aes(x=diff)) + geom_histogram()

####
# Trying to say something about the distribution of RT
####
library(mclust)
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
#m=Mclust(moves$rt)
m=densityMclust(moves[,c('rt','move_number')])
summary(m)
plot(m) 


#Do pearson
# Also, (as always), I would suggest to compute the correlation by subject, then report mean and SEM across subjects, since if different subjects are in different regions of the plot, this could easily dilute the correlation.

# Burst detection - "Suprise" measurement - Burst in FR is an anomaly in time-series. 
# This should be done by  window-based time-series analysis methods: 
# [10] V. Ganti, J. Gehrke, and R. Ramakrishnan. Demon: Data evolution and monitoring. In Proceedings of the 16th International Conference on Data Engineering, San Diego, California, 2000.
#[11] J. Gehrke, F. Korn, and D. Srivastava. On computing correlated aggregates over continual data streams. In Proc. ACM SIGMOD International Conf. on Management of Data, 2001.
#[12] A. C. Gilbert, Y. Kotidis, S. Muthukrishnan, and M. Strauss. Surfing wavelets on streams: One-pass summaries for approximate aggregate queries. In VLDB 2001, pages 79–88. Morgan Kaufmann, 2001.
# We want to detect a reoccuring pattern in the subjects rt which is conditioned on the stimuli.
# Dynamic time warping measures the match between two time-series.
# Clustering is also possible.
library(dtw)

moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves, instance=='Jam-6')
ggplot(moves, aes(x=moves$move_number)) + geom_line(aes(y=moves$rt, color=paste(subject,instance,trial_number)), show_guide=F) +
  ggtitle("response time bursts - raw") + xlab('move number') + ylab('Seconds') + ylim(0,90)
query=subset(moves, subject=='gianni.log')$rt
reference=subset(moves, subject=='weiji.log')$rt
d=dtw(query,reference, step=asymmetric,keep.internals = TRUE)

plot(d, type = "twoway")
plot(d, type = "threeway")

#split by solution-paths, heatmap of distances.
moves=read.csv('moves.c.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves, instance=='Jam-6')
moves$path=paste(moves$subject,moves$instance,moves$trial_number,sep = '')
dtw_dist<-function(path1,path2){
  query=subset(moves, path==path1)$rt
  reference=subset(moves, path==path2)$rt
  print(path1)
  cat(query)
  print(path2)
  cat(reference)
  d=dtw(query,reference, distance.only = TRUE)
  return (d$distance)
}
z=outer(moves$path, moves$path, FUN = dtw_dist)

ggplot(moves, aes(x=path, y=path)) + geom_tile(aes(fill= rt)) + scale_fill_gradient(low = "white",high = "steelblue")

lm <- matrix(nrow = 6, ncol = 6, byrow = TRUE, c(
  1,1,2,2,3,3,
  1,1,1,2,2,2,
  3,1,2,2,3,3,
  3,1,2,1,1,2,
  3,2,1,2,1,2,
  3,3,3,2,1,2 
))
alignment <- dtw(lm, step = asymmetric, keep = TRUE)
lcm <- alignment$localCostMatrix
image(x = 1:nrow(lcm), y = 1:ncol(lcm), lcm)
text(row(lcm), col(lcm), label = lcm)
lines(alignment$index1, alignment$index2)
ccm <- alignment$costMatrix
image(x = 1:nrow(ccm), y = 1:ncol(ccm), ccm)
text(row(ccm), col(ccm), label = ccm)
lines(alignment$index1, alignment$index2)


