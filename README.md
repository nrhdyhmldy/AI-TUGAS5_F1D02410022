# AI-TUGAS5_F1D02410022
## SISTEM PAKAR EVALUASI KESESUAIAN LAHAN KOPI ARABIKA MENGGUNAKAN FORWARD CHAINING

### Topik
Menilai kelas kesesuaian lahan untuk tanaman kopi arabika (S1 sangat sesuai, S1 cukup sesuai,
S3 sesuai marginal, N tidak sesuai) dari empat masukan yaitu ketinggian tempat, suhu udara, kemiringan lereng,
dan pH tanah, lalu memberi rekomendasi perbaikan.

### Sumber Jurnal
[1]  Wardani, N. R., Putra, D. F., & Supriyanto, A. Evaluasi Kesesuaian Lahan Kopi di Wilayah Giripurno
     Kota Batu Jawa Timur. Jurnal Swarnabhumi, Vol. 9 No. 1, Agustus 2024.
     Tabel 2 dipakai sebagai kriteria kelas tiap faktor.
     https://jurnal.univpgri-palembang.ac.id/index.php/swarna/article/view/10961/8701

[2]  Syahrul, Amir, & Saida. Evaluasi Kesesuaian Lahan untuk Pengembangan Tanaman Kopi Arabika
     (Coffea arabica L.) di Kecamatan Bungaya, Kabupaten Gowa. Jurnal AGrotekMAS (UMI). 
     Dipakai untuk usulan perbaikan (naungan, teras, serbuk belerang) dan prinsip faktor pembatas.
     https://jurnal.fp.umi.ac.id/index.php/agrotekmas/article/download/191/167

### Kriteria Kelas Arabika
| Faktor | S1 | S2 | S3 | N |
| :--- | :--- | :--- | :--- | :--- |
| Ketinggian (m dpl) | 1000-1500 | 850-1000; 1500-1750 | 650-850; 1750-2000 | <650; >2000 |
| Suhu (C) | 20-24 | 24-28 | 18-20; 28-32 | <18; >32 |
| Lereng (%) | 0-8 | 8-25 | 25-45 | >45 |
| pH tanah | 5,5-6,0 | 6,1-7,0; 5,0-5,4 | 7,1-8,0; 4,0-4,9 | >8,0; <4,0 |

Asumsi batas: batas bawah masuk ke kelas itu, batas atas masuk kelas berikutnya (interval[bawah, atas])

### Aturan (24 aturan, 7 kemungkinan kesimpulan)
* R1-R16: nilai mentah menjadi kelas per faktor (kelas_elevasi, kelas_suhu, kelas_lereng, kelas_ph).
* R17: aturan berantai yang memakai hasil R1-R16: kelas_lahan = kelas terburuk dari keempat faktor (hukum faktor pembatas).
* R18-R21: kelas_lahan menjadi kesimpulan (S1, S2, S3, atau N). Rantai 3 tingkat: nilai mentah -> kelas faktor -> kelas lahan -> kesimpulan.
* R22-R24: rekomendasi naungan (suhu), teras (R23 memakai hasil kelas_lereng), dan serbuk belerang (pH tinggi).

### Algoritma Forward Chaining:
1. Mulai dari fakta masukan.
2. Cari aturan yang semua syaratnya terpenuhi dan hasilnya belum ada.
3. Jalankan aturan, tambahkan hasilnya sebagai fakta baru, catat jejaknya.
4. Ulangi sampai tidak ada aturan baru yang menyala.
5. Tampilkan kesimpulan, lalu telusuri jejak mundur sebagai alasan beserta sumbernya.

### Batasan
* Curah hujan, bulan kering, kedalaman efektif, dan drainase tidak dimasukkan karena batas kelasnya di tabel sumber kurang jelas/tumpang tindih.
* Kriteria suhu dan pH pada S1 dan S2 berbeda; kelas memakai S1, S2 hanya untuk usulan perbaikan.
* Rekomendasi bersifat umum, bukan pengganti uji tanah lapangan.
