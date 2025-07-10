import sqlite3
import os
import base64
import random
import string

from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog

# === Verschlüsselungsschlüssel laden oder erstellen ===
def schluessel_laden():
    if not os.path.exists("key.key"):
        schluessel = Fernet.generate_key()
        with open("key.key", "wb") as datei:
            datei.write(schluessel)
    else:
        with open("key.key", "rb") as datei:
            schluessel = datei.read()
    return Fernet(schluessel)

f = schluessel_laden()

# === Datenbank vorbereiten ===
def datenbank_erstellen():
    conn = sqlite3.connect("passwoerter.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eintraege (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dienst TEXT NOT NULL,
            benutzer TEXT NOT NULL,
            passwort TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

datenbank_erstellen()

# === Passwort-Verschlüsselung ===
def passwort_verschluesseln(pw):
    return base64.b64encode(f.encrypt(pw.encode())).decode()

def passwort_entschluesseln(pw_verschluesselt):
    return f.decrypt(base64.b64decode(pw_verschluesselt)).decode()

# === Passwortgenerator ===
def passwort_generieren(laenge=16):
    zeichen = string.ascii_letters + string.digits + "!@#$%&*?"
    return ''.join(random.choice(zeichen) for _ in range(laenge))

# === Passwort speichern ===
def eintrag_speichern(dienst, benutzer, passwort):
    pw_verschluesselt = passwort_verschluesseln(passwort)
    conn = sqlite3.connect("passwoerter.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO eintraege (dienst, benutzer, passwort)
        VALUES (?, ?, ?)
    """, (dienst, benutzer, pw_verschluesselt))
    conn.commit()
    conn.close()

# === Einträge anzeigen ===
def eintraege_anzeigen():
    conn = sqlite3.connect("passwoerter.db")
    cursor = conn.cursor()
    cursor.execute("SELECT dienst, benutzer, passwort FROM eintraege")
    daten = cursor.fetchall()
    conn.close()

    textfeld.delete("1.0", tk.END)
    for dienst, benutzer, verschluesselt in daten:
        pw = passwort_entschluesseln(verschluesselt)
        textfeld.insert(tk.END, f"Dienst: {dienst}\nBenutzer: {benutzer}\nPasswort: {pw}\n\n")

# === Eintrag löschen ===
def eintrag_loeschen():
    dienst = simpledialog.askstring("Eintrag löschen", "Welchen Dienst möchtest du löschen?")
    if not dienst:
        return
    conn = sqlite3.connect("passwoerter.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eintraege WHERE dienst = ?", (dienst,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Eintrag gelöscht", f"Alle Einträge für '{dienst}' wurden gelöscht.")

# === Neues Passwort hinzufügen ===
def neues_passwort_fenster():
    dienst = simpledialog.askstring("Dienst", "Für welchen Dienst?")
    benutzer = simpledialog.askstring("Benutzername", "Benutzername:")
    passwort = simpledialog.askstring("Passwort", "Passwort:")

    if dienst and benutzer and passwort:
        eintrag_speichern(dienst, benutzer, passwort)
        messagebox.showinfo("Gespeichert", "Eintrag wurde gespeichert.")

# === Passwortgenerator-Popup ===
def passwort_generieren_popup():
    try:
        laenge = simpledialog.askinteger("Länge", "Wie lang soll das Passwort sein?", minvalue=6, maxvalue=64)
        if laenge:
            pw = passwort_generieren(laenge)
            fenster.clipboard_clear()
            fenster.clipboard_append(pw)
            messagebox.showinfo("Passwort generiert", f"Passwort:\n{pw}\n\n(Kopiert in Zwischenablage)")
    except:
        messagebox.showerror("Fehler", "Ungültige Eingabe.")

# === GUI starten ===
def starten():
    if simpledialog.askstring("Masterpasswort", "Bitte gib das Masterpasswort ein:") != "1887":
        messagebox.showerror("Fehler", "Falsches Passwort!")
        return

    global fenster, textfeld
    fenster = tk.Tk()
    fenster.title("🔐 Passwortmanager")
    fenster.geometry("500x600")
    fenster.configure(bg="#1e1e1e")

    titel = tk.Label(fenster, text="Passwortmanager", font=("Helvetica", 18, "bold"), bg="#1e1e1e", fg="#00ffcc")
    titel.pack(pady=10)

    frame = tk.Frame(fenster, bg="#1e1e1e")
    frame.pack(pady=10)

    def neuer_button(text, command):
        return tk.Button(frame, text=text, command=command,
                         font=("Helvetica", 12),
                         bg="#333", fg="white", activebackground="#555", activeforeground="#00ffcc", width=30)

    neuer_button("➕ Neues Passwort", neues_passwort_fenster).pack(pady=5)
    neuer_button("🔐 Passwort generieren", passwort_generieren_popup).pack(pady=5)
    neuer_button("📋 Alle anzeigen", eintraege_anzeigen).pack(pady=5)
    neuer_button("🗑️ Eintrag löschen", eintrag_loeschen).pack(pady=5)

    # === Scrollbares Textfeld ===
    text_rahmen = tk.Frame(fenster)
    text_rahmen.pack(pady=10)

    scrollbar = tk.Scrollbar(text_rahmen)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    textfeld = tk.Text(text_rahmen, width=60, height=20, bg="#2a2a2a", fg="#ffffff", insertbackground="white", yscrollcommand=scrollbar.set)
    textfeld.pack()

    scrollbar.config(command=textfeld.yview)

    fenster.mainloop()
starten()