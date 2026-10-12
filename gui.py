import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
import csv
import os
# from tkcalendar import DateEntry
from tkinter import ttk
import psycopg2
from psycopg2 import sql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from scipy.special import comb
 

# Configuration PostgreSQL via variables d'environnement.
# Définir DB_HOST, DB_PORT, DB_NAME, DB_USER et DB_PASSWORD avant le lancement.
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
dbname = os.getenv("DB_NAME", "gestion_patient")
user = os.getenv("DB_USER", "")
password = os.getenv("DB_PASSWORD", "")

def ouvrir_connexion_db():
    """Ouvre une connexion PostgreSQL avec les paramètres locaux."""
    if not user or not password:
        raise RuntimeError(
            "Configuration PostgreSQL manquante : définissez DB_USER et DB_PASSWORD."
        )
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

def connecter_db():
  try:
    # Établir la connexion
    connection = ouvrir_connexion_db()

    print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
    cursor = connection.cursor()

    # Exemple de requête : récupérer les tables de la base de données
    cursor.execute("SELECT * FROM patients;")
    
    tables = cursor.fetchall()
    print("Tables dans la base de données :", tables)
    
  except Exception as e:
    print("Erreur lors de la connexion à la base de données :", e)
  finally:
    # # Fermer le curseur et la connexion
    # if cursor:
    #     cursor.close()
    # if connection:
    #     connection.close()
    return [tables,cursor]
  
# def submit_form():
#     # Récupération des valeurs
#     name = entry_name.get()
#     email = entry_email.get()
#     message = text_message.get("1.0", tk.END).strip()
#     selected_ratio = ratio_var.get()  # Récupère le ratio sélectionné
#     selected_date = entry_date.get()  # Récupère la date saisie
    
#     if name and email and message and selected_ratio and selected_date:
#         messagebox.showinfo("Form Submitted", 
#                              f"Nom: {name}\nEmail: {email}\nRatio sélectionné: {selected_ratio}\nDate: {selected_date}\nMessage: {message}")
#     else:
#         messagebox.showwarning("Incomplete Form", "Veuillez remplir tous les champs.")

   
root = tk.Tk()
# root.configure(bg="#000000")
root.title("SmartControl")

def info1():
    new_window = tk.Toplevel(root)
    new_window.title("Info") 
    largeur = new_window.winfo_screenwidth()
    hauteur = new_window.winfo_screenheight()
    new_window.geometry(f"{largeur}x{hauteur}") 
    image = Image.open("./logo.png")
    image = image.resize((150,150))
    photo = ImageTk.PhotoImage(image)
    frame_image = tk.Frame(new_window)
    frame_image.pack()
    label_logo = tk.Label(frame_image,image=photo)
    label_logo.pack()

    marque = tk.Label(new_window, text="Smart control v1.0.0",font=("Arial",15,"bold italic"),fg="#003366")
    marque.pack(side=tk.TOP) 
    title_label2 = tk.Label(new_window, text="Powered By Jojo404 jojoemmanuel38@gmail.com",font=("Arial",10),fg="#003366")
    title_label2.pack() 
    bold_font = font.Font(family="Sergeo UI", size=23,weight="bold")
    label_tite = tk.Label(new_window,text="Contrat de Confidentialite",font=bold_font)
    label_tite.pack(pady=10)
    label_text = tk.Label(new_window,text="Veuillez Lire le contrat.txt present dans le dossier du logiciel")
    new_window.mainloop()

def open_file_dialogue():
    file_csv = filedialog.askopenfilename(title="Sectionnez un  fichier CSV",filetypes=(("Fichier CSV","*.csv"),("Tous les fichiers","*.*"))) #ouvre la boite de dialogue a la recherche du fichier csv
    if file_csv : # verifie si le fichier csv a ete selectionner 
        print(f"fichier selectionner : {file_csv}")
        chemin_var.set(file_csv)
    else :
        print("Aucun fichier selectionne")    
 
def revenir_fen_principal(fenetre_segondaire,fenetre_principal):
    fenetre_segondaire.destroy()
    fenetre_principal.deiconify() #demasque la fenetre principal NB: la fenetre principal est masquer avec le mot cle widraw lorsque tu accede a la fonction annalyse par ex

def quitter(fenetre_segondaire,fenetre_pricipal):
 if messagebox.askokcancel("Quitter","Voulez-vous vraiment quitter ?"):   
    fenetre_pricipal.destroy()
    fenetre_segondaire.destroy()

def open_auther_model():
   new_windows = tk.Toplevel(root)
   new_windows.title("Autre Modele")
# Fonction pour la loi de Benford
   def benford_distribution():
    return [np.log10(1 + 1/d) for d in range(1, 10)]

# Fonction pour la loi binomiale
   def binomial_distribution(n, p):
    x = np.arange(0, n + 1)
    binom_probs = [comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in x]
    return x, binom_probs

# Fonction pour la loi normale
   def normal_distribution(mu, sigma, num_points=100):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, num_points)
    y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    return x, y
   frame_graph = tk.Frame(new_windows)
# Frame pour la loi de Benford
   frame_benford = tk.Frame(new_windows)
   frame_benford.pack(side=tk.LEFT, padx=5)

