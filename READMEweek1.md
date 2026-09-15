### Tugas 1

1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

Ya, saya menggunakan elemen semantik HTML5 seperti `<section>`, `<header>`, `<nav>`, `<main>`, dan `<footer>`.

Elemen-elemen tersebut membantu karena:

- Struktur lebih jelas, `<section>` memisahkan bagian Profile dan Skills, `<header>` untuk judul dan navigasi, `<footer>` untuk copyright.
- Aksesibilitas lebih baik, screen reader dan search engine lebih mudah memahami struktur halaman.
- Kode lebih rapi dan mudah dibaca, dibandingkan hanya pakai `<div>` tanpa makna, elemen semantik bikin kode lebih self-explanatory.
- Memudahkan styling, CSS bisa langsung menargetkan tag seperti `header`, `nav`, `section` tanpa perlu banyak class.

---

2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

Tantangan yang saya temukan:

- Layout grid berubah, di desktop, hero section pakai 2 kolom (identitas + foto), di mobile harus jadi 1 kolom.
- Ukuran font kegedean di mobile, heading `clamp(3rem, 7vw, 5rem)` perlu disesuaikan.
- Social links dan audio player, harus di-center atau full-width di layar kecil.
- Navigasi navbar, di layar kecil, jarak antar link harus diperkecil.

Cara evaluasi:

- Pakai media queries untuk ubah layout dari 2 kolom jadi 1 kolom.
- Prioritaskan konten utama (foto, nama, bio) tetap terlihat jelas di mobile.
- Elemen sekunder (social links, audio) diletakkan setelah konten utama, ukurannya disesuaikan.
- Testing langsung di browser dengan mode responsive (F12 → Toggle Device Toolbar).

---

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

Batasan yang saya rasakan:

- Konten hard-coded di HTML, setiap update (ganti bio, tambah skill, tambah karya) harus edit code dan redeploy.
- Gak bisa nambah data dari luar, semua data statis, gak bisa diinput lewat form atau admin.
- Gak ada manajemen konten, gak ada cara buat nambah/ubah/hapus konten tanpa ngoding.
- Data gak terstruktur, informasi tersebar di HTML, susah di-query atau difilter.

Fungsionalitas dinamis yang ingin ditambahkan:

- Database untuk menyimpan data, biar konten bisa diinput tanpa edit code.
- Halaman terpisah per section.
- Form input, buat user/admin nambah data langsung dari web.
- Search & filter, buat nyari data tertentu dengan cepat.