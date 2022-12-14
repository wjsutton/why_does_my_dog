
library(dplyr)

build_segment <- function(min,max,increment,inner_radius,outer_radius){
  x <- c()
  y <- c()
  
  for(i in seq(min, max, increment)){
    x1 <- inner_radius * sin(2*pi*(i/360))
    y1 <- inner_radius * cos(2*pi*(i/360))
    x <- c(x,x1)
    y <- c(y,y1)
  }
  
  for(j in seq(max, min, -increment)){
    x2 <- outer_radius * sin(2*pi*(j/360))
    y2 <- outer_radius * cos(2*pi*(j/360))
    x <- c(x,x2)
    y <- c(y,y2)
  }
  
  path <- 1:length(x)
  
  df <- data.frame(x = x,y = y,path = path,stringsAsFactors = F)
  return(df)
}

dog_df <- read.csv("why_does_my_dog.csv",stringsAsFactors = F)
names(dog_df)[1] <- 'title'
head(dog_df)

sizes <- c('Small','Medium','Large')

for(s in 1:length(sizes)){
  print(s)
  size <- sizes[s]

  n_rings <- length(unique(filter(dog_df,Size==size)$title))
  n_questions <- 100
  radius_start <- 4
  radius_increase <- 1.5
  
  inner_radius <- c()
  outer_radius <- c()
  
  for(r in 1:n_rings){
    inner_radius <- c(inner_radius,rep(radius_start + (radius_increase*(r-1)),n_questions))
    outer_radius <- c(outer_radius,rep(radius_start + (radius_increase*(r)),n_questions))
  }
  
  min <- rep(0:(n_questions-1) *(360/n_questions),n_rings)
  max <- rep(1:n_questions *(360/n_questions),n_rings)
  increment <- rep(360/(n_questions*10),n_questions * n_rings)
  
  levels_df <- data.frame(min = min,
                          max = max,
                          increment = increment,
                          inner_radius = inner_radius,
                          outer_radius = outer_radius,
                          stringsAsFactors = F)
  
  
  n <- nrow(levels_df)
  
  sunburst_list = vector("list", length = n)
  
  for(a in 1:nrow(levels_df)){
    
    df <- build_segment(levels_df$min[a],levels_df$max[a],levels_df$increment[a],levels_df$inner_radius[a],levels_df$outer_radius[a])
    df$id <- a
    df$ring <- floor(a / (n_questions+1)) + 1
    df$segment <- ifelse((a %% n_questions)==0,n_questions,(a %% n_questions)) - (100-73)
    df$size <- size
    sunburst_list[[a]] <- df
  }
  sunburst_df <- do.call(rbind, sunburst_list)
  
  if(size == 'Large'){
    large_sun <- filter(sunburst_df,size == 'Large')
  }
  if(size == 'Medium'){
    med_sun <- filter(sunburst_df,size == 'Medium')
  }
  if(size == 'Small'){
    small_sun <- filter(sunburst_df,size == 'Small')
  }
}
sunburst_df <- rbind(large_sun,med_sun,small_sun)

write.csv(sunburst_df,"test_sunburst.csv",row.names = F)