# Tracer la loi de Benford
   benford_fig = plt.Figure(figsize=(5, 4), dpi=100)
   ax_benford = benford_fig.add_subplot(111)
   ax_benford.bar(range(1, 10), benford_distribution(), color='blue', alpha=0.7)
   ax_benford.set_title("Loi de Benford")
   ax_benford.set_xlabel("Chiffres")
   ax_benford.set_ylabel("Probabilité")

   canvas_benford = FigureCanvasTkAgg(benford_fig, master=frame_benford)
   canvas_benford.draw()
   canvas_benford.get_tk_widget().pack()

# Frame pour la loi binomiale
   frame_binomial = tk.Frame(frame_graph)
   frame_binomial.pack(side=tk.LEFT, padx=5)

# Tracer la loi binomiale
   n = 20  # nombre d'essais
   p = 0.5 # probabilité de succès
   x_binom, y_binom = binomial_distribution(n, p)

   binom_fig = plt.Figure(figsize=(5, 4), dpi=100)
   ax_binom = binom_fig.add_subplot(111)
   ax_binom.bar(x_binom, y_binom, color='green', alpha=0.7)
   ax_binom.set_title("Loi Binomiale (n=20, p=0.5)")
   ax_binom.set_xlabel("Nombre de succès")
   ax_binom.set_ylabel("Probabilité")

   canvas_binomial = FigureCanvasTkAgg(binom_fig, master=frame_binomial)
   canvas_binomial.draw()
   canvas_binomial.get_tk_widget().pack()

# Frame pour la loi normale
   frame_normal = tk.Frame(frame_graph)
   frame_normal.pack(side=tk.LEFT, padx=5)

# Tracer la loi normale
   mu = 0   # moyenne
   sigma = 1 # écart-type
   x_norm, y_norm = normal_distribution(mu, sigma)

   norm_fig = plt.Figure(figsize=(5, 4), dpi=100)
   ax_norm = norm_fig.add_subplot(111)
   ax_norm.plot(x_norm, y_norm, color='red')
   ax_norm.set_title("Loi Normale")
   ax_norm.set_xlabel("Valeur")
   ax_norm.set_ylabel("Densité")

   canvas_normal = FigureCanvasTkAgg(norm_fig, master=frame_normal)
   canvas_normal.draw()
   canvas_normal.get_tk_widget().pack()
   frame_graph.pack()






#fonction qui ouvre une nouvelle fenetre
def open_annalyseFichier():
    new_window = tk.Toplevel(root)
    new_window.title("Annalyse du fichier")
    root.withdraw() #Masque la fenetre principal
    largeur = new_window.winfo_screenwidth()
    hauteur = new_window.winfo_screenheight()
    new_window.geometry(f"{largeur}x{hauteur}") 
    # new_window.geometry("1000*400")  
    def open_file_dialogue2():
      file_csv = filedialog.askopenfilename(title="Sectionnez un  fichier CSV",filetypes=(("Fichier CSV","*.csv"),("Tous les fichiers","*.*"))) #ouvre la boite de dialogue a la recherche du fichier csv
      if file_csv : # verifie si le fichier csv a ete selectionner 
        print(f"fichier selectionner : {file_csv}")
        chemin_var.set(file_csv)
      else :
        print("Aucun fichier selectionne")    
    

 # creation de la frame barre de tache
    toolbar = tk.Frame(new_window)
    # ajout de boutton a la barre de tache
    btn_fichier = tk.Button(toolbar,text="Fichier",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=open_file_dialogue2)
    btn_fichier.pack(side=tk.LEFT,padx=2,pady=2) # tk.left permet d'aligner verticalement les 2 button
    btn_quitter = tk.Button(toolbar,text="Quitter",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=lambda:quitter(new_window,root))
    btn_quitter.pack(side=tk.LEFT)
    btn_info = tk.Button(toolbar,text="info",fg="#FFFFFF",background="#003366",borderwidth=0,width=10,cursor="hand2",command=info1)
    btn_info.pack(side=tk.LEFT,padx=2,pady=2) # tk.left permet d'aligner verticalement les 2 button
    btn_acceuil = tk.Button(toolbar,text="Acceuil",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=lambda:revenir_fen_principal(new_window,root)) #le mot cle lambda permet d'indiquer que nous utilisons une fonction avec argument
    btn_acceuil.pack(side=tk.LEFT)

    # afficher la toolbar
    toolbar.pack(side=tk.TOP,fill=tk.X)
    
    bold_font = font.Font(family="Helvetica", size=24,weight="bold")
    title_label = tk.Label(new_window, text="Annalyse du Jeux de Donnee", font=bold_font)
    title_label.pack(pady=30)  # Ajoute un espacement vertical
    frame_space = tk.Frame(new_window,height=10)
    frame_space.pack()
    title_label2 = tk.Label(new_window, text="Pour importer et annalyser un fichier cliquez sur le bouton Fichier",fg="#003366")
    title_label2.pack(pady=10) 
    chemin_var = tk.StringVar()
    frame_fichier = tk.Frame(new_window)
    label_name = tk.Label(frame_fichier, text="Le nom du fichier s'affiche ici" ,fg="#003366", font=("Helvetica" , 13))
    label_name.pack(side=tk.LEFT,padx=5)
    entry_name = tk.Entry(frame_fichier,textvariable=chemin_var,width=60,borderwidth=0)
    entry_name.pack(side=tk.LEFT ,padx=5)
    vx = tk.Label(frame_fichier,text="Entrez X",fg="#003366")
    vx.pack(side=(tk.LEFT))
    entry_x = tk.Entry(frame_fichier)
    entry_x.pack(side=tk.LEFT,padx=5)
    vy = tk.Label(frame_fichier,text="Entrez Y",fg="#003366")  
    vy.pack(side=(tk.LEFT))
    entry_y = tk.Entry(frame_fichier)
    entry_y.pack(side=tk.LEFT,padx=5)
    btn_annalyser = tk.Button(frame_fichier,text="Annalyser",fg="#FFFFFF",background="#003366",borderwidth=0,width=10,cursor="hand2",command=lambda:annalyse_complete(entry_name.get()))  
    btn_annalyser.pack(side=tk.LEFT)
    frame_fichier.pack(pady=10)
    
    
    def annalyse_complete(donnee):
      data_set = pd.read_csv(donnee)
      print(data_set)
      colonnes = data_set[[entry_x.get(),entry_y.get()]]
      data_dict = colonnes.to_dict(orient ='list') #pour obtenir un dictionnaire
      print(data_dict)
      frame_annalyse = tk.Frame(new_window)
      frame_regrssion_lineaire= tk.Frame(frame_annalyse)
    #regression lineaire
     # Création d'un DataFrame exemple
      new_dic = {
         'X': data_dict[entry_x.get()],
         'Y': data_dict[entry_y.get()]
      }
      print(new_dic)
      data = new_dic
    #   data = {
    # 'X': [1, 2, 3, 4, 5],
    # 'Y': [2, 3, 5, 7, 11]
    #  
      df = pd.DataFrame(data)

