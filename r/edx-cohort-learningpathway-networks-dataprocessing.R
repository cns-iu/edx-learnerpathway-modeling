#### Set up environment ####

#Load packages
library(plyr)
library(dplyr)
library(magrittr)
library(igraph)
library(ggplot2)
library(ggraph)
#library(ggnetwork)

#Set paths to data
#path_data <- "W:/data/edx/mitxpro-amxb-1t2018"
#path_output <- "W:/data/sow2.1-AM-course"
#path_output <- "W:/data/sow2.2-LAAL/MITxPRO-LASERxB1-1T2019"
#path_output <- "W:/data/sow2.2-LAAL/MITxPRO-LASERxBw-1T2019"


#Checks if a user has previously assign a path with a prior script 
#If false, lets user assign path to previous processing output files of an
#edX course using the a previous processing scripts from this pipeline.
if(exists("path_output")==FALSE){
  path_output = tclvalue(tkchooseDirectory())
}

#### Load relevant data ####
#The pattern parameter identifies the outputs of the edX-1-studentUserList.R script
users <- read.csv(list.files(full.names = T, recursive = FALSE, 
                             path = paste0(path_output,"/analysis/studentActivity/"),
                             pattern = "-selectedActivity.csv$"), header=T)[c(1,6,7,10,11,13,15:17)]

#Read in course structure - processed
courseStr <- read.csv(list.files(full.names = TRUE, recursive = FALSE, 
                                 path = paste0(path_output,"/course/"),
                                 pattern = "modules.csv"),header=T)
courseID <- gsub("\\+","\\-",courseStr$courseID)[1]

#Read in a list of student edges, append data to master edge list
fileEdges <- list.files(full.names = TRUE, recursive = FALSE, 
                        path = paste0(path_output,"/networks/edges/"),
                        pattern = ".csv$")

#### Create list of students' aggregated course pathway network ####
# Temp dataframes for aggregating data
tmp <- NA
# List for sa
stdNetList <- NA
# Sets session condition for loop calculations
# Sess= F, no sessions are considered in the student networks
# Sess= T, session data is preserved in the student networks
sess <- F
# Loop for aggregating individual student's course pathways logs
# and adding to the student list.
for(i in 1:length(fileEdges)){
  message("Processing edge list ", i, " of ", length(fileEdges))
  #Read in edge list
  tmp <- read.csv(fileEdges[i])[c(1,2,8:13)]
  #Fix dir labels for self loops
  if(length(tmp[tmp$sl==1,]$sl)){
    tmp[tmp$sl==1,]$dir <- 's'
  }
  #Refactoring session identifiers
  tmp$t.tsession <- factor(tmp$t.tsession)
  levels(tmp$t.tsession) <- seq_along(levels(tmp$t.tsession))
  tmp$t.tsession <- as.numeric(tmp$t.tsession)
  #Update from and to fields with temporal session identifier
  tmp$from_s <- paste0(tmp$from,"-",tmp$t.tsession)
  tmp$to_s <- paste0(tmp$to,"-",tmp$t.tsession)
  #Value added for summing up edge count
  tmp$val <- 1
  #Add sequence value to data
  tmp$seq <- rownames(tmp)
  #Aggregate function
  #Check to aggregate by student session or not
  if(sess==T){
    ddply(tmp, .(from,to,user_id,t.tsession), summarize,
          weight = sum(val),
          dis = mean(dis),
          sl = mean(sl),
          seq_min = as.numeric(min(seq))) %>% 
      arrange(t.tsession,seq_min)
  } else {
    tmp <- ddply(tmp, .(from,to,user_id), summarize,
                 weight = sum(val),
                 dis = mean(dis),
                 sl = mean(sl),
                 seq_min = as.numeric(min(seq))) %>% 
           arrange(seq_min)
  }
  #Appends network to list of all student pathway networks
  if(is.data.frame(stdNetList)==F){
    stdNetList <- tmp
  } else {
    stdNetList <- bind_rows(stdNetList,tmp)  
  }
}
 rm(tmp)

