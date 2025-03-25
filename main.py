from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import Font

salles = []

class DomotiqueApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartHome Manager")
        self.geometry("800x600")
        self.configure(padx=25, pady=25, bg='#F0F0F0')
        
        # Configuration des styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._setup_styles()
        
        self.main_menu()

    def _setup_styles(self):
        self.style.configure('Titre.TLabel', 
                           font=('Helvetica', 16, 'bold'), 
                           foreground='#2C3E50',
                           background='#F0F0F0')
                           
        self.style.configure('Bouton.TButton', 
                           font=('Arial', 10), 
                           padding=10,
                           foreground='white',
                           background='#3498DB')
                           
        self.style.map('Bouton.TButton',
                     background=[('active', '#2980B9')])
                     
        self.style.configure('Entry.TEntry', 
                           padding=5,
                           relief='flat',
                           fieldbackground='#ECF0F1')

        self.style.configure('Switch.TCheckbutton', 
                           width=10,
                           relief='raised',
                           padding=5)
        self.style.map('Switch.TCheckbutton',
                     relief=[('selected', 'sunken'), ('!selected', 'raised')],
                     background=[('selected', '#4CAF50'), ('!selected', '#F44336')])

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_frame()
        ttk.Label(self, text="🏠 SmartHome Manager", style='Titre.TLabel').pack(pady=20)
        
        buttons = [
            ("➕ Ajouter une pièce", self.show_add_room),
            ("📋 Gérer les pièces", self.show_manage_rooms),
            ("🚪 Quitter", self.destroy)
        ]
        
        for text, cmd in buttons:
            ttk.Button(self, text=text, style='Bouton.TButton', command=cmd).pack(fill=X, pady=5)

    def show_add_room(self, room_data=None):
        add_window = Toplevel()
        add_window.title("Modifier une pièce" if room_data else "Nouvelle pièce")
        add_window.configure(padx=20, pady=20, bg='#F0F0F0')
        
        # Formulaire stylisé
        form_frame = ttk.Frame(add_window, padding=10)
        form_frame.pack(pady=10, fill=X)
        
        ttk.Label(form_frame, text="Nom de la pièce:").grid(row=0, column=0, sticky=W)
        name_entry = ttk.Entry(form_frame, style='Entry.TEntry', width=25)
        name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(form_frame, text="Type de pièce:").grid(row=1, column=0, sticky=W, pady=10)
        type_var = StringVar()
        type_combobox = ttk.Combobox(form_frame, textvariable=type_var, 
                                   values=["Cuisine", "Chambre", "Salon", "Salle de bain", "Balcon"])
        type_combobox.grid(row=1, column=1, padx=5)
        
        # Pré-remplissage si modification
        if room_data:
            name_entry.insert(0, room_data["name"])
            type_var.set(room_data["type"])
        
        # Boutons de contrôle
        btn_frame = ttk.Frame(add_window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="✔ Valider", style='Bouton.TButton',
                 command=lambda: self.save_room(name_entry.get(), type_var.get(), room_data, add_window))\
            .grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="✖ Annuler", style='Bouton.TButton',
                 command=add_window.destroy).grid(row=0, column=1, padx=5)

    def show_manage_rooms(self):
        manage_window = Toplevel()
        manage_window.title("Gestion des pièces")
        manage_window.configure(padx=20, pady=20, bg='#F0F0F0')
        
        # Liste moderne avec scrollbar
        list_frame = ttk.Frame(manage_window)
        list_frame.pack(fill=BOTH, expand=True)
        
        columns = ('type', 'temp', 'light')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading('#0', text='Pièce')
        self.tree.heading('type', text='Type')
        self.tree.heading('temp', text='Température')
        self.tree.heading('light', text='Éclairage')
        
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        vsb.pack(side=RIGHT, fill=Y)
        
        # Remplissage des données
        for room in salles:
            self.tree.insert('', 'end', text=room['name'], 
                      values=(room['type'], f"{room.get('temp', 20)}°C", '🟢 ON' if room.get('light') else '🔴 OFF'))
        
        # Contrôles avancés
        control_frame = ttk.Frame(manage_window)
        control_frame.pack(pady=10)
        
        controls = [
            ("⚙ Modifier", self.edit_room),
            ("🗑 Supprimer", self.delete_room),
            ("⚡ Réglages", self.show_advanced_settings),
            ("🔙 Fermer", manage_window.destroy)
        ]
        
        for i, (text, cmd) in enumerate(controls):
            ttk.Button(control_frame, text=text, style='Bouton.TButton', command=cmd)\
                .grid(row=0, column=i, padx=5)

    def edit_room(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner une pièce")
            return
        item = selected[0]
        room_name = self.tree.item(item, "text")
        room = next((r for r in salles if r['name'] == room_name), None)
        if room:
            self.show_add_room(room_data=room)

    def delete_room(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner une pièce")
            return
        item = selected[0]
        room_name = self.tree.item(item, "text")
        if messagebox.askyesno("Confirmation", f"Supprimer {room_name} ?"):
            global salles
            salles = [r for r in salles if r['name'] != room_name]
            self.tree.delete(item)
            messagebox.showinfo("Succès", f"Pièce {room_name} supprimée")

    def show_advanced_settings(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner une pièce")
            return
        item = selected[0]
        room_name = self.tree.item(item, "text")
        room = next((r for r in salles if r['name'] == room_name), None)
        
        if room:
            settings_window = Toplevel()
            settings_window.title(f"Réglages: {room_name}")
            settings_window.geometry("300x200")
            
            # Contrôle température
            ttk.Label(settings_window, text=f"Température actuelle: {room['temp']}°C").pack(pady=5)
            temp_scale = ttk.Scale(settings_window, from_=10, to=30, value=room['temp'])
            temp_scale.pack(fill=X, padx=20)
            
            # Contrôle éclairage
            light_var = BooleanVar(value=room['light'])
            ttk.Checkbutton(settings_window, text="Éclairage ON", variable=light_var,
                          command=lambda: room.update(light=light_var.get())).pack(pady=10)

    def save_room(self, name, type, room_data, add_window):
        if not name:
            messagebox.showerror("Erreur", "Le nom ne peut pas être vide")
            return
            
        # Mode édition
        if room_data:
            if name != room_data['name'] and any(p['name'] == name for p in salles):
                messagebox.showerror("Erreur", "Cette pièce existe déjà!")
                return
            room_data.update(name=name, type=type)
            messagebox.showinfo("Succès", f"Pièce {name} modifiée!")
        # Mode ajout
        else:
            if any(p['name'] == name for p in salles):
                messagebox.showerror("Erreur", "Cette pièce existe déjà!")
                return
            salles.append({'name': name, 'type': type, 'temp': 20, 'light': False})
            messagebox.showinfo("Succès", f"Pièce {name} ajoutée!")
        
        add_window.destroy()
        # Rafraîchir la fenêtre de gestion
        for child in self.winfo_children():
            if isinstance(child, Toplevel) and child.title().startswith("Gestion"):
                child.destroy()
                self.show_manage_rooms()

if __name__ == "__main__":
    app = DomotiqueApp()
    app.mainloop()