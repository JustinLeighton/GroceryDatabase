
# Import packages
library(tidyverse)

# Set working directory
setwd("C:/Users/Justin Leighton/Desktop/Development/Grocery Database/BurrowDB/finance/backups")

# Loop through files and concatenate data
files <- list.files(pattern = "*.csv")
dfs <- list()
for(i in files){
  dfs[[i]] <- read.csv(i, header=T)
}
gc()
df <- do.call(rbind, dfs)

# Format fields
df <- df %>%
  mutate(Date = as.Date(Date, format="%Y-%m-%d"),
         Amount = as.numeric(Amount))

# Month start function
monthStart <- function(x) {
  x <- as.POSIXlt(x)
  x$mday <- 1
  as.Date(x)
}



df %>%
  filter(Source == "Expense") %>%
  filter(Category == "Food") %>%
  mutate(Date = monthStart(Date)) %>% 
  group_by(Date) %>%
  summarise(Amount = sum(Amount)) %>%
  ggplot(aes(x = Date, y = Amount)) +
  geom_line()
