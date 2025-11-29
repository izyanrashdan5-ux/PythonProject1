Izyan Rashdan (10)(X-2)
Darrell Faiq Athallah Maulana (7)(x-2)
Muhammad Yusuf Pradyanto (24)(X-1)
## 1. Cara Menjalankan

1. Simpan kode kamu ke dalam sebuah file, misalnya:
    
    ```
    test.py
    
    ```
    
2. Buka **terminal / command prompt** di folder tempat file itu disimpan.
3. Jalankan:
    
    ```bash
    python test.py
    
    ```
    
    atau kalau di komputer kamu pakai `python`:
    
    ```bash
    python game_2048.py
    
    ```
    
4. Jendela game 2048 akan muncul.
    
    Kamu bisa main pakai:
    
    - Tombol panah di **keyboard** (`↑`, `↓`, `←`, `→`)
    - Tombol panah di **layar** (GUI)
    - Tombol **Restart** buat mulai ulang

---

## 2. Representasi Papan (Grid)

Papan game disimpan di variabel:

```python
self.grid = [[0] * SIZE for _ in range(SIZE)]

```

- `SIZE = 4` → papan berukuran **4x4**.
- `self.grid` adalah **list 2D**, contohnya:
    
    ```python
    [
        [0, 2, 0, 2],
        [4, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0],
    ]
    
    ```
    
- Setiap angka berarti:
    - `0` → sel kosong
    - `2, 4, 8, 16, ...` → nilai tile

---

## 3. Alur Game Satu Langkah

Setiap kali pemain menekan arah (kiri/kanan/atas/bawah), alurnya kira-kira:

1. **Baca semua baris/kolom** sesuai arah gerakan
2. **Geser & gabungkan tile** yang nilainya sama (pakai fungsi `merge_line`)
3. Jika ada perubahan di papan:
    - Tambahkan **1 tile baru** (2 atau 4) secara acak di sel kosong (`add_random_tile`)
    - Update tampilan
    - Cek apakah **game over** (`is_game_over`)
4. Kalau tidak ada perubahan, tidak dilakukan apa-apa (tidak spawn tile baru)

---

## 4. Logika Tambah Tile Baru (`add_random_tile`)

```python
def add_random_tile(self):
    empty_cells = [
        (r, c)
        for r in range(SIZE)
        for c in range(SIZE)
        if self.grid[r][c] == 0
    ]
    if not empty_cells:
        return

    r, c = random.choice(empty_cells)
    # 90% muncul 2, 10% muncul 4
    self.grid[r][c] = 4 if random.random() < 0.1 else 2

```

Intinya:

1. Cari semua posisi yang masih `0` (kosong).
2. Pilih satu posisi secara acak.
3. Isi dengan:
    - `2` (90% kemungkinan)
    - `4` (10% kemungkinan)

Tile baru ini hanya muncul **kalau ada gerakan yang valid** (papan bener-bener berubah).

---

## 5. Logika Merge Satu Baris (`merge_line`)

Ini jantung logika 2048 di kode ini.

```python
def merge_line(self, line):
    # Buang semua 0
    non_zero = [v for v in line if v != 0]

    new_line = []
    i = 0
    while i < len(non_zero):
        # Jika dua angka berurutan sama, gabungkan
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            new_line.append(non_zero[i] * 2)
            i += 2  # lompat 2 karena sudah digabung
        else:
            new_line.append(non_zero[i])
            i += 1

    # Tambah 0 di belakang sampai panjangnya 4
    while len(new_line) < SIZE:
        new_line.append(0)

    return new_line

```

Cara kerjanya (contoh step-by-step):

### Contoh 1

Input:

```python
line = [2, 0, 2, 4]

```

1. Buang nol:
    
    ```python
    non_zero = [2, 2, 4]
    
    ```
    
2. Proses merge dari kiri ke kanan:
    - `2` dan `2` sama → digabung jadi `4`
    - `4` di belakangnya tidak punya pasangan yang sama → tetap `4`
    
    Hasil sementara:
    
    ```python
    new_line = [4, 4]
    
    ```
    
3. Tambah nol di belakang sampai panjang 4:
    
    ```python
    new_line = [4, 4, 0, 0]
    
    ```
    

Output:

`[4, 4, 0, 0]`

---

### Contoh 2

Input:

```python
line = [2, 2, 2, 2]

```

1. Buang nol (tidak ada):
    
    ```python
    non_zero = [2, 2, 2, 2]
    
    ```
    
2. Merge:
    - `2` + `2` → `4`
    - lanjut ke angka berikutnya:
    - `2` + `2` → `4`
    
    Hasil sementara:
    
    ```python
    new_line = [4, 4]
    
    ```
    
3. Tambah nol:
    
    ```python
    new_line = [4, 4, 0, 0]
    
    ```
    

Perhatikan: **Merge hanya sekali per pasangan** — ini sesuai aturan resmi game 2048.

