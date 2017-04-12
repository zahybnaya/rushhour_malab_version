library(ggplot2)
setwd("~/gdrivezb9/Zahy - Rush Hour/results/pilot")
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



moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
d= subset(moves, moves$rt < 90)
ggplot(d, aes(x=d$distance_to_goal,y= d$rt)) + geom_point() + 
  geom_smooth(method = "glm", color = "blue") +
  geom_smooth(method = "lm", color = "red") + 
  geom_smooth(method = "gam", color = "black") + 
  geom_smooth(method = "loess", color = "yellow") + 
  geom_smooth(formula = y ~ poly(x,2), method = "loess", color = "purple") 
  
  



####
# Plot 18, RT average across subjects, per instance, in relation to distance from goal.
# Normalized by subject median
#
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
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



####
# Plot 17, RT average across subjects, per instance, in relation to distance from goal.
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves, moves$rt<90)
ggplot(moves, aes(x=moves$distance_to_goal,y= moves$rt, group=instance)) + 
  stat_summary(fun.y = "mean", geom="point") + stat_summary(fun.data = mean_sem, geom="errorbar")


####
# Plot 16, RT histograms per move category (good, neutral, wrong), trucncated (rt<15), with medians. 
####
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Same',ifelse(progress>0,'Closer','Further')))
moves= subset(moves, moves$rt < 15)
ggplot() + 
  geom_histogram(data = subset(moves,category=='Closer'), aes(x=rt,fill="Closer"), alpha=0.5, binwidth = 0.2) + 
  geom_histogram(data = subset(moves,category=='Further'), aes(x=rt,fill='Further'), alpha=0.8,binwidth = 0.2) + 
  geom_histogram(data = subset(moves,category=='Same'), aes(x=rt,fill='Same'), alpha=0.8, binwidth = 0.2) + 
  scale_fill_manual(name="Move category", values=c("blue","yellow","red"))+theme(legend.position=c(.8, .9))+
  #add means
  geom_vline(xintercept=median(subset(moves,category=='Closer')$rt), color="blue", size=1, linetype=2)+
  geom_vline(xintercept=median(subset(moves,category=='Further')$rt), color="yellow", size=1, linetype=2)+
  geom_vline(xintercept=median(subset(moves,category=='Same')$rt), color="red", size=1, linetype=2)+
  ggtitle("Response Times per move quality") + xlab("Seconds")


#####
# Plot 15 - histogram of rt  (median normalized - zoom [-1 - 1])
####
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
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


#####
# Plot 14 - histogram of rt  (median normalized)
####
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90)
med_rt = aggregate(moves, by = list('subject'=moves$subject), FUN=median)[,c('subject','rt')]
sd_rt = aggregate(moves, by = list('subject'=moves$subject), FUN=sd)[,c('subject','rt')]
names(med_rt)<-c('subject','med_rt')
names(sd_rt)<-c('subject','sd_rt')
d=merge(moves,med_rt)
d=merge(d,sd_rt)
d$norm_rt = (d$rt - d$med_rt)/d$sd_rt
#d=subset(d, d$norm_rt < 1)
ggplot(d, aes(x=d$norm_rt)) + geom_histogram(binwidth = 0.01) + ggtitle("Response times (normalized by median)") + xlab("Seconds")

#####
# Plot 13 - histogram of rt 
####
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90)
ggplot(moves, aes(x=moves$rt)) + geom_histogram(bins = 100) + ggtitle("Response times") + xlab("Seconds")


###
# Plot 12, bursts plot of mean response-time by move number
##
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90 & moves$move_number < 40)
ggplot(moves, aes(x=moves$move_number, y=moves$rt)) +
  stat_summary(fun.y = 'mean', geom='line', size=2)+
  stat_summary(fun.y = 'mean', geom='point', size=3)+
  scale_alpha_discrete(aggregate(moves, by = list('move_number'=moves$move_number), FUN=length)$rt)+
  stat_summary(fun.data = mean_sem, geom='errorbar')+
  stat_summary(fun.data = function(x){data.frame(y=mean(x), label=length(x))} , geom='text' ,vjust=-1.5, hjust=1 , color='red', size=4)+
  ggtitle("response time bursts ") + xlab('move number') + ylab('Seconds') 