# Préparation des données
      X = df[['X']]  # Les caractéristiques (features)
      y = df['Y']    # La variable cible
      print(X)
# Création et entraînement du modèle de régression linéaire
      model = LinearRegression()
      model.fit(X, y)

# Prédiction
      predictions = model.predict(X)

    # Calcul du coefficient de corrélation et R²
      correlation_matrix = np.corrcoef(df['X'], df['Y'])
      correlation_coefficient = correlation_matrix[0, 1]
      r_squared = correlation_coefficient ** 2

# Coefficients du modèle
      slope = model.coef_[0]
      intercept = model.intercept_

# Équation de régression sous forme de chaîne
      equation_text = f"y = {slope:.2f}x + {intercept:.2f}"


# # Création de la fenêtre Tkinter
# root = tk.Tk()
# root.title("Régression Linéaire")
# root.geometry("200x100")  # Dimensions de la fenêtre

# Création du graphique
      fig, ax = plt.subplots(figsize=(4.6,4))  # Taille de la figure en pouces
      ax.scatter(df['X'], df['Y'], color='blue', label='Données réelles')
      ax.plot(df['X'], predictions, color='red', label='Régression linéaire')
      ax.set_title('Régression Linéaire')
      ax.set_xlabel('X')
      ax.set_ylabel('Y')
      ax.legend()
    
    
# Affichage du coefficient de corrélation et R² sur le graphique
      ax.text(0.1, 0.2, f"Corrélation: {correlation_coefficient:.2f}", transform=ax.transAxes)
      ax.text(0.1, 0.4, f"R²: {r_squared:.2f}", transform=ax.transAxes)
      ax.text(0.1, 0.6, equation_text, transform=ax.transAxes)

# Intégration du graphique dans la fenêtre Tkinter
      canvas = FigureCanvasTkAgg(fig, master=frame_regrssion_lineaire)
      canvas.draw()
      canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
      frame_regrssion_lineaire.pack(side=tk.LEFT)
 #regression logistique   
    # Génération de données d'exemple
    # np.random.seed(0)
    # X = df[data["X"]] #np.random.rand(100, 1) * 10  # 100 échantillons entre 0 et 10
    # print(X[0])
    # y = (X > 5).astype(int).ravel()    # Classe 1 si X > 5, sinon classe 0
      df = pd.DataFrame(data)

# Étape 2 : Extraire X et Y 
      X = df[['X']]  # Note que X doit être un DataFrame, donc on utilise des doubles crochets
      y = df['Y']

# Étape 3 : Préparation des données - vérifie si Y est binaire
# Pour la régression logistique, Y doit être binaire (0 ou 1)
# Dans ce cas, nous devons transformer Y en valeurs binaires.
# Par exemple, nous pouvons définir une condition pour transformer Y en binaire.

# Supposons que nous voulons prédire si Y est supérieur à une certaine valeur
      threshold = 5
      y_binary = (y > threshold).astype(int)  # Transforme Y en binaire
      y = y_binary 
# Création du modèle de régression logistique
      model = LogisticRegression()
      model.fit(X, y)

