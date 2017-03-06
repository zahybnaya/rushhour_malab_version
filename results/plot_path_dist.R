library(ggplot2)
library(grid)
library(gridExtra)
setwd("~/gdrivezb9/rushhour/results")

# sample, step, state, instance, alg
#dist<-read.csv('raw_path_dist1.csv',header = TRUE, sep = ' ')
dist<-read.csv('raw_dist_algs.1.csv',header = TRUE, sep = ' ')
dist<-read.csv('raw_path_dist_2.csv',header = TRUE, sep = ' ')
dist<-read.csv('all_astar.csv',header = TRUE, sep = ' ')

dists=split(dist,dist[,c('instance')])



solution_lengths<-function(d){
  steps=aggregate(d[,c('sample','step')],by = list(d$sample), FUN = max)
  return(paste(unique(d$instance),unique(steps$step),sep = ':'))
}


solution_length_plot<-function(d){
  alg_splits=split(d, d$alg)
  all_steps=list()
  for (x in alg_splits){
    steps=aggregate(x[,c('sample','step')],by = list(x$sample), FUN = max)
    steps$alg=unique(x$alg)
    all_steps=rbind(all_steps,steps)
  }
  g<-ggplot(all_steps,aes(x=all_steps$step,fill=all_steps$alg)) + xlab('length') + geom_bar(position = "dodge")+theme(legend.position="top", legend.direction="vertical", axis.title.x=element_blank(), axis.title.y=element_blank())
  return(g);
}

path_dist_plot<-function(d){
  g<-ggplot(d,aes(x=factor(d$state,d$state),fill=d$alg)) + geom_bar(position = "dodge")+theme(legend.position="none", axis.title.x=element_blank(),axis.title.y=element_blank())
  return(g);
}


slplots=lapply(dists, solution_length_plot)
do.call('grid.arrange',c(slplots, ncol = 5, top = "Solution Lengths"))


optimal_alg=subset(dist,dist$alg=='A*_h:zeroh_f:1*(g+1)+1h_is_stop:<lambda>_lapse_rate:0')

dist1=subset(dist,dist$alg=='A*_h:zeroh_f:1*(g+1)+1h_is_stop:<lambda>_lapse_rate:0' | dist$alg=='A*_h:zeroh_f:1*(g+1)+1h_is_stop:<lambda>_lapse_rate:0.01')

dists=split(dist1,dist1[,c('instance')])

slplots=lapply(dists, path_dist_plot)
do.call('grid.arrange',c(slplots, ncol = 5, top = "Path Distributions"))
