library(shiny)
library(tidyverse)

ui <- fluidPage(
  titlePanel("Drowsiness Analytics Dashboard"),
  
  sidebarLayout(
    sidebarPanel(
      actionButton("refresh", "Reload Data")
    ),
    
    mainPanel(
      plotOutput("earPlot"),
      tableOutput("stats")
    )
  )
)

server <- function(input, output) {
  
  data_reactive <- eventReactive(input$refresh, {
    read_csv("logs/ear_log.csv")
  }, ignoreNULL = FALSE)
  
  output$earPlot <- renderPlot({
    data <- data_reactive()
    
    ggplot(data, aes(x = time, y = avgEAR, color = status)) +
      geom_line() +
      labs(title="Eye Aspect Ratio Over Time", x="Time", y="EAR")
  })
  
  output$stats <- renderTable({
    data <- data_reactive()
    
    data %>%
      summarise(
        avg_EAR = mean(avgEAR, na.rm = TRUE),
        closed_sec = sum(status == "CLOSED")
      )
  })
}

shinyApp(ui, server)
