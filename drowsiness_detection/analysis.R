library(ggplot2)

data <- read.csv("ear_log.csv")

ggplot(data, aes(x = time, y = ear)) +
  geom_line(color = "blue", size = 1) +
  geom_point(aes(color = as.factor(is_drowsy)), size = 2) +
  scale_color_manual(values = c("0" = "black", "1" = "red"),
                     labels = c("Awake", "Drowsy"),
                     name = "State") +
  geom_hline(yintercept = 0.24, color = "red", linetype = "dashed") +
  labs(title = "Eye Aspect Ratio (EAR) Over Time",
       x = "Time (seconds)",
       y = "EAR") +
  theme_minimal()
