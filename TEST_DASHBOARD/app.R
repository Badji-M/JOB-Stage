library(shiny)
library(bs4Dash)
library(plotly)
library(leaflet)
  

ui <- dashboardPage(
  dashboardHeader(title = "Tableau de bord ODD"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Accueil", tabName = "home", icon = icon("home")),
      menuItem("Par ODD", tabName = "odd", icon = icon("globe")),
      menuItem("Comparaison Régionale", tabName = "region", icon = icon("map")),
      menuItem("Téléchargement", tabName = "download", icon = icon("download"))
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(tabName = "home",
              fluidRow(
                valueBoxOutput("poverty"),
                valueBoxOutput("education"),
                valueBoxOutput("health")
              ),
              fluidRow(
                box(title = "Évolution de la pauvreté", width = 6, plotlyOutput("plot1")),
                box(title = "Carte d'accès à l'eau", width = 6, leafletOutput("map"))
              )
      )
    )
  )
)

server <- function(input, output, session) {
  output$poverty <- renderValueBox({
    valueBox("42%", "Population sous le seuil de pauvreté", icon = icon("users"), color = "danger")
  })
  
  output$education <- renderValueBox({
    valueBox("78%", "Taux de scolarisation", icon = icon("book"), color = "info")
  })
  
  output$health <- renderValueBox({
    valueBox("65 ans", "Espérance de vie", icon = icon("heartbeat"), color = "success")
  })
  
  output$plot1 <- renderPlotly({
    plot_ly(x = 2000:2025, y = runif(26, 30, 50), type = 'scatter', mode = 'lines+markers')
  })
  
  output$map <- renderLeaflet({
    leaflet() %>%
      addTiles() %>%
      addMarkers(lng = -17.45, lat = 14.69, popup = "Dakar")
  })
}

#Téléchagement

shinyApp(ui, server)


