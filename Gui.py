import Tkinter as tk
from tkFileDialog import askopenfilename
import tkMessageBox
import model

class Gui(tk.Frame):

    def __init__(self, master):
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self, master, width=500, height=500)
        # Set the title
        self.master.title('"K Means Clustering"')

        # This allows the size specification to take effect
        self.pack_propagate(0)

        # We'll use the flexible pack layout manager
        self.pack()

        self.file_path_val = tk.StringVar()
        self.file_path_label = tk.Label(self, text='choose file path')
        self.file_path_label.grid(row=0)

        self.file_path = tk.Entry(self)
        self.file_path.grid(row=0, column=1)

        self.brows = tk.Button(self, text='Browse', command=self.brows_file)
        self.brows.grid(row=0,column=2)

        self.Num_of_runs_val = tk.IntVar()
        self.Num_of_runs_label = tk.Label(self, text='Num of runs')
        self.Num_of_runs_label.grid(row=1)

        self.Num_of_runs = tk.Entry(self, textvariable=self.Num_of_runs_val)
        self.Num_of_runs.grid(row=1, column=1)
        self.Num_of_runs_val.set(1)

        self.Num_of_clusters_val = tk.IntVar()
        self.Num_of_clusters_label = tk.Label(self, text='Num of clusters k')
        self.Num_of_clusters_label.grid(row=2)

        self.Num_of_clusters = tk.Entry(self, textvariable=self.Num_of_clusters_val)
        self.Num_of_clusters.grid(row=2, column=1)
        self.Num_of_clusters_val.set(2)

        # The pre_process button
        self.pre_process = tk.Button(self, text='Pre-process', command=self.pre_process)
        self.pre_process.grid(row=3)

        # The cluster button
        self.cluster = tk.Button(self, text='Cluster', command=self.build_model)
        self.cluster.grid(row=3, column=1)

    def run(self):
        self.mainloop()

    def brows_file(self):
        self.file_path_val = askopenfilename(title='K Means Clustering', filetypes=[("Excel files", "*.xlsx")])
        self.file_path.insert(0, self.file_path_val)

    def pre_process(self):
        try:
            model.pre_process(self.file_path_val)
            tkMessageBox.showinfo("K Means Clustering", "Preprocessing complited successfully")
        except ValueError as ve:
            tkMessageBox.showerror("K Means Clustering", ve.message)

    def build_model(self):
        try:
            num_of_runs = self.Num_of_runs_val.get()
            num_of_clusters = self.Num_of_clusters_val.get()
            if(num_of_runs < 1):
                tkMessageBox.showerror("K Means Clustering", 'invalid number of runs')
            if (num_of_clusters < 2):
                tkMessageBox.showerror("K Means Clustering", 'number of cluster have to be grater then 1')
            model.k_means(num_of_clusters, num_of_runs)
            model.plot_scatter()
        except ValueError as ve:
            tkMessageBox.showerror("K Means Clustering", ve.message)

app = Gui(tk.Tk())
app.run()
