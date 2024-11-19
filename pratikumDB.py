import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Membuat koneksi ke database SQLite
def create_database():
    con = sqlite3.connect('nilai_siswa.db')     # Membuat atau menghubungkan ke database 'nilai_siswa.db'
    cursor = con.cursor()                       # Membuat objek cursor untuk menjalankan perintah SQL
    cursor.execute('''                          
        CREATE TABLE IF NOT EXISTS nilai_siswa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    con.commit()# Menyimpan perubahan pada database
 
def fetch_data():
    con = sqlite3.connect('nilai_siswa.db')     # Membuka koneksi ke database
    cursor = con.cursor()                       # Membuat objek cursor untuk menjalankan perintah SQL
    cursor.execute("SELECT * FROM nilai_siswa") # Mengambil semua data dari tabel `nilai_siswa`
    rows = cursor.fetchall()                    # Menyimpan hasil query ke dalam variabel `rows`
    con.close()                                 # Menutup koneksi ke database
    return rows                                 # Mengembalikan data hasil query

def save_to_database(nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()                       # Membuat objek cursor untuk menjalankan perintah SQL
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama_siswa, biologi, fisika, inggris, prediksi_fakultas))
    # Menyisipkan data baru ke dalam tabel `nilai_siswa`INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)
    con.commit()                                # Menyimpan perubahan ke database
    con.close()                                 # Menutup koneksi

def update_database(id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    con = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database
    cursor = con.cursor()                   # Membuat objek cursor untuk menjalankan perintah SQL
    cursor.execute("""
        UPDATE nilai_siswa SET
            nama_siswa = ?,
            biologi = ?,
            fisika = ?,
            inggris = ?,
            prediksi_fakultas = ?
        WHERE id = ?
    """, (nama_siswa, biologi, fisika, inggris, prediksi_fakultas, id))
    con.commit()
    con.close()

def delete_database(id):
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM nilai_siswa WHERE id = ?", (id,))  # # Menghapus data berdasarkan ID
    con.commit()
    con.close()


def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  #Jika nilai Biologi tertinggi
        return "Kedokteran"                     #Prediksi fakultas Kedokteran
    elif fisika > biologi and fisika > inggris: #Jika nilai Fisika tertinggi
        return "Teknik"                         #Prediksi fakultas Teknik
    elif inggris > biologi and inggris > fisika:#Jika nilai Bahasa Inggris tertinggi
        return "Bahasa"                         #Prediksi fakultas Bahasa
    else:
        return "Tidak Diketahui"
    
def submit():
    try:
        nama_siswa = nama_var.get()             # Mengambil input nama siswa dari form
        biologi = int(biologi_var.get())        # Mengambil input nilai Biologi
        fisika = int(fisika_var.get())          # Mengambil input nilai Fisika
        inggris = int(inggris_var.get())        # Mengambil input nilai Bahasa Inggris

        if not nama_siswa:                      # Validasi jika nama kosong
            raise Exception("Nama siswa tidak boleh kosong.")   

        prediksi = calculate_prediction(biologi, fisika, inggris)       # Menghitung prediksi fakultas
        save_to_database(nama_siswa, biologi, fisika, inggris, prediksi) # Menyimpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def update():
    try:
        if not selected_id.get():
            raise Exception("Pilih data yang akan diupdate!")  # Validasi jika tidak ada data yang dipilih untuk diupdate
        
        id = int(selected_id.get())         ## Mendapatkan ID data yang dipilih
        nama = nama_var.get()               # Mendapatkan input nama siswa dari form
        biologi = int(biologi_var.get())    ## # Mendapatkan input nilai Biologi
        fisika = int(fisika_var.get())      # Mendapatkan input nilai Fisika
        inggris = int(inggris_var.get())     # Mendapatkan input nilai Bahasa Inggris

        prediksi = calculate_prediction(biologi, fisika, inggris)   ## Menghitung prediksi fakultas
        update_database(id, nama, biologi, fisika, inggris, prediksi)   # # Memperbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diupdate!")    # # Menampilkan notifikasi sukses
        clear_inputs()      # # Mengosongkan input
        populate_table()    # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete():         # Validasi jika tidak ada data yang dipilih untuk dihapus
    try:
        if not selected_id.get():           
            raise Exception("Pilih data yang akan dihapus!")
        
        id = int(selected_id.get()) # Mendapatkan ID data yang dipilih
        delete_database(id) # Menghapus data berdasarkan ID dari database

        messagebox.showinfo("Sukses", "Data berhasil dihapus!") # Menampilkan notifikasi sukses
        clear_inputs() # Mengosongkan input
        populate_table()# Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs():
    nama_var.set("")# Mengosongkan input nama siswa
    biologi_var.set("")# Mengosongkan input nilai Biologi
    fisika_var.set("")# Mengosongkan input nilai Fisika
    inggris_var.set("") # Mengosongkan input nilai Bahasa Inggris

    selected_id.set("")# Mengosongkan input ID data yang dipilih

def populate_table():
    for row in tree.get_children():
        tree.delete(row)# Membersihkan semua data di tabel TreeView
    for row in fetch_data():
        tree.insert("", "end", values=row)# Menambahkan setiap baris data ke tabel TreeView

def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)["values"]# Mengisi nama siswa ke dalam variabel input

        selected_id.set(selected_row[0])

        nama_var.set(selected_row[1])   # Mengisi ID ke dalam variabel input
        biologi_var.set(selected_row[2])# Mengisi nilai Biologi ke dalam variabel input
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

create_database()

root = Tk()# Membuat jendela utama aplikasi
root.title("Prediksi Fakultas Siswa")# Memberikan judul pada jendela

nama_var = StringVar()# Variabel untuk menyimpan input nama siswa
biologi_var = StringVar()# Variabel untuk menyimpan input nilai Biologi
fisika_var = StringVar()# Variabel untuk menyimpan input nilai Fisika
inggris_var = StringVar() # Variabel untuk menyimpan input nilai Bahasa Inggris
selected_id = StringVar() # Variabel untuk menyimpan ID data yang dipilih


Label(root, text="Nama Siswa:").grid(row=0, column=0, sticky="w")    # Label untuk nama siswa
Entry(root, textvariable=nama_var).grid(row=0, column=1)            # Input untuk nama siswa

Label(root, text="Nilai Biologi:").grid(row=1, column=0, sticky="w")    # Label untuk nilai Biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1)             # Input untuk nilai Biologi

Label(root, text="Nilai Fisika:").grid(row=2, column=0, sticky="w")     # Label untuk nilai Fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1)               # Input untuk nilai Fisika

Label(root, text="Nilai Bahasa Inggris:").grid(row=3, column=0, sticky="w")      # Label untuk nilai Bahasa Inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1)                     # Input untuk nilai Bahasa Inggris

Button(root, text="Simpan", command=submit).grid(row=4, column=0)           # Tombol untuk menyimpan data
Button(root, text="Update", command=update).grid(row=4, column=1)           # Tombol untuk memperbarui data
Button(root, text="Hapus", command=delete).grid(row=4, column=2)              # Tombol untuk menghapus data


columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("id", text="ID")#membuat header
tree.heading("nama_siswa", text="Nama Siswa")
tree.heading("biologi", text="Nilai Biologi")
tree.heading("fisika", text="Nilai Fisika")
tree.heading("inggris", text="Nilai Bahasa Inggris")
tree.heading("prediksi_fakultas", text="Prediksi Fakultas")
tree.column("id", width=50) #MEMBUAT COLUMN
tree.column("nama_siswa", width=200)
tree.column("biologi", width=100)
tree.column("fisika", width=100)
tree.column("inggris", width=100)
tree.column("prediksi_fakultas", width=200)

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor="center")

tree.bind("<ButtonRelease-1>", fill_inputs_from_table)

root.mainloop()