###
# Plot 11, raw bursts plot of response-time as move number 
##
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90 & moves$move_number < 40)
ggplot(moves, aes(x=moves$move_number)) + geom_line(aes(y=moves$rt, color=paste(subject,instance,trial_number)), show_guide=F) +
  ggtitle("response time bursts - raw") + xlab('move number') + ylab('Seconds') + ylim(0,90)


###
# Plot 10: Scatter plot of Human solution length, vs Optimal solution length aggregated by instance.
###
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
# Plot 1: Scatter plot of Human solution length, vs Optimal solution length, shape/color by instance.
###
d=subset(paths, paths$complete=='True')
d$instance=factor(d$instance, levels = lvls)
ggplot(d, aes(x=d$optimal_length))+ geom_point(stroke=2,aes(y=d$human_length,color=instance, shape=d$subject))+
scale_shape_manual(values = 1:7, guide=FALSE)+ geom_smooth(aes(y=d$human_length))+
  ggtitle('Solutions') + xlab('Optimal solution') + ylab('Human solution')

## Plot 2: Plot of instances  optimal legths.
d=aggregate(paths, by = list(instance=paths$instance), FUN=mean)[,c('instance', 'optimal_length')]
d$instance=factor(d$instance, levels = lvls)
ggplot(d, aes(d$instance, d$optimal_length)) +geom_bar(stat="identity") + 
  ggtitle('Optimal solution lengths per instance')+ xlab('Instance') + ylab('Optimal length')



###
# Plot 3, scatter plot of response-time as move number
##
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90)
ggplot(moves, aes(x=moves$move_number)) + geom_point(aes(y=moves$rt, color=subject)) +
  ggtitle("response times") + xlab('move number') + ylab('Seconds') + ylim(0,90)

###
# Plot 9
###
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves= subset(moves, moves$rt < 90)
d=aggregate(moves,by = list("subject"=moves$subject,"move_num"=moves$move_number), FUN = mean)
ggplot(d, aes(x=d$move_number,y=d$rt)) + stat_summary(fun.y = "mean", geom = "point", size=1) +stat_summary(fun.y = "mean", geom = "line" ) + 
  stat_summary(fun.data = func, geom = "errorbar" , color="blue", size=1, width=2)


###
# Plot 4, how many moves on each counter
###
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
ggplot(moves, aes(x=moves$move_number, fill=instance)) + geom_bar() + ggtitle("occurences per move_number")

####
# Plot 5, the counting of (good, neutral, wrong)
# TODO: do across instances/subjects
####
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Same',ifelse(progress>0,'Closer','Further')))
ggplot(moves,aes(x=moves$category)) + geom_bar() + ggtitle('Moves Category') + xlab('Moving closer/same/further from solution')

####  
# Plot 8 
####  
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves$category=with(moves, ifelse(progress==0, 'Same',ifelse(progress>0,'Closer','Further')))
d=aggregate(moves,by = list("category"=moves$category,"subject"=moves$subject), FUN = "length")

ggplot(d,aes(x=d$category, y=d$rt)) + stat_summary( fun.y="mean", geom="bar") + ggtitle('Moves Category Across Subjects') + xlab('Moving closer/same/further from solution')+
  stat_summary(geom = "errorbar", position = "dodge", width=0.2, size=1,fun.data = func)
  
####
# Plot 6, (the progress of every path)
# TODO: Fix Maija 
# TODO: Aggregate per instance/subjects/filter complete paths
####
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)

plot6<-function(moves){
g<-ggplot(moves,aes(x=moves$move_number)) + geom_line(aes(color=paste(moves$subject, moves$trial_number),y=moves$distance_to_goal), size=2) +
  geom_point(aes(y=moves$distance_to_goal), size=0.1) + ggtitle(moves$instance[[2]])  + xlab('move number') + ylab('distance from goal') +
    guides(color=guide_legend(title="path"))+theme(legend.position="none", axis.title.x=element_blank(),axis.title.y=element_blank())
 return(g)
}
moves_ins = split(moves, moves$instance)
slplots=lapply(moves_ins, plot6)
slplots<-slplots[order(nchar(names(slplots)),names(slplots))]
do.call('grid.arrange',c(slplots, ncol = 4, top = "Solution Progress"))

