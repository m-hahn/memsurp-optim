# Visualizes posteriors per relation, for optimized and real grammars


library(dplyr)
library(tidyr)
library(ggplot2)
library(forcats)

dependencies = c("acl", "advcl", "advmod", "amod", "appos", "aux", "ccomp", "compound", "conj", "csubj", "dep", "det", "discourse", "dislocated", "expl", "fixed", "flat", "goeswith", "iobj", "case", "cc", "cop", "mark", "list", "nmod", "nsubj", "nummod", "obl", "orphan", "parataxis", "reparandum", "vocative", "xcomp")



#balanced = read.csv("results-ground-agree.tsv", sep="\t")
#balanced = balanced %>% 

library(dplyr)
library(tidyr)
library(ggplot2)




library(dplyr)
library(tidyr)
library(ggplot2)



type = "AUC"
dependency = "acl"


  for(dependency in dependencies) {
     data =  read.csv(paste("~/posteriors/posterior-", dependency, "-", type, "-large.csv", sep=""))
     data = data %>% mutate(Prevalence = 1/(1+exp(-b_Intercept)))
     if(dependency %in% c("aux", "case", "cop", "mark")) {
         data = data %>% mutate(Prevalence=1-Prevalence)
     }
     plot = ggplot(data=data)
     plot = plot  + geom_density(aes(x=Prevalence, y=..scaled..), alpha=.5, fill="blue")
     plot = plot + xlim(0,1)
     plot = plot + theme_classic()
     plot = plot + theme_void()
     plot = plot  + theme(legend.position="none")
     plot = plot + geom_segment(aes(x=0.5, xend=0.5, y=0, yend=1), linetype=2)
     ggsave(paste("../figures/posteriors/posterior_perRelation_", type, "_", dependency, ".pdf", sep=""), plot=plot, height=1, width=2)
  }


#
#type = "Real"
#for(dependency in dependencies) {
#data = D %>% filter(Dependency==dependency)
#     if(dependency == "aux") {
#         data = data %>% mutate(Agree=1-Agree)
#     }
#
#   plot = ggplot(data=data)
#   plot = plot + geom_bar(stat="identity", width = 0.1, aes(x=Agree, y=1))
#   plot = plot + xlim(0,1)
#   plot = plot + theme_classic()
#   plot = plot + theme_void()
#   plot = plot  + theme(legend.position="none")
#   plot = plot + geom_segment(aes(x=0.5, xend=0.5, y=0, yend=1), linetype=2)
#   plot = plot + theme(axis.line.x = element_line(colour = "black"))
#   ggsave(paste("../figures/posteriors/posterior_perRelation_", type, "_", dependency, ".pdf", sep=""), plot=plot, height=1, width=2)
#}
#
#
#
#
#
