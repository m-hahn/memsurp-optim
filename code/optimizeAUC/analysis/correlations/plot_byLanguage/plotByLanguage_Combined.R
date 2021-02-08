library(forcats)
library(dplyr)
library(tidyr)
library(ggplot2)



ofInterest =  c("acl", "aux", "case", "cop", "mark", "nmod", "obl", "xcomp")




data = read.csv("../../../output/grammars.tsv", sep="\t") %>% rename(Language=language)


HEADs = data %>% group_by(idForProcess) %>% filter(dependency == "HEAD") %>% select(idForProcess, weight) %>% rename(HEAD_weight=weight)



data = merge(data, HEADs, by=c("idForProcess"), all=TRUE)

objs = data %>% group_by(idForProcess) %>% filter(dependency == "obj")  %>% select(idForProcess, weight, HEAD_weight)%>% rename(obj_weight=weight) %>% mutate(ObjDir = (obj_weight > HEAD_weight)) %>% select(idForProcess, ObjDir)

data = merge(data, objs, by=c("idForProcess"), all=TRUE)



data$Dir = (data$weight > data$HEAD_weight)


ground1 = read.csv("/home/user/optimization-landscapes/analysis/mle-fine_selected_auto-summary-lstm_2.6.tsv", sep="\t")
ground2 = read.csv("/home/user/optimization-landscapes/analysis/mle-fine_selected_auto-summary-lstm_2.7.tsv", sep="\t")
ground = rbind(ground1, ground2) %>% mutate(dependency=Dependency)

ground$Dir = (ground$DH_Mean_NoPunct < 0)

groundObjDir = ground %>% filter(dependency == "obj") %>% rename(GroundObjDir = Dir) %>% select(Language, GroundObjDir)
data = merge(data, groundObjDir, by=c("Language"), all.x=TRUE)
data = data %>% filter(ObjDir == GroundObjDir)

ground = merge(ground, groundObjDir, by=c("Language"), all.x=TRUE)


data$Type = "Optimized"
ground$Type = "Real"

D = rbind(data %>% select(Type, Language, dependency, Dir, idForProcess) %>% rename(FileName=idForProcess), ground %>% select(Type, Language, dependency, Dir, FileName))

D = D %>% group_by(Type, Language, dependency) %>% summarise(Dir = (mean(Dir)) > 0.5)
#D = D %>% group_by(Type, Language, dependency) %>% summarise(Dir = (mean(Dir)))



families = read.csv("families.tsv", sep="\t")

D = merge(D, families, by=c("Language"), all.x=TRUE)

unique((D %>% filter(is.na(Family)))$Language)


lang51 = read.csv("languages_54.R", sep="\t")

D = merge(D, lang51, by=c("Language"))


#iso = read.csv("languages-wals-mapping.csv", sep="\t")


#D = merge(D, iso, by=c("Language"), all.x=TRUE)

#unique((D %>% filter(is.na(iso_code)))$Language)



D$Language_Ordered = factor(D$Language, levels=unique(D[order(D$Family),]$Language), ordered=TRUE)
#D$iso_Ordered = factor(D$iso_code, levels=unique(D[order(D$Family),]$iso_code), ordered=TRUE)



D$Dir = ifelse(D$dependency %in% c("case", "aux", "mark", "cop"), 1-D$Dir, D$Dir)

D$Dir = 1-D$Dir

D$LanguageNumeric = as.numeric(D$Language_Ordered)

D$FamilyPrint = as.character(D$Family)
D = D %>% mutate(FamilyPrint = ifelse(FamilyPrint == "Malayo-Sumbawan", "Mal.-Sum.", as.character(FamilyPrint)))
D = D %>% mutate(FamilyPrint = ifelse(FamilyPrint == "Sino-Tibetan", "Sin.-Tib.", as.character(FamilyPrint)))
D = D %>% mutate(FamilyPrint = ifelse(FamilyPrint == "Viet-Muong", "Viet-M.", as.character(FamilyPrint)))


DFam = D %>% group_by(FamilyPrint) %>% summarise(Start = min(LanguageNumeric), End = max(LanguageNumeric), Mean = mean(LanguageNumeric))

DFam$yOffset = 0.2*(1:(nrow(DFam))) 
D$yOffset=NULL
D = merge(D, DFam %>% select(FamilyPrint, yOffset), by=c("FamilyPrint"))


DLang = unique(D %>% select(Language_Ordered, LanguageNumeric, yOffset))


D = D %>% mutate(dependency = recode(dependency, case=1, cop=2, aux=3, nmod=4, acl=5, mark=6, obl=7, xcomp=8))

D = (D %>% filter(!is.na(dependency)))


plot_orders_real = ggplot(D %>% filter(Type == "Real"), aes(x = 1, y = LanguageNumeric+yOffset, group=dependency)) + 
  geom_point(aes(fill=Dir, colour = Dir, size =1), position = position_dodge(width=2.0)) +
#  scale_color_gradient() + #values=c("blue", "green")) +
  theme_classic() +
  #theme_bw() + 
  theme(axis.text.x=element_blank(), #element_text(size=9, angle=0, vjust=0.3),
                     axis.text.y=element_blank(),axis.ticks=element_blank(),
                     plot.title=element_text(size=11)) +
  theme(axis.title=element_blank()) + 
  theme(legend.position="none") + labs(x=NULL) +
  scale_x_continuous(breaks = NULL) +
  scale_y_continuous(breaks = NULL)

