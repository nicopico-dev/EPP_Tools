# TODO Ajouter un systeme d'onglet navigable avec les fleches Gauche et Droite.
#      Objectif : Afficher les mots du fichier et les mots du langage séparément. Rester le plus générique possible (Ajouter un parameter à addWords ?)
# FIXME : Il faut une wordslist par onglet !

import tkinter as tk
import tkinter.ttk as ttk

import epp_utils as epp
from epp_utils import Struct

class TkWordsList(tk.Frame):
    __separator = '------------------------------'

    def __init__(self, master=None, title='WordsList', width=200, height=250):
        self.choix = None
        self.wholeSearch = None
        
        # Structure contenant les objets Mots (pour séparer affichage/données)
        # Mots doit avoir un attribut 'string' et un attribut 'infos'
        self.wordsList = []
        
        self.tabIndexes = {}
        self.currTab = 0
        self.arrListBox = []
        
        tk.Frame.__init__(self, master)
        self.pack(fill="both", expand="true")
        self.create_widgets()
        self.set_title(title)
        self.set_geometry(width, height)        
    
    def __getattr__(self, name):
        if name == "currentListBox":
            return self.get_current_listbox()
        else:
            raise AttributeError("Attribute {0} does not exist".format(name))
    
    def create_widgets(self):
        # Onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", side="top", expand="true")
        
        # Creation de l'onglet par defaut
        self.create_tab("Default")
        
        # Focus sur la liste courante
        self.currentListBox.focus_set()
        
        # Bouton Ok
        self.buttonOk = tk.Button(self, text="Ok", command=self.handle_word, default=tk.ACTIVE)
        self.buttonOk.pack(fill="x", side="left", expand="true")
        
        # Bouton Cancel
        self.buttonExit = tk.Button(self, text="Cancel", command=self.quit)
        self.buttonExit.pack(fill="x", side="right", expand="true")
        
        # Evenements clavier
        self.master.bind("<KeyPress>", self.handle_key_press)
        self.master.bind("<Escape>", self.quit)
        
        # Autres evenements
        self.notebook.bind("<<NotebookTabChanged>>", self.handle_tabChanged)
    
    def create_tab(self, tab_name):
        if not tab_name in self.tabIndexes:
            listBox = tk.Listbox(self, selectmode=tk.BROWSE, activestyle="none")
            listBox.configure(font=("Courier New", "8"))
            listBox.bind("<Double-Button-1>", self.handle_word)
            
            self.notebook.add(listBox, text=tab_name)
            
            tabID = len(self.tabIndexes)
            self.tabIndexes[tab_name] = tabID
            epp.log("Tabs : {0}".format(self.tabIndexes))
            
            self.arrListBox.append(listBox)
        else:
            tabID = self.tabIndexes[tab_name]
            
        return tabID
        
    def get_current_listbox(self):
        return self.get_tab_listbox(self.currTab)
        
    def get_tab_listbox(self, tabID):
        return self.arrListBox[tabID]
    
    def set_geometry(self, wapp, happ):
        # Centre l'application sur l'ecran
        xapp = (self.winfo_screenwidth() - wapp) / 2
        yapp = (self.winfo_screenheight() - happ) / 2
        
        self.master.geometry("%dx%d+%d+%d" % (wapp, happ, xapp, yapp))
    
    def set_title(self, title):
        self.master.title(title)
        
    def set_always_on_top(self, doIt):
        if doIt:
            self.master.wm_attributes('-topmost', 1)
        else:
            self.master.wm_attributes('-topmost', 0)
    
    def add_words(self, wordObjs, addSeparator=False, tabName='Default'):
        # Cree l'onglet si il n'existe pas, ou retourne l'onglet existant de meme nom
        tabID = self.create_tab(tabName)
        epp.log("Adding words to tab {0} (ID {1})".format(tabName, tabID))
        
        listBox = self.get_tab_listbox(tabID)
        
        # Ajoute une sequence de mots à la liste
        if addSeparator and listBox.size() > 0 and len(wordObjs) > 0:
            listBox.insert(tk.END, self.__separator)
            self.wordsList.append(None)
        for wordObj in wordObjs:
            if isinstance(wordObj, str):
                wordObj = Struct(string=wordObj, infos="")
            
            listBox.insert(tk.END, "%-30s|%s" % (wordObj.string, wordObj.infos))
            
            # Mot du langage en couleur
            if hasattr(wordObj, "color"):
                listBox.itemconfig(len(self.wordsList), fg=wordObj.color)
            
            self.wordsList.append(wordObj)
            
        listBox.select_set(0)
    
    def select_word(self, search):
        self.currentListBox.selection_clear(0, tk.END)
        
        if self.wholeSearch == None:
            self.wholeSearch = search
        else:
            self.wholeSearch += search
        
        for (index, wordObj) in [ (index, self.wordsList[index]) for index in range(len(self.wordsList)) ]:
            if wordObj == None:
                # Separateur -> pas de wordObj. On recupere l'affichage de la liste
                str_check = self.currentListBox.get(index)
            else:
                str_check = wordObj.string
            
            if str_check.startswith(search):
                self.currentListBox.selection_set(index)
                self.currentListBox.activate(index)
                self.currentListBox.see(index)
                return wordObj
        
        # Si non trouve, on retourne le 1er element
        self.currentListBox.selection_set(0)
        self.currentListBox.activate(0)
        self.currentListBox.see(0)
        return self.wordsList[0]
    
    def get_selection(self):
        cur_index = int(self.currentListBox.curselection()[0])
        return self.wordsList[cur_index] 
    
    def handle_key_press(self, event):
        epp.log(event.keysym)
        cur_element = self.get_selection()
        if cur_element != None:
            if event.keysym in ("Return", "<Return>", "Enter", "<Enter>"):
                # Entrée -> même action que le bouton Ok
                self.handle_word(event)
            elif event.char != '':
                # Autre touche -> choix + caractère correspondant à la touche
                self.choix = cur_element + event.char
                self.quit()
    
    def handle_tabChanged(self, event):
        self.currTab = event.widget.index("current")
        epp.log("Selected tab : {0}".format(self.currTab))
        
    
    def handle_word(self, event=None):
        cur_element = self.get_selection()
        # On empêche de sélectionner le séparateur comme mot !
        if cur_element != None:
            self.choix = cur_element.string
            self.quit()
    
    def quit(self, event=None):
        self.master.quit()
        
def main(argv):
    app = TkWordsList()
    app.add_words(('bonjour', 'monsieur', 'le', 'chien'))
    app.add_words(('bonsoir', 'madame', 'la', 'vache'), tabName="TEST")
    app.select_word('mon')
    
    app.mainloop()
    
    if app.choix != None:
        epp.write(app.choix)
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])