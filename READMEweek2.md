### Tugas 2

1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portfolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran `urls.py` proyek, `urls.py` aplikasi, view, model, dan template.

Ketika pengguna membuka halaman Creative Space (`/creative-space/`), alurnya:

1. Browser mengirim HTTP request ke server.
2. `urls.py` proyek menerima request dan mengarahkannya ke `urls.py` aplikasi `main` (via `include`).
3. `urls.py` aplikasi mencocokkan URL `creative-space/` dengan view `show_creative_space`, lalu meneruskan request ke view tersebut.
4. View (`show_creative_space`) memanggil model `CreativeSpace` untuk mengambil data dari database.
5. Model menjalankan query ke database dan mengembalikan data dalam bentuk QuerySet.
6. View memasukkan data tersebut ke dalam `context` dan merender template `creative_space.html`.
7. Template menampilkan data menggunakan Django Template Language (loop `{% for %}`).
8. Browser menerima HTML yang sudah dirender dan menampilkannya ke pengguna.

---

2. Mengapa data untuk bagian portfolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

Karena dengan menyimpan data di model:

- Single source of truth: data tersimpan di satu tempat (database), bukan tersebar di HTML.
- Maintenance lebih mudah: nambah/ubah/hapus data cukup lewat admin atau shell, tanpa perlu edit HTML dan redeploy.
- Konsisten: model punya validasi, jadi data gak rawan typo atau format yang beda-beda.
- Scalable: data yang sama bisa dipakai di banyak halaman (homepage, detail, search) tanpa copy-paste.
- Separation of concerns: data (model) terpisah dari tampilan (template), sesuai prinsip MVT.

Dampaknya: aplikasi lebih gampang di-maintain, dikembangin, dan di-test. Kalo data di-hardcode di template, setiap perubahan konten harus lewat edit code + deploy ulang.

---

3. Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

- `makemigrations` → membuat file migrasi dari perubahan model (belum mengubah database).
- `migrate` → menerapkan file migrasi ke database (mengubah struktur tabel).
Contoh: Saat menambahkan model `CreativeSpace` di `models.py`.

```bash
python manage.py makemigrations
# Output: main/migrations/0002_creativespace.py

python manage.py migrate
# Output: Applying main.0002_creativespace... OK