#### Revising distance measure for nodes ####
#Old order based on full tree order with course structure data
#Log data does not preserve structural actions, and so distances values are larger than
#nodes in network representation
#Subset content modules from course structure (Levels 0-3 are organizational modules)
courseStr <- courseStr[courseStr$treelevel==4,][c(2:3,4,7,10:12)]
#Sets new order (linear), but preserves tree sort order values
courseStr$orderNew <- 1:nrow(courseStr)
#Check to see of process preserves sessions or not
if(sess==T){
  #Needs testing
  #Rename course structure fields to join
  names(courseStr)[c(1,8)] <- c("from_o","ordF")
  #Update from nodes order values for 'from' nodes
  stdNetList <- join(stdNetList,courseStr[,c(1,8)], by="from_o")
  #Rename course structure fields for join
  names(courseStr)[c(1,8)] <- c("to_o","ordT")
  #Update to nodes order values for 'to' nodes
  stdNetList <- join(stdNetList,courseStr[,c(1,8)], by="to_o")
  #Rename course structure fields for join 
  names(courseStr)[c(1,8)] <- c("id","orderNew")
} else {
  #Rename course structure fields for join 
  names(courseStr)[c(1,8)] <- c("from","ordF")
  #Update from and to node order values for 'from' nodes
  stdNetList <- join(stdNetList,courseStr[,c(1,8)], by="from")
  #Rename course structure fields for join 
  names(courseStr)[c(1,8)] <- c("to","ordT")
  #Update from and to node order values for 'to' nodes
  stdNetList <- join(stdNetList,courseStr[,c(1,8)], by="to")
  #Rename course structure fields for clarity
  names(courseStr)[c(1,8)] <- c("id","orderNew")
}
#Calculate revised distance measure with new order values
stdNetList$dis <- stdNetList$ordT - stdNetList$ordF
names(stdNetList)[8] <- "order"
stdNetList <- stdNetList[,1:8]

#### Export list of aggregated student pathway networks
#Saving list of students' aggregated edge lists
if(sess==T){
  write.csv(stdNetList, paste0(path_output,"/networks/",courseStr$courseID[1],"-stdAgg-edgeList-sessionLevel.csv"),
            row.names = F)
} else {
  write.csv(stdNetList, paste0(path_output,"/networks/",courseStr$courseID[1],"-stdAgg-edgeList.csv"),
            row.names = F)
}

#### Overall student pathway network edge and node lists (aggregated for whole course) ####
#Aggegate to an overall network for all students
if(sess==T){
  # Add to this section
  
  
  
  
  # write.csv(stdNetList, paste0(path_output,"/networks/",courseStr$courseID[1],"-stdAgg-edges-sessionLevel.csv"),
  #           row.names = F)
  
  
  
  
  
  # write.csv(nodes, paste0(path_output,"/networks/",courseStr$courseID[1],"-stdAgg-nodes-sessionLevel.csv"),
  #           row.names = F)
} else {
  #Calculate edge list stats
  edges <- ddply(stdNetList,.(from,to),summarize,
                 stds = length(unique(user_id)),
                 weight = sum(weight),
                 dis = mean(disRevised),
                 sl = mean(sl))
  #Save edge list
  write.csv(edges, paste0(path_output,"/networks/",courseStr$courseID[1],"-stdAgg-edges.csv"),
            row.names = F)
  #Calculate node stats
  nodes <- ddply(stdNetList,.(from),summarize,
                 stds = length(unique(user_id)),
                 count = sum(weight))
  #Append nodes with course structure data
  names(courseStr)[1] <- names(nodes)[1] <- "name"
  names(courseStr)[c(4,8)] <- c("order_o","order")
  nodes <- join(courseStr[,c(1:3,8,5:7)],nodes,"name")
  #Replace NA values with 0
  nodes[is.na(nodes[,c(9)]),c(9)] <- 0
  nodes[is.na(nodes[,c(8)]),c(8)] <- 0
  #Save node list
  write.csv(nodes, paste0(path_output,"/networks/",courseStr$courseID[1],"-stdAgg-nodes.csv"),
            row.names = F)
}

#Agg Studen Pathway Net Density
nrow(edges)/length(nodes$name)^2
nrow(edges)/length(unique(edges$to))^2

#Create a graph of the network
g <- graph_from_data_frame(d=edges, vertices=nodes, directed=T)
