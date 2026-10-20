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
    input_tipo=ft.TextField(label="Tipo")
    input_marca=ft.TextField(label="Marca")
    input_anno=ft.TextField(label="Anno acquisto")
    txtout = ft.TextField(width=50, disabled=True,
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

    def aggiungi_strumento_ft(e):
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        anno_str = input_anno.value.strip()
        valore_str = txtout.value.strip()
        if not tipo or not marca:
            alert.show_alert("❌ Inserire tipo e marca dello strumento.")
            return
        try:
            anno=int(anno_str)
            valore=float(valore_str)
        except ValueError:
            alert.show_alert("❌ Anno di acquisto o valore non validi: inserire valori numerici.")
            return
        deposito.aggiungi_strumento(tipo, marca, anno, valore)
        input_tipo.value=""
        input_marca.value=""
        input_anno.value=""
        txtout.value="0"
        aggiorna_lista_strumenti()

    def handleAdd(e):
        val=int(txtout.value)
        txtout.value=str(val+1)
        txtout.update()

    def handleRemove(e):
        val=int(txtout.value)
        if val>0:
            txtout.value=str(val-1)
            txtout.update()

    # --- EVENTI ---
    toggle_cambia_tema=ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile=ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    minus=ft.IconButton(
        icon=ft.Icons.REMOVE,
        icon_color="red",
        icon_size=20,
        on_click=handleRemove
    )
    add=ft.IconButton(
        icon=ft.Icons.ADD,
        icon_color="green",
        icon_size=20,
        on_click=handleAdd
    )

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi_strumento=ft.ElevatedButton("Aggiungi strumento", on_click=aggiungi_strumento_ft)

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
        ft.Divider(),
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(spacing=20,
               controls=[input_tipo, input_marca, input_anno, minus, txtout, add],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
