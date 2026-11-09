# Buka website BMD di aplikasi Codex

Paket ini berisi kode lengkap website versi 15, termasuk foto, font, versi
Mandarin Tradisional, dan data pencarian. Tampilan yang sudah kamu setujui tetap
menjadi titik awal.

## Langkah di komputermu

1. Ekstrak ZIP ini terlebih dahulu, misalnya ke `Documents/TCU-BMD-Website`.
2. Di aplikasi Codex, buka folder **TCU-BMD-Website** yang berisi `AGENTS.md`,
   `build.py`, dan folder `dist`. Pilih folder utama ini agar Codex dapat membaca
   sumber dan petunjuk proyek.
3. Mulai percakapan di proyek tersebut. Kamu bisa memakai pesan pembuka ini:

```text
Ini proyek website Tzu Chi BMD yang sudah aku kerjakan sebelumnya.
Baca AGENTS.md dan README.md, lalu jalankan preview lokalnya.
Pertahankan desain versi sekarang, termasuk identitas hijau, foto,
tipografi, animasi halus, fitur, dan bahasa Inggris/Mandarin Tradisional.
Setelah preview siap, aku akan memberi perubahan berikutnya.
```

## Melihat preview

Minta Codex menjalankan:

```bash
python preview.py
```

Lalu buka **http://127.0.0.1:4173/**. Preview ini memakai file yang sudah tersedia
di `dist/`; tidak perlu membangun ulang untuk melihat hasil versi 15.

Jika komputermu memakai perintah `py` untuk Python, jalankan `py preview.py`.
Jika Python belum tersedia, beri tahu Codex agar membantu menyiapkan runtime.

## Setelah mengubah isi atau desain

Codex dapat mengikuti `AGENTS.md` untuk memasang dependensi, membangun ulang
halaman, dan menjalankan pemeriksaan. Pustaka Python yang digunakan untuk
membangun ulang tercantum di `requirements.txt`.

Kode utama dan data konten ikut disertakan, jadi perubahan tidak terbatas pada
file HTML hasil akhirnya saja. Font dan foto disimpan lokal; video YouTube serta
tautan resmi universitas tetap memerlukan internet.

## Website yang sudah online

Versi online saat ekspor:
https://tcu-bmd-green-campus.violetray64.chatgpt.site/

Membuka folder ini memberi Codex akses untuk mengedit salinan di komputermu.
Perubahan tersebut belum otomatis tersinkron ke situs online atau repository
GitHub. Publikasi dan sinkronisasi bisa disiapkan setelah proyek berhasil dibuka.

Dokumentasi resmi OpenAI tentang membuka folder dan memilih Codex:
https://learn.chatgpt.com/docs/quickstart
