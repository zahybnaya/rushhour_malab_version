library(ggplot2)
setwd("~/gdrivezb9/rushhour/results/pilot")
paths=read.csv('paths.csv', header = TRUE, sep=',',stringsAsFactors=F)
lvls=unique(paths[order(nchar(paths$instance),paths$instance),c('instance')])


###
# Plot 1: Scatter plot of Human solution length, vs Optimal solution length, shape/color by instance.
# What is smooth (and if not, drop it.)
###
d=subset(paths, paths$complete=='True')
d$instance=factor(d$instance, levels = lvls)
#png(filename = './png/p1.png', width = 1022, height = 555)
ggplot(d, aes(x=d$optimal_length))+ geom_point(stroke=2,aes(y=d$human_length,color=instance, shape=d$subject))+
scale_shape_manual(values = 1:7, guide=FALSE)+ geom_smooth(aes(y=d$human_length))+
  ggtitle('Solutions') + xlab('Optimal solution') + ylab('Human solution')
#dev.off()

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
ggplot(moves, aes(x=moves$move_number)) + geom_point(aes(y=moves$rt, color=subject)) + geom_smooth(aes(y=moves$rt))+
  ggtitle("response times") + xlab('move number') + ylab('Seconds') + ylim(0,90)


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
# Plot 6, (the progress of every path)
# TODO: Fix Maija 
# TODO: Aggregate per instance/subjects/filter complete paths
####
moves=read.csv('moves.csv', header = TRUE, sep=',',stringsAsFactors=F)
moves=subset(moves, moves$instance=='Jam-10')

plot6<-function(moves){
ggplot(moves,aes(x=moves$move_number)) + geom_line(aes(color=paste(moves$subject, moves$trial_number),y=moves$distance_to_goal)) +
  geom_point(aes(y=moves$distance_to_goal), size=0.5) + ggtitle('Solution progress') + xlab('move#') + ylab('optimal solution') +
    guides(color=guide_legend(title="path"))
}

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