# Préparation des données pour la prédiction
      x_values = np.linspace(0, 10, 300).reshape(-1, 1)
      y_probabilities = model.predict_proba(x_values)[:, 1]

    # Création d'une Frame pour le graphique
      frame = tk.Frame(frame_annalyse)
      frame.pack(side=tk.LEFT,padx=5)

# Création du graphique dans Matplotlib
      fig, ax = plt.subplots(figsize=(4.6, 4))
      ax.scatter(X, y, color='blue', label='Données réelles')
      ax.plot(x_values, y_probabilities, color='orange', label='Régression logistique')
      ax.set_title('Régression Logistique')
      ax.set_xlabel('X')
      ax.set_ylabel('Probabilité')
      ax.legend()

# Intégration du graphique dans la Frame Tkinter
      canvas = FigureCanvasTkAgg(fig, master=frame)
      canvas.draw()
      canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
      
    # Prédictions sur les données d'entraînement
      y_pred = model.predict(X)

# Calcul de la matrice de confusion
      cm = confusion_matrix(y, y_pred)  
    
  # Création d'une Frame pour la matrice de confusion
      frame_cm = tk.Frame(frame_annalyse)
      frame_cm.pack(side=tk.LEFT,padx=5)

# Création du graphique pour la matrice de confusion avec Seaborn
      fig2, ax2 = plt.subplots(figsize=(4.6, 4))
      sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2)
      ax2.set_title('Matrice de Confusion')
      ax2.set_xlabel('Prédictions')
      ax2.set_ylabel('Vérités Réelles')

# Intégration du graphique dans la Frame Tkinter
      canvas2 = FigureCanvasTkAgg(fig2, master=frame_cm)
      canvas2.draw()
      canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
      frame_annalyse.pack(pady=20)
      btn_auther_model = tk.Button(new_window,text="Autre model d'annalyse (Prochaine mise a jour)",fg="#FFFFFF",background="#003366",borderwidth=0,width=60,cursor="hand2",command=open_auther_model) #le mot cle lambda permet d'indiquer que nous utilisons une fonction avec argument
      btn_auther_model.pack(pady=20)
    

def open_gestion_des_patients():


    # def open_file_dialogue():
    #   file_csv = filedialog.askopenfilename(title="Sectionnez un  fichier CSV",filetypes=(("Fichier CSV","*.csv"),("Tous les fichiers","*.*"))) #ouvre la boite de dialogue a la recherche du fichier csv
    #   if file_csv : # verifie si le fichier csv a ete selectionner 
    #    print(f"fichier selectionner : {file_csv}")
    #    chemin_var.set(file_csv)
    #    afficher_contenu_csv(file_csv)
    #   else :
    #     print("Aucun fichier selectionne")    