plot6(moves)
#per instance, show the number of times subjects skipped it (skipped=True), the number of times it was solved in first trial (complete=True and trial_number=0) 
# and number of times it was completed in the not first trial (complete + trial_number>0).

##
# Plot 7 : Instance Status
##
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
paths$success<-with(paths, ifelse(paths$skipped,'skipped',ifelse(paths$complete,ifelse(paths$trial_number=='0','solved','restarted'),'NA')))
paths=subset(paths,success!= 'NA')
paths$instance=factor(paths$instance, levels = lvls)
ggplot(paths, aes(x=paths$instance, na.rm=T)) + geom_bar(aes(fill=success)) + ggtitle('instance status') + xlab('instance') + ylim(0,7)










complete_paths= subset(paths, paths$complete==' True')
incomplete_paths= subset(paths, paths$complete==' False')

ggplot(data=incomplete_paths)  + geom_bar(aes(x=incomplete_paths$instance)) + ggtitle("Skips/Restarts")

d1=aggregate(paths, by=list('instance'=paths$instance), length)
d1=d1[,c('instance','complete')]
d1$total=d1$complete
d2=aggregate(incomplete_paths, by=list('instance'=incomplete_paths$instance), length)
d2=d2[,c('instance','complete')]
d2$incomplete=d2$complete
d3=merge(d1,d2,by="instance")
d3$ratio = d3$incomplete/d3$total
d4=d3[,c('instance','ratio')]

ggplot(data=d3)  + geom_bar(aes(x=d3$instance,y=d3$ratio), stat='identity', fill='blue' ) + ggtitle("Skips/Restarts Ratio")


d=aggregate(complete_paths, by=list('subject'=complete_paths$subject, complete_paths$optimal_length), mean)
all_subject=aggregate(complete_paths, by=list(complete_paths$optimal_length), mean)
sd_subject= aggregate(complete_paths, by=list(complete_paths$optimal_length), sd)
sd_subject$human_length=sd_subject$human_length/sqrt(length(unique(complete_paths$subject)))
sd_subject$rt=sd_subject$rt/sqrt(length(unique(complete_paths$subject)))

all_subject$subject='all'
all_subject$length_se=sd_subject$human_length
all_subject$rt_se=sd_subject$rt

#Human solution length vs optimal solution length
ggplot(d, aes(x=d$optimal_length)) +
  geom_line(size=2, aes(y=d$human_length, color=d$subject)) + 
  geom_point(aes(y=d$human_length), fill='white' , shape=21) +
  geom_line(size=3, data = all_subject, aes(x=all_subject$optimal_length, y=all_subject$human_length)) +
  geom_errorbar(data = all_subject, 
                aes(x=all_subject$optimal_length, ymin=all_subject$human_length-(all_subject$length_se/2), 
                    ymax=all_subject$human_length+(all_subject$length_se/2)), width=.2) +
  ggtitle('Human solution length') +
  xlab('Difficulty (Optimal solution length)') + ylab('Human solution ')



ggplot(d, aes(x=d$optimal_length)) +
  geom_line(size=2, aes(y=d$rt, color=d$subject)) + 
  geom_point(aes(y=d$rt), fill='white' , shape=21) +
  geom_line(size=3, data = all_subject, aes(x=all_subject$optimal_length, y=all_subject$rt)) +
  geom_errorbar(data = all_subject, 
                aes(x=all_subject$optimal_length, ymin=all_subject$rt-(all_subject$rt_se/2), 
                    ymax=all_subject$rt+(all_subject$rt_se/2)), width=.2) +
  ggtitle('Solution times') +
  xlab('Difficulty (Optimal solution length)') + ylab('Response time for path')




