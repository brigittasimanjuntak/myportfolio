### Tugas 6

1. Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!

REST (Representational State Transfer) adalah gaya arsitektur untuk merancang web API, bukan sekadar library atau format data. REST memperlakukan data sebagai *resource* (sumber daya) yang diakses melalui URL, dan menggunakan metode HTTP (GET, POST, PUT, PATCH, DELETE) untuk menyatakan tindakan terhadap resource tersebut. 

Mengembalikan data dalam format JSON saja belum cukup untuk menyebut API sebagai RESTful. API yang mengembalikan JSON tapi menggunakan URL seperti `/getData.php?id=1` atau `/deleteProject.php` belum tentu RESTful. Sebuah API bisa disebut RESTful jika mematuhi batasan (constraints) REST, seperti:
- Resource-based URLs: Menggunakan kata benda (noun) di URL, misalnya `/api/v1/projects/` (bukan kata kerja).
- HTTP Methods: Tindakan ditentukan oleh metode HTTP (DELETE untuk menghapus, bukan URL `/delete`).
- Stateless: Setiap request harus membawa semua informasi yang dibutuhkan (meskipun pada praktiknya kita tetap menggunakan SessionAuthentication untuk kenyamanan AJAX).

Perbedaan PUT dan PATCH:
- PUT digunakan untuk mengganti seluruh representasi resource. Jika ada field yang enga dikirim, field tersebut akan dianggap kosong atau kembali ke nilai default. Cocok digunakan ketika kita mengirim seluruh data form dari awal (misal: update profile lengkap).
- PATCH digunakan untuk mengubah sebagian field saja. Field yang enga dikirim akan tetap mempertahankan nilai lamanya. Cocok digunakan ketika kita hanya ingin mengubah judul tanpa menyentuh deskripsi (misal: edit cepat judul artwork di modal). Pada implementasi DRF kita, `partial=True` pada PATCH membuat pembaruan parsial ini berjalan.

---

2. Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?

Peran Serializer:
Serializer adalah jembatan dua arah antara objek Python (model database) dan format data seperti JSON. Pada saat klien melakukan GET, serializer mengubah data model (QuerySet) menjadi format JSON (serialization). Sebaliknya, pada saat klien melakukan POST/PUT/PATCH, serializer menerima input dari klien (JSON), memvalidasinya, dan mengubahnya menjadi objek Python yang siap disimpan ke database (deserialization).

Keuntungan dibandingkan merakit dictionary manual dengan JsonResponse:
1. Validasi Otomatis: Pada Tutorial 05, kita harus merakit dictionary manual dan menulis validasi sendiri (misalnya lewat `ProjectForm`). Di DRF, serializer otomatis memvalidasi tipe data berdasarkan model, serta mempermudah validasi kustom (seperti pengecekan `strip_tags` pada `validate_title`).
2. Kode Lebih Ringkas & DRY: Kita enga perlu lagi menulis perulangan manual untuk mengonversi setiap objek menjadi dictionary (seperti `data.append({...})`). Cukup panggil `Serializer(objek, many=True)` dan hasilnya siap dirender.
3. Keamanan Terpusat: Mengatur field mana yang boleh dibaca (`read_only_fields`) atau disembunyikan menjadi jauh lebih aman. Kita enga berisiko enga sengaja membocorkan data sensitif (seperti password hash atau email) karena daftar field dideklarasikan eksplisit di satu tempat.
4. Penanganan Status HTTP & Error: Saat serializer gagal memvalidasi input (misalnya judul kosong), DRF secara otomatis mengembalikan respons JSON berisi pesan error dengan status `400 Bad Request`. Kita enga perlu lagi merakit manual `JsonResponse` beserta `form.errors`.

---

3. Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?

Perbedaan Autentikasi dan Otorisasi:
- Autentikasi adalah proses memverifikasi "Siapa kamu?". Di DRF, kita menggunakan `SessionAuthentication` untuk mengenali pengguna berdasarkan cookie session yang dibuat saat login di web Django.
- Otorisasi adalah proses menentukan "Apa yang boleh kamu lakukan?". Ini dilakukan oleh *permission class* (misalnya `IsPortfolioOwnerOrEditorOrReadOnly`). Setelah server tahu siapa penggunanya, permission class memeriksa apakah user tersebut punya izin mencoba akses (misal: apakah dia Superuser atau Editor?).

Mengapa hak akses harus diperiksa di server?
Menyembunyikan tombol di template (misalnya dengan `{% if user.is_superuser %}`) hanyalah lapisan UI (User Experience) agar tampilan rapi. Ini bukan keamanan.
Jika kita hanya menyembunyikan tombol, penyerang bisa membuka Developer Tools, mengubah DOM, atau menggunakan aplikasi seperti Postman untuk mengirim request HTTP `POST` atau `DELETE` secara langsung ke endpoint API. Jika server enga memvalidasi hak akses, penyerang bisa merusak data meskipun tombolnya enga terlihat. Karena itu, pengecekan via *permission class* di server adalah benteng pertahanan utama yang wajib ada.

---

4. Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate enga cukup untuk membuktikan bahwa perlindungan CSRF berjalan?

Mengapa butuh token CSRF?
Saat menggunakan `SessionAuthentication`, browser secara otomatis melampirkan cookie session milik pengguna pada setiap request ke domain yang sama. 
Tanpa proteksi CSRF, penyerang bisa membuat situs web palsu (misal: `situsjahat.com`) yang berisi form atau script yang mengirim request `POST` ke `https://portofolio-kamu.com/api/v1/creativespaces/`. Karena browser pengguna masih memiliki cookie session yang aktif, server Django akan mengira request itu sah dan menghapus data pengguna. 
Token CSRF (dikirim via header `X-CSRFToken`) memastikan bahwa request tersebut sengaja dibuat dari antarmuka web kita sendiri (yang memiliki token), bukan dari situs penyerang (yang enga memiliki token).

Mengapa `force_authenticate` enga cukup?
Fungsi `force_authenticate` di *test suite* bertindak seolah-olah user sudah login dan mem-bypass seluruh mekanisme autentikasi bawaan, termasuk pengecekan CSRF. Test tersebut hanya membuktikan bahwa *permission class* (otorisasi) bekerja berdasarkan user yang sudah login, tetapi enga menguji apakah *SessionAuthentication* dan proteksi CSRF benar-benar aktif di dunia nyata.
Untuk membuktikannya, kita harus membuat test khusus menggunakan `APIClient(enforce_csrf_checks=True)` yang memaksa DRF memeriksa CSRF, lalu melakukan request tanpa header `X-CSRFToken`. Jika request tersebut ditolak dengan status `403 Forbidden`, barulah kita tahu bahwa server benar-benar melindungi endpoint dari serangan CSRF.