#     def afficher_contenu_csv(fichier):
#       texte.delete(1.0,tk.END)
#       with open(fichier,'r') as f:
#         reader = csv.reader(f)
#         entetes = next(reader) #lire aussi les entetes
#         tableau =[] 
#         #boucle pour lire chaque ligne
#         for ligne in reader:
#             object={}
#    #boucle pour associer chaque valeur a son entete
#             for i , entetes in enumerate(entetes):
#                object[entetes]=ligne[i]
#                tableau.append(object) #ajouter l'objet au tableau   
#                texte.insert(tk.END,','.join(ligne)+'\n')
#       for objet in tableau :
#          print(objet)
           

    new_window = tk.Toplevel(root)
    new_window.title("Gestion des patients")
    root.withdraw()
    largeur = new_window.winfo_screenwidth()
    hauteur = new_window.winfo_screenheight()
    new_window.geometry(f"{largeur}x{hauteur}") 
        
    def btn_search_patient():
      if entry_name.get():
        result = search_patient(entry_name.get())
        fill_treeview(tree,result)

    def btn_search_consultation():
      if consultation_id.get():
        result = search_consult(consultation_id.get())
        fill_treeview(tree1,result)   

    def insert_patient():
         connection = ouvrir_connexion_db()
         print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
         cursor = connection.cursor()

    # Exemple de requête : récupérer les tables de la base de données
         cursor.execute("INSERT INTO patients (nom_client,age,sexe,adresse,numero_telephone) VALUES (%s,%s,%s,%s,%s)",(entry_name_comp.get(),entry_age.get(),ratio_var.get(),entry_adresse.get(),entry_tel.get()))
         connection.commit()
         fill_treeview(tree,connecter_db()) 

    def update_patient():
         connection = ouvrir_connexion_db()
         print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
         cursor = connection.cursor()
         if entry_name_comp.get() :
           cursor.execute("UPDATE patients SET nom_client = %s WHERE id_client = %s ;",(entry_name_comp.get(),id_patient.get()))
           connection.commit()
           fill_treeview(tree,connecter_db()) 
         if entry_age.get() :
           cursor.execute("UPDATE patients SET age = %s WHERE id_client = %s ;",(entry_age.get(),id_patient.get()))
           connection.commit()
           fill_treeview(tree,connecter_db()) 
         if ratio_var.get() :
           cursor.execute("UPDATE patients SET sexe = %s WHERE id_client = %s ;",(ratio_var.get(),id_patient.get()))
           connection.commit()
           fill_treeview(tree,connecter_db())   
         if entry_adresse.get() :
           cursor.execute("UPDATE patients SET adresse = %s WHERE id_client = %s ;",(entry_adresse.get(),id_patient.get()))
           connection.commit()
           fill_treeview(tree,connecter_db())
         if entry_tel.get() :
           cursor.execute("UPDATE patients SET numero_telephone = %s WHERE id_client = %s ;",(entry_tel.get(),id_patient.get()))
           connection.commit()
           fill_treeview(tree,connecter_db())      

    def update_consultation():
          connection = ouvrir_connexion_db()
          print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
          cursor = connection.cursor()     
          if entry_consult_doctor.get():
            cursor.execute("UPDATE consultation SET nom_docteur = %s WHERE id_consultation = %s ;",(entry_consult_doctor.get(),id_consultation.get()))
            connection.commit()
            fill_treeview(tree1,select_consult())  
          if consult_body.get("1.0", tk.END).strip():
            cursor.execute("UPDATE consultation SET contenue = %s WHERE id_consultation = %s ;",(consult_body.get("1.0", tk.END).strip(),id_consultation.get()))
            connection.commit()
            fill_treeview(tree1,select_consult())   

    def delete_patient():
         connection = ouvrir_connexion_db()
         print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
         cursor = connection.cursor()
        
    # Exemple de requête : récupérer les tables de la base de données
         cursor.execute("DELETE  FROM patients  WHERE id_client  = %s",(id_patient.get(),))
         connection.commit() #pour accepter les modification
         fill_treeview(tree,connecter_db())

    def delete_consultation():
         connection = ouvrir_connexion_db()
         print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
         cursor = connection.cursor()
        
    # Exemple de requête : récupérer les tables de la base de données
         cursor.execute("DELETE  FROM consultation  WHERE id_consultation  = %s",(id_consultation.get(),))
         connection.commit() #pour accepter les modification
         fill_treeview(tree1,select_consult())  

    def insert_consultation():
         connection = ouvrir_connexion_db()
         print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
         cursor = connection.cursor()
            
     
         date = datetime.datetime.now()
         aujourdhuit = date.strftime("%d/%m/%Y %H:%M:%S")
 
         cursor.execute("INSERT INTO consultation (mat_patient,date_consultation,nom_docteur,contenue) VALUES (%s,%s,%s,%s)",(entry_consult_id.get(),aujourdhuit,entry_consult_doctor.get(),consult_body.get("1.0", tk.END).strip()))
         connection.commit()
         fill_treeview(tree1,select_consult()) 

    def select_consult():
         connection = ouvrir_connexion_db()
         print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
         cursor = connection.cursor()
            
     
         date = datetime.datetime.now()
         aujourdhuit = date.strftime("%d/%m/%Y %H:%M:%S")
         cursor.execute("SELECT * FROM consultation")
         done = cursor.fetchall()
         connection.commit()   
         return [done]

 # creation de la frame barre de tache
    toolbar = tk.Frame(new_window)
    # ajout de boutton a la barre de tache
    btn_fichier = tk.Button(toolbar,text="Fichier",fg="#FFFFFF",background="#003366",borderwidth=0,width=10,cursor="hand2" )
    btn_fichier.pack(side=tk.LEFT,padx=2,pady=2) # tk.left permet d'aligner verticalement les 2 button
    btn_quitter = tk.Button(toolbar,text="Quitter",fg="#FFFFFF",background="#003366",borderwidth=0,width=10,cursor="hand2",comman=lambda:quitter(new_window,root))
    btn_quitter.pack(side=tk.LEFT)
    btn_info = tk.Button(toolbar,text="info",fg="#FFFFFF",background="#003366",borderwidth=0,width=10,cursor="hand2",command=info1)
    btn_info.pack(side=tk.LEFT,padx=2,pady=2) # tk.left permet d'aligner verticalement les 2 button
    btn_acceuil = tk.Button(toolbar,text="Acceuil",fg="#FFFFFF",background="#003366",borderwidth=0,width=10,cursor="hand2",command=lambda:revenir_fen_principal(new_window,root)) #le mot cle lambda permet d'indiquer que nous utilisons une fonction avec argument
    btn_acceuil.pack(side=tk.LEFT)
    # afficher la toolbar
    toolbar.pack(side=tk.TOP,fill=tk.X)
    
    bold_font = font.Font(family="Helvetica", size=24,weight="bold")
    title_label = tk.Label(new_window, text="Gestion des Patients", font=bold_font)
    title_label.pack(pady=1)  # Ajoute un espacement vertical
    frame_space = tk.Frame(new_window,height=10)
    frame_space.pack()
  
    title_label2 = tk.Label(new_window, text="Pour rechercher un patient saisissez son nom ici ",fg="#003366")
    title_label2.pack( pady=5) 

    frame_fichier = tk.Frame(new_window)
    label_name = tk.Label(frame_fichier, text="Nom du Patient",fg="#003366" , font=("Helvetica" , 13))
    label_name.pack(side=tk.LEFT,padx=5)
    entry_name = tk.Entry(frame_fichier,width=60,borderwidth=0)
    entry_name.pack(side=tk.LEFT ,padx=5)
    btn_rechercher = tk.Button(frame_fichier,text="Rechercher",fg="#FFFFFF",background="#003366",borderwidth=0,width=10,cursor="hand2",command=btn_search_patient)  
    btn_rechercher.pack(side=tk.LEFT)
    btn_Docteur = tk.Button(frame_fichier,text="Liste des Docteur de L'hopital",fg="#FFFFFF",background="#003366",borderwidth=0,width=30,cursor="hand2")  
    btn_Docteur.pack(side=tk.LEFT,padx=5)
    frame_fichier.pack(pady=10)

        # new_window.geometry("700*400")

    # Fonction pour remplir le Treeview avec des lignes colorées
    def fill_treeview(tree,data):
    # Suppression des anciennes données
      for row in tree.get_children():
        tree.delete(row)
    
    # Insertion des nouvelles données avec coloration alternée
      for index, row in enumerate(data[0]):
        tree.insert("", "end", values=row)
        if index % 2 == 0:
            tree.item(tree.get_children()[-1], tags=('evenrow',))
        else:
            tree.item(tree.get_children()[-1], tags=('oddrow',))

    frame_gadget = tk.Frame(new_window)
    frame_tableau = ttk.Frame(frame_gadget)  #frame pour contenir le tableau
    frame_tableau.pack(fill=tk.BOTH,expand=True,side=tk.LEFT,padx=50) #Both pour occuper toute l'espace de la frame disponible expend poor un redimentionnement automatique lors de l'agrandissement de la fenetre      
 
    # Création du Treeview
    tree = ttk.Treeview(frame_tableau, columns=("col1", "col2", "col3","col4","col5","col6"), show='headings')
    tree.heading("col1", text="Matricule Patient")
    tree.heading("col2", text="Noms et Prenom")
    tree.heading("col3", text="Age")
    tree.heading("col4", text="Sexe")
    tree.heading("col5", text="Adresse")
    tree.heading("col6", text="Tel")
    tree.column("col1",width=120 , stretch=tk.YES) # largeur flexible ? oui
    tree.column("col2",width=220 , stretch=tk.YES)
    tree.column("col3",width=50 , stretch=tk.YES)
    tree.column("col4",width=50 , stretch=tk.YES)
    tree.column("col5",width=180 , stretch=tk.YES)
    tree.column("col6",width=80 , stretch=tk.YES)
    
 
