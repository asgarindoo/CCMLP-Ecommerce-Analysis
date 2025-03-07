# 📊 Ecommerce Dashboard  

Dashboard analitik penjualan online menggunakan Streamlit untuk menganalisis data penjualan!  

## 🚀 Cara Menjalankan Dashboard  

### 1. **Persyaratan**  
Pastikan sistem Anda memiliki:  

```
- Python 3.8 atau lebih baru  
- pip (Python package manager)  
- Virtual environment (opsional, disarankan)  
```

### 2. **Instalasi Dependensi**  
Jika belum menginstal dependensi, jalankan perintah berikut:  

```bash
pip install -r requirements.txt
```

### 3. **Menjalankan Dashboard**  
Jalankan perintah berikut di terminal atau command prompt:  

```bash
streamlit run dashboard.py
```
Pastikan `dashboard.py` adalah file utama dari proyek ini. Setelah menjalankan perintah, Streamlit akan membuka dashboard di browser secara otomatis.  

### 4. **Menyiapkan Data**  
Pastikan file dataset (`all_data.csv`) tersedia di direktori proyek yang sama. Jika tidak, letakkan file tersebut sesuai dengan konfigurasi di dalam kode.  

### 5. **Menyesuaikan Rentang Waktu**  
Di sidebar, Anda bisa memilih rentang waktu dengan dua kolom input: `start_date` dan `end_date`. Pastikan memilih rentang tanggal yang benar untuk menghindari error.  

### 6. **Error Handling**  
Jika muncul error saat memilih rentang tanggal, pastikan:  
- File `all_data.csv` memiliki kolom `order_purchase_timestamp` dalam format yang benar (datetime).  
- `start_date` tidak lebih besar dari `end_date`.  

### 7. **Menutup Dashboard**  
Untuk menghentikan dashboard, tekan `CTRL + C` di terminal.  

## 📌 Catatan Tambahan  
- Pastikan semua library telah diperbarui dengan menjalankan:  

```bash
pip freeze > requirements.txt
```
- Jika mengalami masalah, coba jalankan ulang di virtual environment atau pastikan dataset tersedia.  

🎯 **Selamat menggunakan Ecommerce Dashboard!** 🚀  
