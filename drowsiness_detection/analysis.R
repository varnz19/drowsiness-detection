library(tidyverse)

# Read log
data <- read_csv("logs/ear_log.csv")

# Basic stats
summary <- data %>%
  summarise(
    avg_EAR = mean(avgEAR, na.rm = TRUE),
    min_EAR = min(avgEAR, na.rm = TRUE),
    max_EAR = max(avgEAR, na.rm = TRUE),
    closed_seconds = sum(status == "CLOSED")
  )

print(summary)

# Plot RAW EAR
ggplot(data, aes(x = time, y = avgEAR, color = status)) +
  geom_line() +
  labs(title="Eye Aspect Ratio Over Time", x="Time", y="EAR")
