### Tugas 3

1. Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!

Kita menggunakan `ModelForm` alih-alih membuat form HTML manual karena:

- Otomatis generate field — `ModelForm` bikin field HTML berdasarkan field di model, gak perlu nulis `<input>` satu-satu.
- Validasi bawaan — Django otomatis validasi input sesuai tipe data di model (misal: `URLField` cek apakah input beneran URL).
- Hemat kode — Gak perlu nulis ulang field HTML + CSS + validasi manual.
- Konsisten dengan model — Kalo field di model berubah, form otomatis update.
- Langsung bisa `save()` — `form.save()` langsung simpen ke database tanpa perlu mapping manual.

`{% csrf_token %}` wajib ditambahkan karena:

- CSRF (Cross-Site Request Forgery) protection — Tanpa token ini, website bisa diserang CSRF, di mana penyerang memalsukan request dari user yang udah login.
- Validasi Django — Tanpa `{% csrf_token %}`, Django bakal nolak request POST dengan error `403 Forbidden`.
- Token unik per session — Token ini di-generate Django per session dan diverifikasi pas form disubmit.

---

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

JSON lebih disukai karena:

- Lebih ringkas — JSON gak butuh closing tag kaya XML (`<nama>...</nama>` vs `"nama": "..."`), jadi ukuran data lebih kecil.
- Lebih cepat di-parse — Parser JSON lebih cepat dan ringan dibanding XML.
- Integrasi natural dengan JavaScript — JSON itu subset dari JavaScript, jadi frontend bisa langsung `JSON.parse()` tanpa library tambahan.
- Lebih mudah dibaca — Struktur key-value lebih simpel dibanding nested tag XML.
- Cocok buat RESTful API — Standar API modern pake JSON.
- Support tipe data — JSON punya tipe data jelas (string, number, boolean, null, array, object), XML semua-nya string.

XML masih dipake di enterprise, SOAP, dan konfigurasi tertentu, tapi buat web modern, JSON lebih praktis.

---

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

Alur ketika view mengembalikan data JSON:

1. Client kirim request ke endpoint, misal `/api/creativespaces/`.
2. URL routing (`urls.py`) arahin ke view `get_creativespaces_json`.
3. View query database — `CreativeSpace.objects.all()` ambil semua objek model.
4. Filter (opsional) — Kalo ada query parameter (`?title=...`), data difilter pake `filter(title__icontains=...)`.
5. Serialization — `serializers.serialize("json", creativespaces)` mengubah objek model jadi string JSON.
6. Response — `HttpResponse(json_data, content_type="application/json")` kirim balik ke client.
7. Client terima JSON — Bisa diproses lebih lanjut (misal: di-deserialize buat render HTML, atau dipake JavaScript fetch).

Kenapa perlu serialization?

- Objek Python gak bisa dikirim langsung — Django model itu objek Python kompleks (punya method, relasi, dll), gak bisa langsung dijadikan response HTTP.
- HTTP cuma transfer teks — Response HTTP harus berupa string/byte, bukan objek.
- JSON = format universal — Setelah di-serialize, data bisa dibaca oleh bahasa apapun (JavaScript, Python, Java, dll).
- Deserialization — Di sisi client, JSON bisa di-deserialize balik jadi objek Python pake `serializers.deserialize()`, seperti yang kita lakukan di `show_creative_space`.

Tanpa serialization, kita gak bisa ngirim data terstruktur lewat HTTP dengan format standar.