# BMD — revisi desain dan akses informasi

8 November 2026 · berdasarkan ekspor versi 15. Ini revisi lokal, bukan nomor versi publikasi situs online.

## Penilaian desain

Fondasinya sudah kuat: identitas hijau, kampus Hualien, kombinasi Archivo/Public Sans/Newsreader, dan foto kegiatan nyata memberi karakter yang layak dipertahankan. Mengganti semuanya dengan template baru justru membuang bagian terbaiknya.

Yang perlu diperbaiki ialah hubungan antara tampilan menarik dan kegunaan: label yang jelas, hierarki informasi, keterbacaan tombol, akses mahasiswa internasional, dan kalender yang membedakan informasi berikutnya dengan kegiatan yang telah selesai. Skor numerik dalam evaluasi AI bukan pengganti pengujian visual dan interaksi.

## Sudah diterapkan

- Homepage: identitas jurusan dijelaskan dalam satu kalimat; tautan cepat punya keterangan tujuan; berita memakai judul yang lebih spesifik; komposisi foto bidang studi dibuat lebih bervariasi. Ukuran tombol dan kontrol slideshow diperbesar. Foto, warna hijau, serta animasi yang sudah disetujui tetap digunakan.
- Sertifikat: 62 entri yang diturunkan dari seluruh tabel publikasi, dengan pencarian nama Inggris/Mandarin serta filter 10/15/20 poin. Inggris merupakan terjemahan deskriptif, bukan klaim nama sertifikat Inggris resmi. Versi Mandarin mengutamakan nama asli dan menyediakan alias Inggris. Kedua tabel asli tetap utuh dalam bagian yang bisa dibuka. Tanggal revisi aturan dan contoh perhitungan 20 + 10 ditampilkan dengan arahan konfirmasi ke系辦/departemen.
- Admissions: bagian khusus pelamar internasional dengan tautan ke panduan pendaftaran, beasiswa/biaya, pusat bahasa, serta Global Affairs dan student handbook. Pengunjung mendapat jalur yang jelas tanpa diwajibkan mengunduh presentasi besar terlebih dahulu.
- Kalender: status Upcoming, In progress, dan Completed; agenda mendatang didahulukan dan agenda selesai ditempatkan dalam disclosure. Memilih tanggal lampau tetap memperlihatkan kegiatannya langsung. Perhitungan hari tetap memakai Asia/Taipei.
- Responsif: hero ponsel tidak bertumpuk dengan kontrol, dan kalender halaman Academic Calendar tidak lagi melebar keluar panel. Susunan tabel sertifikat menyesuaikan layar kecil; tabel asli tetap dapat digeser di dalam areanya.
- Aksesibilitas: indikator fokus lebih terlihat, hitungan hasil sertifikat dibacakan melalui live region, serta Escape dari navigasi ponsel mengembalikan fokus ke tombol menu.
- Bahasa Inggris dan Mandarin Tradisional dibangun bersama. Label bidang studi diberi konteks bahwa nama resmi modul/kursus mengikuti dokumen kurikulum setiap angkatan.

## Saran evaluasi yang perlu disesuaikan

- **Halaman International Students terpisah:** kebutuhan informasinya benar; penambahan halaman baru tidak wajib. Admissions sekarang memiliki bagian khusus. URL international.html tetap redirect otomatis agar bookmark lama bekerja.
- **Pencarian dipindah ke header:** tombolnya sudah berada di header; posisi elemen dialog di bawah footer pada HTML bukan posisi tombol yang terlihat oleh pengguna.
- **Redirect halaman lama:** meta refresh dan location.replace sudah ada. Pemeriksaan proyek memastikan enam redirect Inggris/Mandarin tetap tersedia. Redirect HTTP permanen baru dapat diatur sesuai layanan hosting saat publikasi.
- **Timeline perlu detail:** penjelasan perubahan program dan nama sudah ada di panel tahun yang interaktif. Tidak perlu menambah sejarah yang belum terverifikasi.
- **Berita perlu tanggal:** mekanisme tampilan tanggal ditambahkan untuk rekaman yang memiliki publication_date. Rekaman berita terbaru pada ekspor ini belum menyediakan tanggal publikasi eksplisit. Tanggal kegiatan di poster tidak diubah menjadi tanggal publikasi.
- **Testimoni dan hasil mahasiswa:** tidak dibuat tanpa bukti. Cerita dan foto asli yang sudah tersedia dipertahankan.
- **Foto dosen dan kontak:** hanya foto, nama, serta profil yang sudah diverifikasi yang digunakan. Tidak membuat foto dosen sintetis atau mengklaim email masih aktif tanpa verifikasi.
- **Statistik karier:** tahun, jumlah lulusan, jumlah yang melaporkan status, serta kategori gabungan pekerjaan/pendidikan lanjut/wajib militer dipertahankan. Tidak mengubahnya menjadi employment rate.
- **Dokumen duplikat:** nama dokumen yang mirip tidak otomatis berarti file yang sama. Tidak menghapus tautan sumber tanpa bukti duplikasi.
- **Presentasi besar:** file PPTX asli tetap ditautkan dan ukuran yang dicantumkan penerbit tetap terlihat. Tidak mengklaim sudah mengompres atau mengonversi file tersebut. Versi PDF ringan memerlukan pengunduhan/konversi dan pemeriksaan tata letak tersendiri.
- **Stock photography:** label dan kredit ilustrasi tetap ada. Penggantian terbaik berikutnya adalah foto asli kegiatan kuliner/kerja sama yang sesuai konteks, bila tersedia dari pemilik situs.

