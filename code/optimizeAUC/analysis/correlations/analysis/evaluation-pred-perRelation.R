#(base) user@user-X510UAR:~/memsurp-optim/code/optimizeAUC/analysis/correlations/analysis$ cp ~/optimization-landscapes/analysis/families.tsv .
#(base) user@user-X510UAR:~/memsurp-optim/code/optimizeAUC/analysis/correlations/analysis$ ls ../../../output
#arguments.tsv  grammars.tsv

library(forcats)
library(dplyr)
library(tidyr)
library(ggplot2)
library("brms")


families = read.csv("families.tsv", sep="\t")
data = read.csv("../../../output/grammars.tsv", sep="\t") %>% rename(Language=language)

data = merge(data, families, by=c("Language"), all.x=TRUE)

unique((data %>% filter(is.na(Family)))$Language)


objs = data %>% group_by(idForProcess) %>% filter(dependency == "obj")  %>% select(idForProcess, weight)%>% rename(obj_weight=weight)
HEADs = data %>% group_by(idForProcess) %>% filter(dependency == "HEAD") %>% select(idForProcess, weight) %>% rename(HEAD_weight=weight)

data = merge(data, objs, by=c("idForProcess"), all=TRUE)
data = merge(data, HEADs, by=c("idForProcess"), all=TRUE)

data$agree = ((data$weight > data$HEAD_weight) == (data$obj_weight > data$HEAD_weight))

print(data %>% filter(Language == "English_2.6") %>% group_by(dependency) %>% summarise(agree = mean(agree)), n=100)

dependency = "nmod"
dependencies = c("acl", "advcl", "advmod", "amod", "appos", "aux", "ccomp", "compound", "conj", "csubj", "dep", "det", "discourse", "dislocated", "expl", "fixed", "flat", "goeswith", "iobj", "case", "cc", "cop", "mark", "list", "nmod", "nsubj", "nummod", "obl", "orphan", "parataxis", "reparandum", "vocative", "xcomp")
library(ggplot2)


type = "AUC"

u = data %>% filter(dependency == "nmod")
model3 = brm(agree ~ (1|p|Family) + (1|q|Language), family="bernoulli", data=u, iter=100)


for(dependency_ in dependencies) {
   u = data %>% filter(dependency == dependency_)
   model3 = update(model3, newdata=u, iter=5000)
   u = posterior_samples(model3)
   write.csv(u, file=paste("~/posteriors/posterior-", dependency_, "-", type, "-large.csv", sep=""))
}