---

## 6. Logika Gerak ke Kiri, Kanan, Atas, Bawah

Semua gerakan memakai **fungsi yang sama** (`merge_line`), hanya cara baca baris/kolomnya yang beda.

### 6.1. Gerak Kiri (`move_left`)

```python
def move_left(self):
    moved = False
    new_grid = []

    for r in range(SIZE):
        line = self.grid[r]           # ambil 1 baris apa adanya
        merged = self.merge_line(line)
        if merged != line:
            moved = True              # berarti ada perubahan
        new_grid.append(merged)

    if moved:
        self.grid = new_grid
        self.after_move()

```

- Ambil setiap baris
- Merge seolah-olah digeser ke kiri
- Kalau ada baris yang berubah → anggap gerakan valid
- Setelah itu tambahkan tile baru dan cek game over (`after_move`)

---

### 6.2. Gerak Kanan (`move_right`)

```python
def move_right(self):
    moved = False
    new_grid = []

    for r in range(SIZE):
        # Balik baris, merge seolah-olah ke kiri, lalu balik lagi
        line = list(reversed(self.grid[r]))
        merged = self.merge_line(line)
        merged = list(reversed(merged))

        if merged != self.grid[r]:
            moved = True
        new_grid.append(merged)

    if moved:
        self.grid = new_grid
        self.after_move()

```

Trik:

1. Balik baris → misalnya `[2, 0, 2, 4]` jadi `[4, 2, 0, 2]`
2. Jalankan `merge_line` (arah kiri)
3. Balik lagi hasilnya supaya jadi arah kanan

Dengan cara ini, kita **nggak perlu** nulis fungsi merge khusus buat kanan.

---

### 6.3. Gerak Atas (`move_up`)

```python
def move_up(self):
    moved = False
    new_grid = [row[:] for row in self.grid]  # salin isi grid

    for c in range(SIZE):
        line = [self.grid[r][c] for r in range(SIZE)]  # ambil 1 kolom dari atas ke bawah
        merged = self.merge_line(line)
        for r in range(SIZE):
            if new_grid[r][c] != merged[r]:
                moved = True
            new_grid[r][c] = merged[r]

    if moved:
        self.grid = new_grid
        self.after_move()

```

- Kolom diambil dari **atas ke bawah**
- Di-merge pakai `merge_line` (anggap gerak ke atas)
- Hasilnya dikembalikan ke kolom yang sama

---

### 6.4. Gerak Bawah (`move_down`)

```python
def move_down(self):
    moved = False
    new_grid = [row[:] for row in self.grid]

    for c in range(SIZE):
        # Ambil kolom dari bawah ke atas
        line = [self.grid[r][c] for r in range(SIZE - 1, -1, -1)]
        merged = self.merge_line(line)
        # Balik lagi supaya posisi dari atas ke bawah
        merged = list(reversed(merged))

        for r in range(SIZE):
            if new_grid[r][c] != merged[r]:
                moved = True
            new_grid[r][c] = merged[r]

    if moved:
        self.grid = new_grid
        self.after_move()

```

Trik sama seperti kanan:

1. Kolom dibaca dari **bawah ke atas**
2. Merge seolah-olah ke “atas”
3. Hasil dibalik lagi dan ditaruh ke atas-bawah

---

## 7. Setelah Gerakan: `after_move`

```python
def after_move(self):
    self.add_random_tile()
    self.update_gui()
    if self.is_game_over():
        messagebox.showinfo("Game Over", "Tidak ada langkah lagi. Game selesai!")

```

Setelah gerakan yang valid:

1. Tambah satu tile baru (`add_random_tile`)
2. Update tampilan (`update_gui`)
3. Cek apakah game buntu (`is_game_over`)

---

## 8. Logika Game Over (`is_game_over`)

```python
def is_game_over(self):
    # Masih ada sel kosong? berarti belum game over
    for r in range(SIZE):
        for c in range(SIZE):
            if self.grid[r][c] == 0:
                return False

    # Cek horizontal (kiri-kanan)
    for r in range(SIZE):
        for c in range(SIZE - 1):
            if self.grid[r][c] == self.grid[r][c + 1]:
                return False

    # Cek vertikal (atas-bawah)
    for c in range(SIZE):
        for r in range(SIZE - 1):
            if self.grid[r][c] == self.grid[r + 1][c]:
                return False

    # Kalau lolos semua cek di atas, berarti bener-bener mentok
    return True

```

Game dianggap **selesai (kalah)** kalau:

1. **Tidak ada sel kosong** (tidak ada `0` sama sekali)
2. **Tidak ada dua tile bertetangga yang nilainya sama**:
    - Dicek kiri-kanan
    - Dicek atas-bawah

Kalau kedua syarat dipenuhi → benar-benar tidak ada langkah lagi → `Game Over`.