## Sumber

- Evaluasi Website BMD.pdf yang diberikan pemilik situs, dibaca seluruhnya (9 halaman).
- Tabel sertifikat dan riwayat revisi: https://mdm.tcu.edu.tw/p/412-1021-5027.php?Lang=en serta rekaman lengkap dalam content/official-en/pages.json.
- Jalur internasional: https://oga.tcu.edu.tw/international-student/
- Beasiswa dan biaya: https://oga.tcu.edu.tw/scholarship/
- Tautan eksternal di atas ditinjau pada 8 November 2026. Persyaratan, tenggat, bahasa pengantar, dan keputusan beasiswa mengikuti publikasi universitas terbaru; tidak disalin menjadi janji pada website ini.

## Implementasi dan pemeriksaan

Sumber revisi: information_design.py, content/information-design.json, assets/information-design.css dan information-design.js. Kalender diperbarui dalam calendar_data.py, calendar-date.js, serta site.js. build.py dan localization.py mengintegrasikan revisi ke kedua bahasa.

Jalankan `python -X utf8 build.py` lalu `python -X utf8 run_checks.py`. Keenam pemeriksaan otomatis mencakup 326 halaman, tautan lokal, aset, tubuh publikasi, tabel asli, nama dosen, tautan magang, cerita foto, dan padanan bahasa. Pemeriksaan tambahan membandingkan 62 nama/poin sertifikat dengan publikasi serta menguji batas tanggal Taiwan.

Pemeriksaan browser menggunakan lebar 390, 768, dan 1440 piksel untuk Home, Certificate Requirements, Admissions, Academic Calendar, dan sertifikat Mandarin; 360 piksel juga diperiksa untuk hero. Pencarian dan filter sertifikat, kondisi tanpa hasil, pemilihan tanggal lampau, disclosure kegiatan selesai, navigasi ponsel/Escape, pencarian global, dan dialog cerita diperiksa langsung. Ini pengujian viewport browser, bukan pengujian ponsel fisik atau sertifikasi aksesibilitas menyeluruh. Playback YouTube, seluruh tautan eksternal bersejarah, dan pratinjau PPTX tidak disertifikasi ulang.

Preview lokal dijalankan dengan `python preview.py` (default port 4173). Sesi revisi menggunakan port 4174. Publikasi adalah langkah terpisah.

## Penyesuaian Tokyo sesuai referensi pemilik

Bagian Jepang tetap tertutup pada kunjungan biasa dan dibuka lewat ringkasan “Tokyo, day by day”. Saat dibuka, tampilan utama mempertahankan judul “Tokyo, from the inside”, foto kelompok besar, lokasi/tahun, dan strip Office hours seperti referensi pemilik. Empat tab pekerjaan memakai satu paragraf per topik; foto tambahan disusun dalam galeri ringkas. Keduanya berada dalam bagian “Work & photographs” yang tertutup secara default, sehingga halaman tidak kembali memanjang seperti sebelumnya.

Tautan langsung ke pekerjaan/komunitas membuka kedua lapisan yang diperlukan. Versi Mandarin mengikuti perubahan yang sama. Pembukaan ringkasan, tab Translation & media, tautan langsung ke komunitas, serta tampilan ponsel Mandarin dan desktop diperiksa di browser; keenam pemeriksaan proyek tetap lolos.

## Foto pilihan dari Google Drive pemilik

Tujuh foto dipilih dari empat album kegiatan Jepang: kerja dapur, briefing tim, latihan kebencanaan, dan budaya teh. Foto ini menggantikan gambar dapur yang sebelumnya sama di Life at BMD dan jurnal Tokyo, serta memberi kartu program dan ringkasan jurnal gambar tersendiri. Foto besar kelompok Tokyo yang disukai pemilik tetap berada pada pengantar utama.

