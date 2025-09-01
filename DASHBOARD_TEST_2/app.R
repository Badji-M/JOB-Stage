library(shiny)
library(bs4Dash)
library(plotly)
library(leaflet)
library(DT)

ui <- dashboardPage(
  
  # --- En-tête (header) ---
  dashboardHeader(
    title = dashboardBrand(
      title = "ODD Sénégal",
      color = "primary",
      href = "#",
      image = "https://upload.wikimedia.org/wikipedia/commons/f/fd/Flag_of_Senegal.svg" # Drapeau Sénégal
    )
  ),
  
  # --- Barre latérale (sidebar) ---
  dashboardSidebar(
    skin = "light",
    status = "primary",
    sidebarMenu(
      menuItem("Accueil", tabName = "home", icon = icon("home")),
      menuItem("Par ODD", tabName = "odd", icon = icon("globe")),
      menuItem("Comparaison Régionale", tabName = "region", icon = icon("map")),
      menuItem("Téléchargements", tabName = "download", icon = icon("download"))
    )
  ),
  
  # --- Contenu principal (body) ---
  dashboardBody(
    tabItems(
      
      # --- Accueil ---
      tabItem(tabName = "home",
              fluidRow(
                valueBox(value = "42%", subtitle = "Population sous le seuil de pauvreté", icon = icon("users"), color = "danger"),
                valueBox(value = "78%", subtitle = "Taux de scolarisation", icon = icon("book"), color = "info"),
                valueBox(value = "65 ans", subtitle = "Espérance de vie", icon = icon("heartbeat"), color = "success")
              ),
              fluidRow(
                box(title = "Évolution de la pauvreté", width = 6, collapsible = TRUE, plotlyOutput("plot1")),
                box(title = "Carte d'accès à l'eau potable", width = 6, collapsible = TRUE, leafletOutput("map"))
              )
      ),
      
      # --- Par ODD ---
      tabItem(tabName = "odd",
              fluidRow(
                box(title = "Sélectionnez un ODD", width = 12, 
                    selectInput("choix_odd", "Choisir un objectif :", 
                                choices = paste("ODD", 1:17),
                                selected = "ODD 1"))
              ),
              fluidRow(
                box(title = "Indicateur principal", width = 6, plotlyOutput("odd_plot")),
                box(title = "Tableau des données", width = 6, DTOutput("odd_table"))
              )
      ),
      
      # --- Comparaison Régionale ---
      tabItem(tabName = "region",
              fluidRow(
                box(title = "Carte par région", width = 8, leafletOutput("region_map")),
                box(title = "Filtre", width = 4,
                    selectInput("indic_region", "Choisir un indicateur :", 
                                choices = c("Pauvreté", "Éducation", "Santé"))
                )
              )
      ),
      
      # --- Téléchargements ---
      tabItem(tabName = "download",
              fluidRow(
                box(title = "Téléchargez les données", width = 12,
                    downloadButton("download_csv", "Télécharger en CSV"),
                    downloadButton("download_pdf", "Télécharger en PDF")
                )
              )
      )
    )
  )
)

server <- function(input, output, session) {
  
  # Exemple graphique Accueil
  output$plot1 <- renderPlotly({
    plot_ly(x = 2000:2025, y = runif(26, 30, 50), type = 'scatter', mode = 'lines+markers')
  })
  
  # Exemple carte Accueil
  output$map <- renderLeaflet({
    leaflet() %>% addTiles() %>%
      addMarkers(lng = -17.45, lat = 14.69, popup = "Dakar")
  })
  
  # Exemple graphique ODD
  output$odd_plot <- renderPlotly({
    plot_ly(x = 2010:2025, y = runif(16, 40, 80), type = 'bar', name = input$choix_odd)
  })
  
  # Exemple tableau ODD
  output$odd_table <- renderDT({
    data.frame(Année = 2010:2025, Valeur = runif(16, 40, 80))
  })
  
  # Carte région
  output$region_map <- renderLeaflet({
    leaflet() %>% addTiles() %>%
      addCircles(lng = -17.45, lat = 14.69, popup = "Dakar", radius = 50000)
  })
  
  # Téléchargements
  output$download_csv <- downloadHandler(
    filename = function() {"indicateurs_ODD.csv"},
    content = function(file) {
      write.csv(data.frame(Année = 2010:2025, Valeur = runif(16, 40, 80)), file, row.names = FALSE)
    }
  )
  
  output$download_pdf <- downloadHandler(
    filename = function() {"rapport_ODD.pdf"},
    content = function(file) {
      # Ici tu pourrais générer un PDF avec rmarkdown ou reportlab
      writeLines("Rapport PDF ODD - Sénégal", file)
    }
  )
}

shinyApp(ui, server)
