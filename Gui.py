import Tkinter as tk

class Gui(tk.Frame):

    def __init__(self, master):
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self, master, width=300, height=200)
        # Set the title
        self.master.title('Clustering Model')

        # This allows the size specification to take effect
        self.pack_propagate(0)

        # We'll use the flexible pack layout manager
        self.pack()

        # The pre_process button
        self.pre_process = tk.Button(self, text='Pre-process', command=master.quit)

        # The cluster button
        self.cluster = tk.Button(self, text='Cluster', command=master.quit)

        # Put the controls on the form
        self.pre_process.pack(fill=tk.X, side=tk.BOTTOM)
        self.cluster.pack(fill=tk.X, side=tk.BOTTOM)

    def run(self):
        self.mainloop()

# app = Gui(tk.Tk())
# app.run()