Caption dan alt text Inggris/Mandarin mengikuti isi foto baru. Foto disimpan lokal sebagai WebP; tujuh berkas berjumlah sekitar 1,25 MB, sehingga pengunjung tidak perlu memuat gambar dari Drive. EXIF tidak disalin ke aset web. Provenans dicatat dalam content/japan-photo-selection.json; folder Drive lengkap tidak ditautkan dalam halaman publik.

Audit japan-photo-audit.json mencatat 10 foto Jepang yang berbeda, masing-masing digunakan sekali pada komposisi editorial Life at BMD dan Beyond Campus. Tampilan foto yang diperbesar serta padanan bahasa tetap menggunakan foto yang bersangkutan. Audit ini tidak mengklaim seluruh foto kampus, kartu berita, dan publikasi arsip di website sudah bebas pengulangan.

## Penggantian foto kampus berikutnya

Sesuai arahan pemilik, lima foto dari folder BMD menggantikan slot gambar yang sudah ada: baking pada Culinary Management, Yide Ri dan relawan RS Tzu Chi Taipei pada pembuka Life at BMD, serta hua dao/cha dao pada detail kreativitas di Introduction. Tidak ada halaman, galeri, modul, atau aset gambar web baru. Foto lama yang masih diperlukan oleh tab proyek memakai salinan kanonis yang sudah tersedia, sehingga foto bunga/teh tidak ikut muncul pada proyek akademik yang berbeda.

Caption dan alt text mengikuti foto serta konteks kegiatan dari pemilik; tidak menambahkan tanggal, nama orang, atau klaim hasil kegiatan. Audit terbaru mencakup 15 foto pilihan pemilik dan menghitung unit editorial di seluruh halaman Inggris, termasuk gambar yang berada di data popup. Masing-masing hanya ditempatkan pada satu unit; versi Mandarin dan pembesaran foto merupakan tampilan dari unit yang sama. Foto lain dalam folder tidak dipaksakan masuk.

## Pembaruan foto kampus — 13 November 2026

Sepuluh foto tambahan dari folder pemilik menggantikan gambar pada bagian yang sudah ada. Home memakai foto kedua yang dikonfirmasi pemilik sebagai Jianguo, serta foto dengan papan nama Jieren yang terlihat jelas. Foto ketiga komunitas BMD pada slideshow Home dipertahankan. Introduction memakai foto kelompok BMD dari koleksi pemilik; rasio tampilannya mengikuti foto agar seluruh kelompok terlihat.

Operations Management pada Home memakai mahasiswa yang sedang belajar dan menulis di kelas. Smart Business memakai foto lain di komputer perpustakaan. Pembuka Learning Directions memakai foto komputer perpustakaan yang berbeda, dengan caption yang menyebut lokasi tersebut secara akurat. Tab Operations Management menampilkan pengajaran di kelas; tab Culinary Management memakai foto praktik baking tersendiri. Baking bersama yang sudah dipasang tetap menjadi foto Culinary pada Home.

Ideas into practice memakai suasana kelas yang berbeda. Ideas into action memakai kelompok relawan RS Tzu Chi Taipei; foto ini dipindahkan dari pembuka Student Life agar tidak berulang. Pembuka Student Life kini memakai foto gedung rumah sakit dari kunjungan yang sama. Seluruh caption, alt text, kredit foto kampus, dan pergantian caption interaktif diperbarui dalam bahasa Inggris/Mandarin Tradisional.

Foto UK summer study, Mao Mao Xiaoyin, Whisper Tour, presentasi mahasiswa, serta Sustainable Innovation/Grace menunggu pilihan berikutnya dari pemilik. Penggantian Workplace Learning juga menunggu kejelasan foto ZY campus. Foto dan konteks lama yang terkait bagian tersebut tetap dipertahankan sementara, sesuai balasan pemilik.

Tidak ada halaman, galeri, atau bagian baru. Delapan aset WebP tambahan diperlukan untuk menyimpan foto yang berbeda tanpa menimpa foto kanonis pada publikasi lama; dua berkas gambar yang hanya dipakai oleh slot terkait diganti langsung. Aset web dioptimalkan dan tidak membawa EXIF. Provenans lengkap tercatat dalam content/japan-photo-selection.json.

Keenam pemeriksaan proyek lolos pada 326 halaman. Audit foto kini mencakup 25 foto Jepang/kampus pilihan, termasuk data popup dan tab dinamis: masing-masing memiliki satu penempatan editorial; padanan bahasa dan pembesaran berbagi foto yang sama. Foto berita dan publikasi arsip lama berada di luar klaim ini.

