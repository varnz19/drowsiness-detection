# app.R
library(shiny)
library(DT)        # for interactive tables
library(ggplot2)   # for plots

# Load sample data from CSV
mock_data <- read.csv("drowsiness.csv", stringsAsFactors = FALSE)
mock_data$Time <- as.POSIXct(mock_data$Time, format="%Y-%m-%d %H:%M:%S")

# UI
ui <- fluidPage(
  titlePanel("Drowsiness Detection Dashboard"),
  
  sidebarLayout(
    sidebarPanel(
      sliderInput("nrows", "Number of recent records to show:", 5, 50, 10),
      actionButton("alertBtn", "Simulate Drowsiness Alert"),
      hr(),
      h4("Instructions:"),
      p("This dashboard shows sample drowsiness detection data."),
      p("EAR = Eye Aspect Ratio; lower values may indicate drowsiness.")
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("Table", DTOutput("data_table")),
        tabPanel("Plot", plotOutput("ear_plot")),
        tabPanel("Summary", verbatimTextOutput("summary_text")),
        tabPanel("Alerts", verbatimTextOutput("alerts"))
      )
    )
  )
)

# Server
server <- function(input, output, session) {
  
  # Reactive dataset based on slider
  reactive_data <- reactive({
    tail(mock_data, input$nrows)
  })
  
  # Render DataTable
  output$data_table <- renderDT({
    datatable(reactive_data(), options = list(pageLength = 5))
  })
  
  # Render Plot
  output$ear_plot <- renderPlot({
    ggplot(reactive_data(), aes(x = Time, y = EAR, color = Status)) +
      geom_line(size=1) + geom_point(size=2) +
      theme_minimal() +
      labs(title = "Eye Aspect Ratio over Time", x = "Time", y = "EAR")
  })
  
  # Summary stats
  output$summary_text <- renderPrint({
    df <- reactive_data()
    cat("Summary of EAR values:\n")
    print(summary(df$EAR))
    cat("\nDrowsy count:", sum(df$Status == "Drowsy"), "\n")
    cat("Awake count:", sum(df$Status == "Awake"), "\n")
  })
  
  # Alerts
  alerts <- reactiveVal("No alerts yet.")
  
  observeEvent(input$alertBtn, {
    new_alert <- paste(Sys.time(), "- Drowsiness detected! Be careful.")
    alerts(new_alert)
  })
  
  output$alerts <- renderText({
    alerts()
  })
  
}

# Run the app
shinyApp(ui = ui, server = server)