plot_orders_eff = ggplot(D %>% filter(Type == "Optimized"), aes(x = 1, y = LanguageNumeric+yOffset, group=dependency)) + 
  geom_point(aes(fill=Dir, colour = Dir, size =1), position = position_dodge(width=2.0)) +
#  scale_color_gradient() + #values=c("blue", "green")) +
  theme_classic() +
 theme(axis.text.x=element_blank(), #element_text(size=9, angle=0, vjust=0.3),
                     axis.text.y=element_blank(),axis.ticks=element_blank(),
                     plot.title=element_text(size=11)) +
  theme(axis.title=element_blank()) + 
  theme(legend.position="none") + labs(x=NULL) +
  scale_x_continuous(breaks = NULL) +
  scale_y_continuous(breaks = NULL)






plot_langs = ggplot(DLang) 
plot_langs = plot_langs +  theme_classic() 
plot_langs = plot_langs + theme(axis.text.x=element_blank(), #element_text(size=9, angle=0, vjust=0.3),
                     axis.text.y=element_blank(),
                     plot.title=element_text(size=11)) 
plot_langs = plot_langs + geom_text(aes(x=1.2 + 0.07, y=LanguageNumeric+yOffset, label=Language_Ordered), hjust=1, size=3, colour="grey30")
plot_langs = plot_langs +      	theme(axis.title=element_blank()) 
plot_langs = plot_langs + xlim(-2.0, 1.35)
plot_langs = plot_langs + geom_segment(data=DFam, aes(x=0, y=Start+yOffset, xend=0.5, yend=Start+yOffset)) 
plot_langs = plot_langs + geom_segment(data=DFam, aes(x=0, y=End+yOffset, xend=0.5, yend=End+yOffset)) 
plot_langs = plot_langs + geom_segment(data=DFam, aes(x=0, y=Start+yOffset, xend=0, yend=End+yOffset))
plot_langs = plot_langs + geom_text(data=DFam, aes(x=-0.1, y=Mean+yOffset , label=FamilyPrint), hjust=1, size=3, colour="grey30")
plot_langs = plot_langs + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
		    panel.background = element_blank(), axis.line = element_blank(),
                    plot.margin=unit(c(0,0,0,0), "mm"),
		    axis.ticks = element_blank()) + labs(x=NULL)
library("gridExtra")
plot_orders_real = plot_orders_real + theme(                    plot.margin=unit(c(0,0,0,0), "mm"))
plot_orders_eff = plot_orders_eff + theme(                    plot.margin=unit(c(0,0,0,0), "mm"))


plot = grid.arrange(plot_langs, plot_orders_real, plot_orders_eff, nrow=1, widths=c(1, 1.2, 1.2, 1.2, 1.2))
ggsave(plot=plot, "../figures/pred-eff-pred-pars-families.pdf", width=6, height=8)



plot_langs2 = plot_langs + annotate("text", label="", x=1, y=58.5, size=6)

plot_orders_real2 = plot_orders_real + annotate("text", label="Real", x=1, y=58.5, size=6)
plot_orders_real2 = plot_orders_real2 + geom_point(data=data.frame(num=c(1,2,3,4,5,6,7,8)), aes(x=0.25 * num - 0.12, group=NA, y=56.7, colour=NA, fill=NA), color="black", fill=NA, size=4.5, shape=21)
plot_orders_real2 = plot_orders_real2 + geom_text(data=data.frame(dependency=unique(D$dependency), num=c(1,2,3,4,5,6,7,8)), aes(x=0.25 * num - 0.12, group=dependency, y=56.55, label=as.character(num)))
plot_orders_real2

plot_orders_eff2 = plot_orders_eff + annotate("text", label="Efficiency", x=1, y=58.5, size=5)
plot_orders_eff2 = plot_orders_eff2 + geom_point(data=data.frame(num=c(1,2,3,4,5,6,7,8)), aes(x=0.25 * num - 0.12, group=NA, y=56.7, colour=NA, fill=NA), color="black", fill=NA, size=4.5, shape=21)
plot_orders_eff2 = plot_orders_eff2 + geom_text(data=data.frame(dependency=unique(D$dependency), num=c(1,2,3,4,5,6,7,8)), aes(x=0.25 * num - 0.12, group=dependency, y=56.55, label=as.character(num)))
plot_orders_eff2


plot = grid.arrange(plot_langs2, plot_orders_real2, plot_orders_eff2, nrow=1, widths=c(1, 1.2, 1.2))
plot

ggsave(plot=plot, "../figures/pred-eff-pred-pars-families-2.pdf", width=10, height=30)


mean((ground %>% filter(!GroundObjDir, Dependency == "aux"))$Dir)
mean((ground %>% filter(!GroundObjDir, Dependency == "mark"))$Dir)
mean((ground %>% filter(!GroundObjDir, Dependency == "cop"))$Dir)
mean((ground %>% filter(!GroundObjDir, Dependency == "acl"))$Dir)
mean((ground %>% filter(!GroundObjDir, Dependency == "xcomp"))$Dir)
mean((ground %>% filter(!GroundObjDir, Dependency == "case"))$Dir)
mean((ground %>% filter(!GroundObjDir, Dependency == "nmod"))$Dir)
mean((ground %>% filter(!GroundObjDir, Dependency == "obl"))$Dir)