Pemeriksaan browser mencakup foto Home, popup Operations/Smart Business, Introduction, tab Culinary Management Inggris/Mandarin, serta viewer Student Life. Tampilan desktop 1280 piksel dan ponsel 390 piksel diperiksa. Lebar bingkai foto Ideas into action diperbaiki agar mengikuti layar ponsel; foto kelompok ditampilkan utuh. Preview berjalan di http://127.0.0.1:4174/. Folder yang sama dibuka di Visual Studio Code; website online belum dipublikasikan ulang.

## Foto Jepang mengikuti tab yang sudah ada

Sesuai koreksi pemilik, galeri terpisah “Work, service & culture” digabung ke empat tab kerja yang sudah ada. Service & operations menampilkan foto dapur serta kunjungan komunitas; Culture & independence menampilkan latihan darurat dan teh. Foto pertemuan relawan yang sebelumnya berada di samping semua tab kini hanya muncul pada Office & finance, dengan caption aslinya. Translation & media tetap berupa uraian singkat karena koleksi foto yang dipilih belum memuat kegiatan penerjemahan. Tidak ada foto baru, salinan gambar tambahan, halaman baru, atau galeri terpisah.

Foto yang diperbesar tetap memakai viewer yang sama. Tautan lama #intern-service membuka tab Service beserta kedua lapisan ringkasan. Versi Mandarin memakai struktur yang sama. Enam pemeriksaan proyek dan audit 25 foto pilihan lolos; perpindahan tab, navigasi keyboard, viewer foto, tautan langsung, serta tampilan Mandarin pada lebar 390 piksel diperiksa di browser. Kode tersimpan pada folder proyek yang sama dengan Visual Studio Code.

## Satu foto untuk masing-masing tab Jepang

Arahan terbaru pemilik menggantikan susunan berpasangan: kini keempat tab masing-masing memiliki tepat satu foto berbeda. Office & finance memakai pertemuan relawan; Translation & media memakai foto kegiatan komunikasi kelompok yang dipilih dari album 小築活動 milik pemilik; Service & operations memakai dapur; Culture & independence memakai teh. Caption foto komunikasi menjelaskan konteks kegiatan komunitas, tanpa menyatakan bahwa foto tersebut memperlihatkan pekerjaan penerjemahan atau penyuntingan subtitle.

Foto kunjungan rumah dan latihan darurat dipensiunkan dari tampilan tab. Tidak ada galeri tambahan. Berkas foto kunjungan yang tidak lagi digunakan diganti dan dinamai communication-activity.webp agar browser memuat pilihan baru; jumlah aset gambar web tetap sama. Alt text, caption Inggris/Mandarin, viewer, dan data penempatan foto diperbarui bersama.

Semua enam pemeriksaan lolos, termasuk pemeriksaan tepat satu foto per panel dalam kedua bahasa. Audit terbaru mencakup 24 foto pilihan yang masih aktif, masing-masing satu penempatan. Empat tab dan pembesaran foto diperiksa pada desktop; tab komunikasi Mandarin juga diperiksa pada lebar 390 piksel tanpa overflow. Perubahan berada di proyek lokal yang sama dengan Visual Studio Code.

## 貓貓小飲 — 14 November 2026

Foto yang dilampirkan pemilik menggantikan foto utama food stall pada bagian Student Life yang sudah ada. Nama dikonfirmasi sebagai 貓貓小飲 / Mao Mao Xiao Yin. Caption, alt text, judul singkat bagian, serta uraian Inggris/Mandarin mengikuti nama dan isi foto. Foto baru hanya ditempatkan sekali; viewer memperbesar gambar yang sama.

Tanggal dan tujuan amal foto baru belum diberikan, sehingga foto tidak diberi atribusi acara援緬 2025. Dua foto arsip lain dalam kolase tetap berlabel jelas sebagai Myanmar-relief fair 2025 dan memiliki tautan laporan asal. Foto asli pada berita dan publikasi dipertahankan. Satu aset WebP khusus ditambahkan agar foto pemilik tidak ikut berulang pada Home dan Introduction yang masih memakai foto arsip lama.

Keenam pemeriksaan proyek dan audit 25 foto pilihan lolos. Foto utama, caption, pembesaran foto, serta versi Mandarin pada lebar 390 piksel diperiksa di browser tanpa overflow. Aset dioptimalkan menjadi 287.548 byte tanpa EXIF. Preview lokal dan proyek Visual Studio Code diperbarui; publikasi online tetap terpisah.
