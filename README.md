# Directory Finder

**Indonesia:** Ini adalah alat untuk mencari direktori dari sebuah situs web dengan metode brute force menggunakan wordlist. Alat ini dapat menemukan file tersembunyi yang sulit ditemukan secara manual di situs web!

## Fitur

- Pencarian direktori dengan metode brute force menggunakan wordlist.
- Kemampuan menggunakan user agent acak untuk setiap permintaan.
- Pilihan antara menggunakan tanggal kalender default atau acak pada URL.
- Dukungan multi-threading untuk pemindaian yang lebih cepat.
- Dukungan proxy, dengan opsi menggunakan proxy acak.

## Memulai

1. Clone repository:

    ```bash
    hhh
    ```

2. Install dependensi:

    ```bash
    hhhh
    ```

3. Jalankan alat dengan parameter yang diinginkan:

    ```bash
    python pencari_direktori.py -u [url_target] -t [timeout] -l [path_wordlist] -s [nama_file_simpan] -v -th [threads] -p [proxy]
    ```

## Penggunaan

- `-u`, `--url`: Tentukan URL situs web target.
- `-t`, `--timeout`: Atur waktu habis untuk setiap permintaan dalam detik.
- `-l`, `--wordlist`: Berikan path ke file wordlist.
- `-s`, `--save`: Tentukan nama file untuk menyimpan hasil.
- `-v`, `--verbose`: Aktifkan output detail, termasuk error 404.
- `-th`, `--threads`: Atur jumlah thread untuk multi-threading (1-20 untuk kinerja optimal).
- `-p`, `--proxy`: Tentukan proxy (contoh: `http://alamatip:port`) atau gunakan "random" untuk proxy acak.

Bebas untuk berkontribusi atau melaporkan masalah!

**Disclaimer:** Gunakan alat ini dengan bijak dan hanya pada situs web di mana Anda memiliki izin untuk melakukan pemindaian direktori.

## Kredit

Dibuat dengan ❤️ oleh [adit624] or [bjorki199]