# Définition des styles pour les lignes colorées
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
    style.configure("evenrow", background="#f0f0f0")  # Couleur pour les lignes paires
    style.configure("oddrow", background="#ADD8E6")   # Couleur pour les lignes impaires

    tree.tag_configure('evenrow', background="#f0f0f0")
    tree.tag_configure('oddrow', background="#ADD8E6")
    # Ajouter une scrollbar verticale
    scrollbar = ttk.Scrollbar(frame_tableau, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
# Pack le Treeview et la scrollbar
    tree.pack(side=tk.LEFT,fill=tk.BOTH)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

# Ajout du Treeview à la fenêtre
    tree.pack()    
    # Remplissage du Treeview avec les données de la base de données
    
    
    fill_treeview(tree,connecter_db()) 
    def search_patient(nom):
          connection = ouvrir_connexion_db()
          print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
          cursor = connection.cursor()

    # Exemple de requête : récupérer les tables de la base de données
          cursor.execute("SELECT * FROM patients WHERE nom_client iLIKE  %s ;",(nom+'%',)) #ilike est censible a la casse
    
          tables = cursor.fetchall()
          print("Tables dans la base de données :", tables)
          return [tables,cursor]
    
    def search_consult(nom):
          connection = ouvrir_connexion_db()
          print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
          cursor = connection.cursor()

    # Exemple de requête : récupérer les tables de la base de données
          cursor.execute("SELECT * FROM consultation WHERE mat_patient = %s ;",(nom,))
    
          tables = cursor.fetchall()
          print("Tables dans la base de données :", tables)
          return [tables,cursor]

    frame_koko = tk.Frame(frame_gadget)     
# Champs du formulaire
    label_name = tk.Label(frame_koko, text="Nom complet :" ,fg="#003366", font=("Helvetica" , 13))
    label_name.pack()
    entry_name_comp = tk.Entry(frame_koko,width=50,borderwidth=0)
    entry_name_comp.pack(pady=10)

    label_age = tk.Label(frame_koko, text="Age:",fg="#003366",font=("Helvetica" , 13))
    label_age.pack()
    entry_age = tk.Entry(frame_koko,width=50,borderwidth=0)
    entry_age.pack(pady=10)

# Variable pour les boutons radio
    ratio_var = tk.StringVar(value="1:1")  # Valeur par défaut

# Boutons radio pour les ratios
    label_ratio = tk.Label(frame_koko, text="Sélectionnez votre sexe :",fg="#003366", font=("Helvetica" , 13))
    label_ratio.pack()

    radio1 = tk.Radiobutton(frame_koko, text="M",fg="#003366", variable=ratio_var, value="M")
    radio1.pack()

    radio2 = tk.Radiobutton(frame_koko, text="F",fg="#003366", variable=ratio_var, value="F")
    radio2.pack()

    label_adresse = tk.Label(frame_koko, text="Adresse :" ,fg="#003366", font=("Helvetica" , 12))
    label_adresse.pack()
    entry_adresse = tk.Entry(frame_koko,width=50,borderwidth=0)
    entry_adresse.pack(pady=10)
    
    label_numero = tk.Label(frame_koko, text="Tel :" ,fg="#003366", font=("Helvetica" , 12))
    label_numero.pack()
    entry_tel = tk.Entry(frame_koko,width=50,borderwidth=0)
    entry_tel.pack(pady=10)

# Champ de saisie pour la date
 
    # label_date = tk.Label(root, text="Sélectionnez une date:",font=("Helvetica" , 15))
    # label_date.pack()
    # entry_date = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
    # entry_date.pack()

    # label_message = tk.Label(root, text="Message:",font=("Helvetica" , 15))
    # label_message.pack()
    # text_message = tk.Text(root, height=5, width=30)
    # text_message.pack()
    frame_bouton = tk.Frame(frame_koko)
    button_submit = tk.Button(frame_bouton, text="Ajouter",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=insert_patient)
    button_submit.pack(pady=10,side=tk.LEFT,padx=5)
    button_suprimer = tk.Button(frame_bouton, text="Supprimer",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=delete_patient)
    button_suprimer.pack(pady=10,side=tk.LEFT,padx=5)
    button_update = tk.Button(frame_bouton, text="Modifier",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=update_patient)
    button_update.pack(pady=10,side=tk.LEFT,padx=5)
    frame_bouton.pack(pady=10,side=tk.LEFT,padx=5)
    id_patient = tk.Entry(frame_bouton,borderwidth=0) 
    id_patient.pack(pady=10,side=tk.LEFT,padx=5)

    frame_koko.pack(side=tk.LEFT)
    frame_gadget.pack()
    
    text_consultation = tk.Label(new_window, text="Pour Voir les consultaions entrez le matricule du Patient NB : Vous ne pouvez pas modifier le amatricule du Patient",fg="#003366")
    text_consultation.pack(pady=10) 

    frame_btn_consult = tk.Frame(new_window)
    consultation_id = tk.Entry(frame_btn_consult,width=60,borderwidth=0)
    consultation_id.pack(pady=5,side=tk.LEFT)
    button_search_consult = tk.Button(frame_btn_consult, text="Rechercher",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=btn_search_consultation)
    button_search_consult.pack(padx=3,side=tk.LEFT)
    button_ajout_consult = tk.Button(frame_btn_consult, text="Modifier",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=update_consultation)
    button_ajout_consult.pack(padx=3,side=tk.LEFT)
    button_modif_consult = tk.Button(frame_btn_consult, text="Ajouter",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=insert_consultation)
    button_modif_consult.pack(padx=3,side=tk.LEFT)
    button_supp_consult = tk.Button(frame_btn_consult, text="Supprimer",fg="#FFFFFF",background="#003366",borderwidth=0 ,width=10,cursor="hand2",command=delete_consultation)
    button_supp_consult.pack(padx=3,side=tk.LEFT)
    id_consultation = tk.Entry(frame_btn_consult,borderwidth=0) 
    id_consultation.pack(pady=10,side=tk.LEFT,padx=5)
    frame_btn_consult.pack()
    
    frame_add_consult = tk.Frame(new_window)
    frame_text = tk.Frame(frame_add_consult)
#     consultation=tk.Text(frame_text,height=12,width=130)
#     consultation.pack()
    frame_tableau = ttk.Frame(frame_text)  #frame pour contenir le tableau
    frame_tableau.pack(fill=tk.BOTH,expand=True) #Both pour occuper toute l'espace de la frame disponible expend poor un redimentionnement automatique lors de l'agrandissement de la fenetre      
 
    # Création du Treeview
    tree1 = ttk.Treeview(frame_tableau, columns=("col1", "col2", "col3","col4","col5"), show='headings')
    tree1.heading("col1", text="id Consultation")
    tree1.heading("col2", text="Matricule Patient")
    tree1.heading("col3", text="Date Consultaion")
    tree1.heading("col4", text="Nom du Docteur")
    tree1.heading("col5", text="Contenue")
    tree1.column("col1",width=100 , stretch=tk.YES) # largeur flexible ? oui
    tree1.column("col2",width=150 , stretch=tk.YES)
    tree1.column("col3",width=150 , stretch=tk.YES)
    tree1.column("col4",width=150 , stretch=tk.YES)
    tree1.column("col5",width=220 , stretch=tk.YES)
    
# Définition des styles pour les lignes colorées
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
    style.configure("evenrow", background="#f0f0f0")  # Couleur pour les lignes paires
    style.configure("oddrow", background="#ADD8E6")   # Couleur pour les lignes impaires

    tree1.tag_configure('evenrow', background="#f0f0f0")
    tree1.tag_configure('oddrow', background="#ADD8E6")
    # Ajouter une scrollbar verticale
    scrollbar = ttk.Scrollbar(frame_tableau, orient="vertical", command=tree.yview)
    tree1.configure(yscrollcommand=scrollbar.set)
# Pack le Treeview et la scrollbar
    tree1.pack(side=tk.LEFT,fill=tk.BOTH)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

# Ajout du Treeview à la fenêtre
    tree1.pack()    
    # Remplissage du Treeview avec les données de la base de données
    frame_text.pack(side=tk.LEFT, padx=5)
    fill_treeview(tree1,select_consult()) 
    frame_consult_form = tk.Frame(frame_add_consult)
    label_consult_id = tk.Label(frame_consult_form, text="Matricule Patient :",fg="#003366" , font=("Helvetica" , 10))
    label_consult_id.pack()
    entry_consult_id = tk.Entry(frame_consult_form,width=50)
    entry_consult_id.pack()
    label_consult_doctor = tk.Label(frame_consult_form, text="Nom Docteur :",fg="#003366" , font=("Helvetica" , 10))
    label_consult_doctor.pack()
    entry_consult_doctor = tk.Entry(frame_consult_form,width=50)
    entry_consult_doctor.pack()
    label_body_consult = tk.Label(frame_consult_form,text="Contenue consultation",fg="#003366", font=("Helvetica" , 10))
    label_body_consult.pack()
    consult_body = tk.Text(frame_consult_form,height=5)
    consult_body.pack()
    frame_consult_form.pack(side=tk.LEFT,padx=5)
    frame_add_consult.pack()   

largeur = root.winfo_screenwidth()
hauteur = root.winfo_screenheight()
root.geometry(f"{largeur}x{hauteur}")  
 # creation de la frame barre de tache
toolbar = tk.Frame(root)

# ajout de boutton a la barre de tache
btn_fichier = tk.Button(toolbar,text="Fichier",fg="#FFFFFF",background="#003366",borderwidth=0,width=10,cursor="hand2",command=open_file_dialogue)
btn_fichier.pack(side=tk.LEFT,padx=1,pady=2) # tk.left permet d'aligner verticalement les 2 button
btn_info = tk.Button(toolbar,text="info",fg="#FFFFFF",borderwidth=0,background="#003366",width=10,cursor="hand2",command=info1)
btn_info.pack(side=tk.LEFT,padx=1)
btn_quitter = tk.Button(toolbar,text="Quitter",fg="#FFFFFF",borderwidth=0,background="#003366",width=10,cursor="hand2",command=root.destroy)
btn_quitter.pack(side=tk.LEFT,padx=1)
# cree une var pour le champ de texte qui va acceuillir le path du fichier csv
chemin_var = tk.StringVar()

# afficher la toolbar
toolbar.pack(side=tk.TOP,fill=tk.X)

image = Image.open("./logo.png")
image = image.resize((200,200))
photo = ImageTk.PhotoImage(image)
frame_image = tk.Frame(root)
frame_image.pack()
label_logo = tk.Label(frame_image,image=photo)
label_logo.pack()

marque = tk.Label(root, text="Smart control v1.0.0",font=("Arial",20,"bold italic"),fg="#003366")
marque.pack(side=tk.TOP, pady=2) 
title_label2 = tk.Label(root, text="Powered By Jojo404 jojoemmanuel38@gmail.com",font=("Arial",10),fg="#003366")
title_label2.pack() 

frame_space = tk.Frame(root,height=40)
frame_space.pack()
bold_font = font.Font(family="Sergeo UI", size=24,weight="bold")
title_label = tk.Label(root, text="Logiciel de gestion et de prise de decision", font=bold_font)
title_label.pack(pady=10)  # Ajoute un espacement vertical
frame_space = tk.Frame(root,height=40)
frame_space.pack()
title_label2 = tk.Label(root, text="Pour importer et annalyser un fichier cliquez sur le bouton Fichier",fg="#003366")
title_label2.pack(pady=10) 

frame_fichier = tk.Frame(root)
label_name = tk.Label(frame_fichier, text="Le nom du fichier s'affiche ici" ,fg="#003366", font=("Helvetica" , 11))
label_name.pack(side=tk.LEFT,padx=5)
entry_name = tk.Entry(frame_fichier,textvariable=chemin_var,width=60,borderwidth=0)
entry_name.pack(side=tk.LEFT ,padx=5)
frame_fichier.pack(pady=10)

frame_space = tk.Frame(root,height=40)
frame_space.pack()
frame_boutonmenuu = tk.Frame(root)
btnAnnalyse = tk.Button(frame_boutonmenuu,text="ANNALYSER \n UN \n FICHIER",font=("Helvetica" , 15),borderwidth=0,width=35,height=15,background="#ADD8E6",cursor="hand2",command=open_annalyseFichier)
btnAnnalyse.pack(side=tk.LEFT)
btnAnnaGestionPatient = tk.Button(frame_boutonmenuu,text="GESTION \n DES \n PATIENTS", font=("Helvetica" , 15),borderwidth=0,width=35,height=15,background="#ADD8E6",cursor="hand2",command=open_gestion_des_patients)
btnAnnaGestionPatient.pack(side=tk.LEFT,padx=10)
frame_boutonmenuu.pack(pady=20)

root.mainloop()