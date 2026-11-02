### Tugas 5

1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

Debouncing merupakan teknik untuk menunda eksekusi sebuah fungsi sampai beberapa waktu tertentu telah berlalu tanpa adanya event baru. Jika event baru terjadi sebelum waktu tunggu habis, timer akan direset dan waktu tunggu dimulai ulang dari awal.

Pada fitur pencarian dengan AJAX, debouncing penting karena tanpa debouncing, setiap karakter yang diketik pengguna akan memicu satu request ke server. Misalnya user mengetik "Dragonair" (9 karakter), tanpa debouncing browser akan mengirim 9 request berturut-turut, padahal user baru selesai mengetik di karakter terakhir. Ini membuang resource server, memperlambat respons, dan bisa menyebabkan hasil pencarian yang ga konsisten (request lama menimpa request baru).

Dengan debouncing (misalnya delay 300ms), browser hanya mengirim satu request setelah pengguna berhenti mengetik selama 300ms. Hasilnya lebih efisien, hemat bandwidth, dan pengalaman pencarian jadi lebih responsif.

---

2. Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita ga menggunakan `await`?

`await` berfungsi untuk "menunggu" Promise dari `fetch()` selesai diproses sebelum melanjutkan ke baris kode berikutnya. Karena `fetch()` mengembalikan Promise (operasi asinkron), tanpa `await`, JavaScript akan langsung mengeksekusi baris berikutnya tanpa menunggu respons dari server.

Jika ga menggunakan `await`:
- Variabel yang seharusnya menyimpan hasil respons justru berisi objek `Promise` yang belum selesai (status `pending`).
- Kode berikutnya berjalan sebelum data tersedia, sehingga bisa menyebabkan error seperti `undefined` atau `TypeError` saat mencoba mengakses data.
- Hasil akhirnya ga deterministic (kadang berhasil, kadang gagal, tergantung seberapa cepat server merespons.)

`await` hanya bisa dipakai di dalam fungsi `async`, dan membuat alur kode asinkron jadi terbaca seperti kode sinkron biasa, jadi lebih mudah dibaca dan didebug.

---

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

XSS (Cross-Site Scripting) adalah jenis serangan di mana penyerang berhasil menyisipkan kode JavaScript berbahaya ke dalam halaman web, yang kemudian dieksekusi di browser pengguna lain. Salah satu variannya adalah stored XSS, di mana kode berbahaya disimpan ke database (misalnya sebagai judul artwork) lalu otomatis dijalankan tiap kali data tersebut ditampilkan.

Data yang ditampilkan lewat template Django relatif aman karena Django melakukan auto-escaping otomatis pada setiap `{{ variabel }}`. Karakter seperti `<`, `>`, `"`, dan `'` diubah menjadi HTML entity (`&lt;`, `&gt;`, dst) sehingga browser menampilkannya sebagai teks biasa, bukan sebagai tag HTML.

Sebaliknya, data yang ditampilkan lewat AJAX/JavaScript kehilangan perlindungan itu. Ketika kita menyisipkan data dari JSON ke `innerHTML` menggunakan template literal, ga ada yang melakukan escaping otomatis. Jika data berisi `<img src=x onerror=alert('XSS!')>`, browser akan mengeksekusi `onerror` sebagai kode JavaScript. Penyerang bahkan bisa membaca cookie `csrftoken` lalu mengirim request atas nama korban.

Karena itu, pada implementasi AJAX kita perlu menambahkan `escapeHtml()` di sisi klien/user untuk menggantikan karakter berbahaya, dan `strip_tags` di sisi server (via method `clean_<field>` pada ModelForm) sebagai lapisan pertahanan kedua.