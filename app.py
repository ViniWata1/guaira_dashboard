# Importar bibliotecas ----
import pandas as pd
import plotly.express as px
from shiny import ui, App, render
from shinywidgets import output_widget, render_widget
from itables.shiny import DT
import shinyswatch


# Importar dados ----
dados = (
    pd.read_csv(
        filepath_or_buffer = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=csv",
        sep = ";",
        decimal = ",",
        converters = {"data": lambda x: pd.to_datetime(x, format = "%d/%m/%Y")}
        )
    .query("data >= '2005-01-01'")
    .assign(variacao_pct = lambda x: ((x.valor / x.valor.shift(1)) - 1) * 100)
)


# Interface do usuário ----
app_ui = ui.page_navbar(
    shinyswatch.theme.minty(),
    ui.nav(
        "Gráficos e Tabelas",
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.markdown(
                    """
                    Um texto em **negrito** ou em *itálico*.

                    Um parágrafo com um [link](https://analisemacro.com.br/).

                    - Item 1
                    - Item 2
                    - Item 3

                    ![]()
                    """
                ),
            width = 2
            ),
            ui.panel_main(
                ui.row(
                    ui.column(6, ui.output_plot("grafico_estatico")),
                    ui.column(6, output_widget("grafico_dinamico")),
                    ),
                ui.row(
                    ui.column(6, ui.output_table("tabela_estatica")),
                    ui.column(6, ui.HTML(DT(dados.tail(15))))
                    )
                )
            )
        ),
    ui.nav_control(ui.a("Análise Macro", href = "https://analisemacro.com.br/")),
    ui.nav_menu(
        "Mais",
        ui.nav_control(ui.a("Blog", href = "https://analisemacro.com.br/blog/")),
        ui.nav_control(ui.a("LinkedIn", href = "https://br.linkedin.com/company/an%C3%A1lise-macro"))
        ),
    title = ui.row(
        ui.column(7, ui.img(src = "https://i.imgur.com/Fi6Y3bY.jpg", style="max-width: 100px; max-height: 100px;")),
        ui.column(5, "Aeroporto Guaíra")
    ),
    bg = "black",
    inverse = True
)


# Servidor ----
def server(input, output, session):
    @output
    @render.plot
    def grafico_estatico():
        return dados.plot(x = "data", y = "valor", kind = "line")
    
    @output
    @render_widget
    def grafico_dinamico():
        return px.line(data_frame = dados, x = "data", y = "valor")
    
    @output
    @render.table
    def tabela_estatica():
        return dados.tail(15)


# Dashboard Shiny App ----
app = App(app_ui, server)

