import tkinter as tk
from tkinter import ttk, messagebox
import requests
from io import BytesIO
from PIL import Image, ImageTk

API_URL = "https://www.thecocktaildb.com/api/json/v1/1/search.php"
TIMEOUT = 10


class CocktailFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Cocktail Finder")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#171923")

        self.drinks = []
        self.current_image = None

        self.configure_style()
        self.create_widgets()

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TButton",
            font=("Arial", 11, "bold"),
            padding=8,
            background="#e0a458",
            foreground="#171923"
        )
        style.map("TButton", background=[("active", "#f2bd75")])
        style.configure(
            "TEntry",
            padding=8,
            fieldbackground="#2d3345",
            foreground="#ffffff"
        )

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#171923", padx=24, pady=20)
        header.pack(fill="x")

        tk.Label(
            header, text="COCKTAIL FINDER",
            font=("Arial", 25, "bold"),
            fg="#f2bd75", bg="#171923"
        ).pack(anchor="w")

        tk.Label(
            header, text="Finde Rezepte, Zutaten und Zubereitungsanleitungen.",
            font=("Arial", 11), fg="#c5c9d6", bg="#171923"
        ).pack(anchor="w", pady=(4, 14))

        search_row = tk.Frame(header, bg="#171923")
        search_row.pack(fill="x")

        self.search_entry = ttk.Entry(search_row, font=("Arial", 12))
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.insert(0, "margarita")
        self.search_entry.bind("<Return>", lambda event: self.search_cocktails())

        ttk.Button(
            search_row, text="Suchen", command=self.search_cocktails
        ).pack(side="left", padx=(10, 0))

        content = tk.Frame(self.root, bg="#171923", padx=24, pady=8)
        content.pack(fill="both", expand=True)

        left = tk.Frame(content, bg="#242a3a", padx=12, pady=12)
        left.pack(side="left", fill="y", padx=(0, 14))

        tk.Label(
            left, text="Suchergebnisse", font=("Arial", 14, "bold"),
            fg="#ffffff", bg="#242a3a"
        ).pack(anchor="w", pady=(0, 10))

        self.result_list = tk.Listbox(
            left, width=27, height=25, font=("Arial", 11),
            bg="#2d3345", fg="#ffffff",
            selectbackground="#bd8243", selectforeground="#171923",
            relief="flat", borderwidth=0, activestyle="none"
        )
        self.result_list.pack(fill="y", expand=True)
        self.result_list.bind("<<ListboxSelect>>", self.show_selected_cocktail)

        right = tk.Frame(content, bg="#242a3a", padx=18, pady=16)
        right.pack(side="left", fill="both", expand=True)

        self.name_label = tk.Label(
            right, text="Willkommen beim Cocktail Finder",
            font=("Arial", 20, "bold"), fg="#f2bd75",
            bg="#242a3a", wraplength=600, justify="left"
        )
        self.name_label.pack(anchor="w")

        self.meta_label = tk.Label(
            right, text="Suche nach einem Cocktail, um Details zu sehen.",
            font=("Arial", 10), fg="#c5c9d6", bg="#242a3a"
        )
        self.meta_label.pack(anchor="w", pady=(5, 12))

        self.image_label = tk.Label(right, bg="#242a3a")
        self.image_label.pack(anchor="w", pady=(0, 12))

        tk.Label(
            right, text="Zutaten", font=("Arial", 14, "bold"),
            fg="#f2bd75", bg="#242a3a"
        ).pack(anchor="w")

        self.ingredients_text = tk.Text(
            right, height=7, wrap="word", font=("Arial", 10),
            bg="#2d3345", fg="#ffffff", relief="flat",
            padx=10, pady=8
        )
        self.ingredients_text.pack(fill="x", pady=(5, 12))
        self.ingredients_text.configure(state="disabled")

        tk.Label(
            right, text="Zubereitung", font=("Arial", 14, "bold"),
            fg="#f2bd75", bg="#242a3a"
        ).pack(anchor="w")

        self.instructions_text = tk.Text(
            right, height=8, wrap="word", font=("Arial", 10),
            bg="#2d3345", fg="#ffffff", relief="flat",
            padx=10, pady=8
        )
        self.instructions_text.pack(fill="both", expand=True, pady=(5, 0))
        self.instructions_text.configure(state="disabled")

        self.status_label = tk.Label(
            self.root, text="Bereit", anchor="w",
            font=("Arial", 9), fg="#c5c9d6", bg="#171923", padx=24, pady=8
        )
        self.status_label.pack(fill="x")

    def search_cocktails(self):
        """Sendet eine GET-Anfrage und verarbeitet die JSON-Antwort."""
        search_term = self.search_entry.get().strip()

        if not search_term:
            messagebox.showwarning("Eingabe fehlt", "Bitte einen Cocktailnamen eingeben.")
            return

        self.status_label.config(text="Suche läuft ...")
        self.root.update_idletasks()

        try:
            response = requests.get(
                API_URL, params={"s": search_term}, timeout=TIMEOUT
            )
            response.raise_for_status()

            # Die JSON-Antwort wird in Python-Daten (Dictionary/Listen) umgewandelt.
            data = response.json()
            self.drinks = data.get("drinks") or []

            self.result_list.delete(0, tk.END)

            if not self.drinks:
                self.clear_details()
                self.status_label.config(text="Keine Cocktails gefunden.")
                messagebox.showinfo(
                    "Keine Ergebnisse",
                    f"Für '{search_term}' wurden keine Cocktails gefunden."
                )
                return

            for drink in self.drinks:
                self.result_list.insert(tk.END, drink.get("strDrink", "Unbekannt"))

            self.result_list.selection_set(0)
            self.result_list.event_generate("<<ListboxSelect>>")
            self.status_label.config(
                text=f"{len(self.drinks)} Cocktail(s) gefunden."
            )

        except requests.exceptions.Timeout:
            self.status_label.config(text="Zeitüberschreitung")
            messagebox.showerror("Verbindungsfehler", "Die API antwortet nicht rechtzeitig.")
        except requests.exceptions.HTTPError as error:
            self.status_label.config(text="HTTP-Fehler")
            messagebox.showerror("HTTP-Fehler", f"Die API-Anfrage war nicht erfolgreich:\n{error}")
        except requests.exceptions.RequestException as error:
            self.status_label.config(text="Verbindungsfehler")
            messagebox.showerror("Verbindungsfehler", str(error))
        except ValueError:
            self.status_label.config(text="Ungültige JSON-Antwort")
            messagebox.showerror("Datenfehler", "Die Antwort konnte nicht als JSON gelesen werden.")

    def show_selected_cocktail(self, event=None):
        """Zeigt die Details des ausgewählten Cocktails an."""
        selection = self.result_list.curselection()
        if not selection:
            return

        drink = self.drinks[selection[0]]
        self.name_label.config(text=drink.get("strDrink") or "Unbekannter Cocktail")

        category = drink.get("strCategory") or "Keine Angabe"
        alcoholic = drink.get("strAlcoholic") or "Keine Angabe"
        glass = drink.get("strGlass") or "Keine Angabe"
        self.meta_label.config(
            text=f"{category}  |  {alcoholic}  |  Glas: {glass}"
        )

        ingredient_lines = []
        for number in range(1, 16):
            ingredient = drink.get(f"strIngredient{number}")
            measure = drink.get(f"strMeasure{number}")
            if ingredient and ingredient.strip():
                amount = measure.strip() if measure and measure.strip() else ""
                ingredient_lines.append(f"• {amount} {ingredient}".strip())

        self.set_text(self.ingredients_text, "\n".join(ingredient_lines) or "Keine Zutaten angegeben.")

        instructions = (
            drink.get("strInstructionsDE")
            or drink.get("strInstructions")
            or "Keine Zubereitung angegeben."
        )
        self.set_text(self.instructions_text, instructions)

        self.load_image(drink.get("strDrinkThumb"))

    def set_text(self, widget, content):
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", content)
        widget.configure(state="disabled")

    def load_image(self, image_url):
        """Lädt das Cocktailbild und zeigt es verkleinert an."""
        self.current_image = None
        self.image_label.config(image="", text="")

        if not image_url:
            self.image_label.config(text="Kein Bild verfügbar", fg="#c5c9d6")
            return

        try:
            response = requests.get(image_url, timeout=TIMEOUT)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))
            image.thumbnail((220, 180))
            self.current_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.current_image)
        except (requests.exceptions.RequestException, OSError):
            self.image_label.config(
                text="Bild konnte nicht geladen werden.", fg="#c5c9d6"
            )

    def clear_details(self):
        self.name_label.config(text="Keine Ergebnisse")
        self.meta_label.config(text="")
        self.image_label.config(image="", text="")
        self.set_text(self.ingredients_text, "")
        self.set_text(self.instructions_text, "")


if __name__ == "__main__":
    root = tk.Tk()
    app = CocktailFinder(root)
    root.mainloop()
