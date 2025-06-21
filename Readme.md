Dokumentasi Styling Website Pengolahan Citra
Dokumen ini menjelaskan cara mengubah tampilan dan gaya (styling) dari aplikasi web pengolahan citra. Anda dapat memodifikasi warna, layout, dan elemen visual lainnya sesuai dengan preferensi Anda.

cara menjalankan website
ketikan python app.py di terminal

1. Struktur File CSS
File CSS utama berada di:

static/css/style.css
2. Mengubah Warna Utama
2.1 Warna Background
Untuk mengubah warna background halaman utama, tambahkan atau ubah kode berikut di style.css:

css
body {
    background-color: #your-color-here; /* Misalnya: #f5f5f5 untuk abu-abu muda */
}
2.2 Warna Sidebar
Untuk mengubah warna background sidebar:

css
#sidebar {
    background-color: #your-color-here; /* Misalnya: #343a40 untuk warna gelap */
}
2.3 Warna Tombol
Untuk mengubah warna tombol "Upload Image":

css
#uploadBtn {
    background-color: #your-color-here; /* Warna background */
    color: #your-text-color; /* Warna teks */
    border-color: #your-border-color; /* Warna border */
}

#uploadBtn:hover {
    background-color: #your-hover-color; /* Warna saat hover */
}
Untuk mengubah warna tombol metode pemrosesan:

css
.nav-link.process-btn {
    color: #your-text-color; /* Warna teks */
}

.nav-link.process-btn:hover {
    background-color: #your-hover-background; /* Warna background saat hover */
    color: #your-hover-text-color; /* Warna teks saat hover */
}

.nav-link.process-btn.active {
    color: #your-active-color; /* Warna teks saat aktif */
    background-color: #your-active-background; /* Warna background saat aktif */
}
3. Mengubah Layout
3.1 Lebar Sidebar
Untuk mengubah lebar sidebar, ubah kedua nilai berikut (pastikan nilai sama):

css
#sidebar {
    width: 16.67%; /* Ubah nilai ini */
}

#main-content {
    margin-right: 16.67%; /* Ubah nilai ini juga (sama dengan width sidebar) */
}
3.2 Tinggi Container Gambar
Untuk mengubah tinggi maksimum dari gambar:

css
img {
    max-height: 400px; /* Ubah nilai ini sesuai kebutuhan */
}
3.3 Margin dan Padding
Untuk mengubah jarak (spacing) di sekitar elemen:

css
#originalImageContainer, #processedImageContainer {
    padding: 15px; /* Ubah nilai padding di dalam container */
    margin-bottom: 20px; /* Ubah jarak bawah container */
}
4. Mengubah Font
4.1 Font Utama
Untuk mengubah font seluruh website:

css
body {
    font-family: 'Font Name', sans-serif; /* Misalnya: 'Arial', 'Roboto', dll. */
}
4.2 Font Header
Untuk mengubah font pada judul:

css
h1, h2, h3, h4, h5, h6 {
    font-family: 'Font Name', sans-serif;
}
5. Container Gambar
Untuk mengubah tampilan container gambar:

css
#originalImageContainer, #processedImageContainer {
    background-color: #your-color-here; /* Warna background */
    border: 1px solid #your-border-color; /* Warna dan ketebalan border */
    border-radius: 6px; /* Kebulatan sudut */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Menambahkan bayangan */
}
6. Responsif untuk Layar Kecil
Anda dapat mengubah tampilan pada layar kecil (mobile):

css
@media (max-width: 767.98px) {
    #sidebar {
        /* Styling untuk sidebar pada layar kecil */
    }
    
    #main-content {
        /* Styling untuk konten utama pada layar kecil */
    }
    
    img {
        /* Styling untuk gambar pada layar kecil */
    }
}
7. Contoh Tema Custom
7.1 Tema Gelap
Berikut contoh CSS untuk tema gelap:

css
body {
    background-color: #121212;
    color: #e0e0e0;
}

#sidebar {
    background-color: #1e1e1e;
    box-shadow: -2px 0 10px rgba(0, 0, 0, 0.5);
}

#originalImageContainer, #processedImageContainer {
    background-color: #2d2d2d;
    border-color: #444;
}

.nav-link {
    color: #e0e0e0 !important;
}

.nav-link:hover {
    background-color: #333;
}

#initialPrompt {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

#uploadBtn {
    background-color: #bb86fc;
    border-color: #bb86fc;
    color: #000;
}

#uploadBtn:hover {
    background-color: #a66dfc;
    border-color: #a66dfc;
}
7.2 Tema Berwarna
Contoh tema dengan warna-warni:

css
body {
    background-color: #f0f8ff; /* Alice Blue */
}

#sidebar {
    background-color: #4169e1; /* Royal Blue */
    color: white;
}

.sidebar .nav-link {
    color: white;
}

.sidebar .nav-link:hover {
    background-color: #6495ed; /* Cornflower Blue */
}

#uploadBtn {
    background-color: #ff6347; /* Tomato */
    border-color: #ff6347;
}

#uploadBtn:hover {
    background-color: #ff4500; /* Orange Red */
    border-color: #ff4500;
}

#originalImageContainer, #processedImageContainer {
    background-color: white;
    border-color: #87ceeb; /* Sky Blue */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
8. Tips Tambahan
Gunakan DevTools Browser: Klik kanan pada elemen yang ingin diubah dan pilih "Inspect" untuk melihat dan mencoba perubahan CSS langsung di browser.
Font dari Google Fonts: Jika ingin menggunakan font custom, Anda bisa menambahkan Google Fonts:
html
<!-- Tambahkan ini di head pada index.html -->
<link href="https://fonts.googleapis.com/css2?family=NamaFont:wght@400;700&display=swap" rel="stylesheet">
Animations: Tambahkan animasi untuk membuat UI lebih dinamis:
css
.process-btn {
    transition: all 0.3s ease;
}
Gradient Background: Gunakan gradient untuk background yang lebih menarik:
css
#sidebar {
    background: linear-gradient(to bottom, #3a1c71, #d76d77, #ffaf7b);
    color: white;
}
Custom Scrollbar: Tambahkan scrollbar custom untuk sidebar:
css
#sidebar::-webkit-scrollbar {
    width: 5px;
}

#sidebar::-webkit-scrollbar-track {
    background: #f1f1f1;
}

#sidebar::-webkit-scrollbar-thumb {
    background: #888;
}

#sidebar::-webkit-scrollbar-thumb:hover {
    background: #555;
}
Dengan panduan ini, Anda dapat memodifikasi tampilan website pengolahan citra sesuai dengan preferensi Anda.

