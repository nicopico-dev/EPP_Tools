# python fastOpen.py -p "%PROJECTFILE%"
import sys
import optparse
import os.path
import tkinter as tk
import tkinter.ttk as ttk

import epp_utils as epp

class TkFastOpen(tk.Frame):
    def __init__(self, master=None, title='Fast Open', width=800, height=300):
        self.availableFiles = []
        self.candidates = []
        self.chosenFile = None

        tk.Frame.__init__(self, master)
        self.grid(sticky="nsew")    # Necessary to make the UI stretchable
        self.create_widgets()
        self.master.title(title)
        self.set_geometry(width, height)

    def create_widgets(self):
        # Strechable UI
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        # Strechable cells / rows
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        # Text input
        self.textInput = tk.Entry(self)
        self.textInput.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.textInput.bind("<KeyRelease>", self.refreshCandidates)
        self.textInput.bind("<Down>", self.focusToList)
        self.textInput.focus()

        # List of candidates
        self.listCandidates = tk.Listbox(self, selectmode=tk.BROWSE, activestyle="none")
        self.listCandidates.configure(font=("Courier New", "8"))
        self.listCandidates.bind("<Double-Button-1>", self.handle_Ok)
        self.listCandidates.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        # Bouton Ok
        self.buttonOk = tk.Button(self, text="Ok", command=self.handle_Ok, default=tk.ACTIVE)
        self.buttonOk.grid(row=2, column=0, sticky="nsew")

        # Bouton Cancel
        self.buttonExit = tk.Button(self, text="Cancel", command=self.quit)
        self.buttonExit.grid(row=2, column=1, sticky="nsew")

        # Global keyboard events
        self.bind_all("<Escape>", self.handle_Escape)
        self.bind("<Enter>", self.handle_Ok)
        self.bind("<Return>", self.handle_Ok)

    def set_geometry(self, wapp, happ):
        # Centre l'application sur l'ecran
        xapp = (self.winfo_screenwidth() - wapp) / 2
        yapp = (self.winfo_screenheight() - happ) / 2
        self.master.geometry("%dx%d+%d+%d" % (wapp, happ, xapp, yapp))

    def handle_Escape(self, event=None):
        if event == None or event.widget != self.listCandidates:
            epp.log("handle_Escape")
            self.quit()
        elif event.widget == self.listCandidates:
            self.focusToTextInput()
        
    def handle_Ok(self, event=None):
        idx = self._getCurrentSelIndex()
        if idx != None:
            self.chosenFile = self.listCandidates.get(idx)
        epp.log("handle_Ok")
        self.quit()
                    
    def _getCurrentSelIndex(self):
         idx = self.listCandidates.curselection()
         if len(idx) > 0:
            return int(idx[0])
         else:
            return None
    
    def refreshCandidates(self, event=None):
        self.listCandidates.delete(0, tk.END)
        searchTerm = self.textInput.get()
        for f in [f for f in self.availableFiles if isValidCandidate(searchTerm, f)]:
            self.listCandidates.insert(tk.END, f)
    
    def focusToList(self, event=None):
        self.listCandidates.focus()
        self.listCandidates.selection_clear(0, tk.END)
        self.listCandidates.selection_set(0, 0)

    def focusToTextInput(self, event=None):
        self.textInput.focus()

    def quit(self, event=None):
        epp.log("QUIT")
        self.master.quit()

def isValidCandidate(searchTerm, candidate):
    filename = os.path.basename(candidate)
    return searchTerm in filename

def main(argv):
    parser = optparse.OptionParser()
    parser.add_option("-p","--project",action="store",type="string",dest="project",help="Project file")
    
    (options, args) = parser.parse_args(argv)
    
    epp.log("project file: %s" % (options.project))
    
    if options.project:
        files = epp.getProjectFiles(options.project)
        
        app = TkFastOpen()
        app.availableFiles = files
        app.mainloop()
    
        if app.chosenFile != None:
            # Open the file with EPP
            epp.openWithEPP(app.chosenFile)
        
    else: 
        # On provoque une erreur
        parser.error('project') 
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])