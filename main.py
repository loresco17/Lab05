import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    new_tipo=''
    new_marca=''
    new_anno=''
    new_valore=0
    def handleAdd(val):
        val = txtout.value
        txtout.value = int(val) + 1
        txtout.update()

    def handleRemove(val):
        val = txtout.value
        txtout.value = int(val) - 1
        txtout.update()
    input_tipo=ft.TextField(value=new_tipo, label="Tipo")
    input_marca=ft.TextField(value=new_marca, label="Marca")
    input_anno=ft.TextField(value=new_anno, label="Anno acquisto")
    minus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=handleRemove)
    add = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)
    txtout = ft.TextField(width=100, disabled=True,
                          value='0',
                          text_align=ft.TextAlign.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    def aggiungi_strumento_ft(tipo, marca, anno, valore):
        try :
            return deposito.aggiungi_strumento(tipo, marca, int(anno), float(valore))
        except ValueError:
            return alert.show_alert("Valori non validi")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi_strumento = ft.ElevatedButton("Aggiungi strumento", on_click=aggiungi_strumento_ft(new_tipo, new_marca, new_anno, new_valore))

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(spacing=200,
               controls=[input_tipo, input_marca, input_anno, minus, txtout, add,
                         pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
