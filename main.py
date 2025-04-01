from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk  # Nécessite la bibliothèque Pillow

class DomotiqueApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartHome Manager")
        self.geometry("800x600")
        self.configure(padx=25, pady=25, bg='#F0F0F0')
        self.load_logo()
        # Données de l'application
        self.salles = []
        self.current_room = None
        
        # Configuration des styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._setup_styles()
        
        # Création des frames principaux
        self.main_frame = ttk.Frame(self)
        self.add_room_frame = ttk.Frame(self)
        self.manage_rooms_frame = ttk.Frame(self)
        self.settings_frame = ttk.Frame(self)
        
        # Initialisation
        self.show_main_menu()

    def load_logo(self):
     try:
        print("Chargement du logo...")  # Débogage
        self.logo_image = Image.open("logo_isi.png")
        self.logo_image = self.logo_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)  # Stocker dans une variable d'instance
        
        # Vérifier si le label existe déjà
        if hasattr(self, 'logo_label'):
            self.logo_label.config(image=self.logo_photo)
        else:
            self.logo_label = Label(self, image=self.logo_photo, bg='#F0F0F0')
            self.logo_label.image = self.logo_photo  # Garder une référence
            self.logo_label.place(x=10, y=10)

        print("Logo chargé avec succès !")
     except Exception as e:
        print(f"Erreur de chargement du logo : {e}")
        if hasattr(self, 'logo_label'):
            self.logo_label.config(text="Logo introuvable", image='')
        else:
            self.logo_label = Label(self, text="Logo introuvable", bg='#F0F0F0')
            self.logo_label.place(x=10, y=10)

    def _setup_styles(self):
        """Configure les styles visuels"""
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

    def show_frame(self, frame):
        """Affiche le frame spécifié et masque les autres"""
        for f in [self.main_frame, self.add_room_frame, 
                 self.manage_rooms_frame, self.settings_frame]:
            f.pack_forget()
        frame.pack(fill=BOTH, expand=True)

    def clear_frame(self, frame):
        """Efface tous les widgets d'un frame"""
        for widget in frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """Affiche le menu principal"""
        self.clear_frame(self.main_frame)
        self.show_frame(self.main_frame)
        
        ttk.Label(self.main_frame, text="SmartHome Manager", style='Titre.TLabel')\
            .pack(pady=20, padx=(60, 0))  # Ajout de padx à gauche
        
        buttons = [
            ("Ajouter une pièce", self.show_add_room),
            ("Gérer les pièces", self.show_manage_rooms),
            ("Quitter", self.destroy)
        ]
        
        for text, cmd in buttons:
            ttk.Button(self.main_frame, text=text, style='Bouton.TButton', 
                      command=cmd).pack(fill=X, pady=5)

    def show_add_room(self, room_data=None):
        """Affiche le formulaire d'ajout/modification de pièce"""
        self.clear_frame(self.add_room_frame)
        self.show_frame(self.add_room_frame)
        
        # Titre contextuel
        title = "Modifier une pièce" if room_data else "Nouvelle pièce"
        ttk.Label(self.add_room_frame, text=title, style='Titre.TLabel').pack(pady=10)
        
        # Formulaire
        form_frame = ttk.Frame(self.add_room_frame)
        form_frame.pack(pady=10)
        
        # Champ Nom
        ttk.Label(form_frame, text="Nom de la pièce:").grid(row=0, column=0, sticky=W, pady=5)
        self.name_entry = ttk.Entry(form_frame, style='Entry.TEntry', width=25)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        # Champ Type
        ttk.Label(form_frame, text="Type de pièce:").grid(row=1, column=0, sticky=W, pady=5)
        self.type_var = StringVar()
        type_combobox = ttk.Combobox(form_frame, textvariable=self.type_var, 
                                   values=["Cuisine", "Chambre", "Salon", "Salle de bain", "Balcon"])
        type_combobox.grid(row=1, column=1, padx=5)
        
        # Pré-remplissage si modification
        if room_data:
            self.current_room = room_data
            self.name_entry.insert(0, room_data["name"])
            self.type_var.set(room_data["type"])
        
        # Boutons
        btn_frame = ttk.Frame(self.add_room_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="✔ Valider", style='Bouton.TButton',
                  command=lambda: self.save_room(room_data is not None))\
            .pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="↩ Retour", style='Bouton.TButton',
                  command=self.show_main_menu).pack(side=LEFT, padx=5)

    def show_manage_rooms(self):
        """Affiche la gestion des pièces"""
        self.clear_frame(self.manage_rooms_frame)
        self.show_frame(self.manage_rooms_frame)
        
        ttk.Label(self.manage_rooms_frame, text="Gestion des pièces", style='Titre.TLabel').pack(pady=10)
        
        # Treeview avec scrollbar
        tree_frame = ttk.Frame(self.manage_rooms_frame)
        tree_frame.pack(fill=BOTH, expand=True, pady=10)
        
        columns = ('type', 'temp', 'light')
        self.rooms_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        # Configuration des colonnes
        self.rooms_tree.heading('#0', text='Pièce')
        self.rooms_tree.heading('type', text='Type')
        self.rooms_tree.heading('temp', text='Température')
        self.rooms_tree.heading('light', text='Éclairage')
        
        # Scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscrollcommand=vsb.set)
        
        self.rooms_tree.pack(side=LEFT, fill=BOTH, expand=True)
        vsb.pack(side=RIGHT, fill=Y)
        
        # Remplissage des données
        self.update_rooms_tree()
        
        # Boutons de contrôle
        control_frame = ttk.Frame(self.manage_rooms_frame)
        control_frame.pack(pady=10)
        
        controls = [
            ("Modifier", self.edit_room),
            ("Supprimer", self.delete_room),
            ("Réglages", self.show_room_settings),
            ("Retour", self.show_main_menu)
        ]
        
        for i, (text, cmd) in enumerate(controls):
            ttk.Button(control_frame, text=text, style='Bouton.TButton', 
                      command=cmd).grid(row=0, column=i, padx=5)

    def update_rooms_tree(self):
        """Met à jour la liste des pièces"""
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)
            
        for room in self.salles:
            self.rooms_tree.insert('', 'end', text=room['name'], 
                                 values=(room['type'], 
                                        f"{room.get('temp', 20)}°C", 
                                        '🟢 ON' if room.get('light') else '🔴 OFF'))

    def edit_room(self):
        """Ouvre le formulaire en mode édition"""
        selected = self.rooms_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner une pièce")
            return
            
        room_name = self.rooms_tree.item(selected[0], "text")
        room = next((r for r in self.salles if r['name'] == room_name), None)
        if room:
            self.show_add_room(room_data=room)

    def delete_room(self):
        """Supprime la pièce sélectionnée"""
        selected = self.rooms_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner une pièce")
            return
            
        room_name = self.rooms_tree.item(selected[0], "text")
        if messagebox.askyesno("Confirmation", f"Supprimer la pièce {room_name} ?"):
            self.salles = [r for r in self.salles if r['name'] != room_name]
            self.update_rooms_tree()
            messagebox.showinfo("Succès", f"Pièce {room_name} supprimée")

    def show_room_settings(self):
        """Affiche les réglages de la pièce sélectionnée"""
        selected = self.rooms_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner une pièce")
            return
            
        room_name = self.rooms_tree.item(selected[0], "text")
        self.current_room = next((r for r in self.salles if r['name'] == room_name), None)
        
        if self.current_room:
            self.clear_frame(self.settings_frame)
            self.show_frame(self.settings_frame)
            
            ttk.Label(self.settings_frame, 
                     text=f"Réglages: {room_name}", 
                     style='Titre.TLabel').pack(pady=10)
            
            # Contrôle température
            temp_frame = ttk.Frame(self.settings_frame)
            temp_frame.pack(pady=5, fill=X, padx=20)
            
            ttk.Label(temp_frame, text="Température:").pack(side=LEFT)
            self.temp_var = IntVar(value=self.current_room.get('temp', 20))
            ttk.Scale(temp_frame, from_=10, to=30, variable=self.temp_var,
                     command=lambda v: self.update_room_temp(int(float(v)))).pack(side=LEFT, padx=10)
            ttk.Label(temp_frame, textvariable=self.temp_var).pack(side=LEFT)
            ttk.Label(temp_frame, text="°C").pack(side=LEFT)
            
            # Contrôle éclairage
            light_frame = ttk.Frame(self.settings_frame)
            light_frame.pack(pady=10, fill=X, padx=20)
            
            ttk.Label(light_frame, text="Éclairage:").pack(side=LEFT)
            self.light_var = BooleanVar(value=self.current_room.get('light', False))
            ttk.Checkbutton(light_frame, text="Activé", variable=self.light_var,
                           command=self.update_room_light).pack(side=LEFT, padx=10)
            
            # Boutons
            btn_frame = ttk.Frame(self.settings_frame)
            btn_frame.pack(pady=20)
            
            ttk.Button(btn_frame, text="↩ Retour", style='Bouton.TButton',
                      command=self.show_manage_rooms).pack(side=LEFT, padx=5)

    def update_room_temp(self, temp):
        """Met à jour la température de la pièce courante"""
        if self.current_room:
            self.current_room['temp'] = temp
            self.temp_var.set(temp)

    def update_room_light(self):
        """Met à jour l'état de l'éclairage de la pièce courante"""
        if self.current_room:
            self.current_room['light'] = self.light_var.get()
            self.update_rooms_tree()

    def save_room(self, is_edit):
        """Sauvegarde une nouvelle pièce ou les modifications"""
        name = self.name_entry.get()
        type_ = self.type_var.get()
        
        if not name or not type_:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return
            
        # Mode édition
        if is_edit and self.current_room:
            if name != self.current_room['name'] and any(r['name'] == name for r in self.salles):
                messagebox.showerror("Erreur", "Une pièce avec ce nom existe déjà")
                return
                
            self.current_room.update(name=name, type=type_)
            messagebox.showinfo("Succès", f"Pièce {name} modifiée")
        # Mode ajout
        else:
            if any(r['name'] == name for r in self.salles):
                messagebox.showerror("Erreur", "Une pièce avec ce nom existe déjà")
                return
                
            self.salles.append({'name': name, 'type': type_, 'temp': 20, 'light': False})
            messagebox.showinfo("Succès", f"Pièce {name} ajoutée")
        
        self.show_manage_rooms()

if __name__ == "__main__":
    app = DomotiqueApp()
    app.mainloop()