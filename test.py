import tkinter as tk
from tkinter import messagebox
import random

# --- KONSTAN / PENGATURAN DASAR ---
SIZE = 4  # ukuran papan 4x4
FONT = ("Helvetica", 24, "bold")
BACKGROUND_COLOR = "#BBADA0"
EMPTY_CELL_COLOR = "#CDC1B4"

# Warna tile (boleh diubah sesuka hati)
TILE_COLORS = {
    0: "#CDC1B4",
    2: "#EEE4DA",
    4: "#EDE0C8",
    8: "#F2B179",
    16: "#F59563",
    32: "#F67C5F",
    64: "#F65E3B",
    128: "#EDCF72",
    256: "#EDCC61",
    512: "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22E",
}

TEXT_COLORS = {
    2: "#776E65",
    4: "#776E65",
}


class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Sederhana")

        # Papan (data) 4x4, isi angka. 0 artinya kosong.
        self.grid = [[0] * SIZE for _ in range(SIZE)]

        # Frame utama untuk papan
        main_frame = tk.Frame(root, bg=BACKGROUND_COLOR, bd=10)
        main_frame.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        # Label 4x4 untuk tampilan tile di GUI
        self.cells = []
        for r in range(SIZE):
            row_cells = []
            for c in range(SIZE):
                lbl = tk.Label(
                    main_frame,
                    text="",
                    width=4,
                    height=2,
                    font=FONT,
                    bg=EMPTY_CELL_COLOR,
                    fg="#776E65",
                    bd=3,
                    relief="ridge",
                    justify="center",
                )
                lbl.grid(row=r, column=c, padx=5, pady=5)
                row_cells.append(lbl)
            self.cells.append(row_cells)

        # Frame untuk tombol arah & tombol restart
        buttons_frame = tk.Frame(root)
        buttons_frame.grid(row=1, column=0, pady=10)

        btn_up = tk.Button(buttons_frame, text="↑", width=5, command=self.move_up)
        btn_left = tk.Button(buttons_frame, text="←", width=5, command=self.move_left)
        btn_right = tk.Button(buttons_frame, text="→", width=5, command=self.move_right)
        btn_down = tk.Button(buttons_frame, text="↓", width=5, command=self.move_down)
        btn_reset = tk.Button(buttons_frame, text="Restart", width=10, command=self.init_game)

        # Posisi tombol
        btn_up.grid(row=0, column=1)
        btn_left.grid(row=1, column=0)
        btn_down.grid(row=1, column=1)
        btn_right.grid(row=1, column=2)
        btn_reset.grid(row=2, column=0, columnspan=3, pady=(10, 0))

        # Biar bisa pakai keyboard arah juga
        root.bind("<Up>", lambda event: self.move_up())
        root.bind("<Down>", lambda event: self.move_down())
        root.bind("<Left>", lambda event: self.move_left())
        root.bind("<Right>", lambda event: self.move_right())

        # Mulai game
        self.init_game()

    # ================= LOGIKA GAME ================= #

    def init_game(self):
        """Reset papan jadi kosong lalu tambah 2 tile awal."""
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.add_random_tile()
        self.add_random_tile()
        self.update_gui()

    def add_random_tile(self):
        """Menambahkan tile baru (2 atau kadang 4) pada posisi kosong secara acak."""
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

    def update_gui(self):
        """Meng-update tampilan label sesuai isi 'grid'."""
        for r in range(SIZE):
            for c in range(SIZE):
                value = self.grid[r][c]
                lbl = self.cells[r][c]

                if value == 0:
                    lbl.config(text="", bg=EMPTY_CELL_COLOR, fg="#776E65")
                else:
                    bg_color = TILE_COLORS.get(value, "#3C3A32")
                    if value in TEXT_COLORS:
                        fg_color = TEXT_COLORS[value]
                    else:
                        fg_color = "#F9F6F2"

                    lbl.config(
                        text=str(value),
                        bg=bg_color,
                        fg=fg_color,
                    )

        # Paksa tkinter menggambar ulang
        self.root.update_idletasks()

    def merge_line(self, line):
        """
        Menerima 1 baris (list panjang 4).
        Contoh line: [2, 0, 2, 4]
        1. Buang 0 -> [2, 2, 4]
        2. Gabungkan angka yang sama sekali saja ->
           [4, 4]
        3. Tambah 0 di belakang sampai panjang 4 -> [4, 4, 0, 0]
        """
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

    # ---------- GERAK KIRI ---------- #
    def move_left(self):
        moved = False
        new_grid = []

        for r in range(SIZE):
            line = self.grid[r]
            merged = self.merge_line(line)
            if merged != line:
                moved = True
            new_grid.append(merged)

        if moved:
            self.grid = new_grid
            self.after_move()

    # ---------- GERAK KANAN ---------- #
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

    # ---------- GERAK ATAS ---------- #
    def move_up(self):
        moved = False
        new_grid = [row[:] for row in self.grid]  # salin isi grid

        for c in range(SIZE):
            line = [self.grid[r][c] for r in range(SIZE)]  # ambil 1 kolom
            merged = self.merge_line(line)
            for r in range(SIZE):
                if new_grid[r][c] != merged[r]:
                    moved = True
                new_grid[r][c] = merged[r]

        if moved:
            self.grid = new_grid
            self.after_move()

    # ---------- GERAK BAWAH ---------- #
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

    def after_move(self):
        """Dipanggil setelah ada gerakan valid (papan berubah)."""
        self.add_random_tile()
        self.update_gui()
        if self.is_game_over():
            messagebox.showinfo("Game Over", "Tidak ada langkah lagi. Game selesai!")

    def is_game_over(self):
        """
        Game over jika:
        1. Tidak ada sel kosong (tidak ada 0)
        2. Tidak ada dua tile bertetangga (atas/bawah/kiri/kanan) yang nilainya sama
        """
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

        # Kalau lolos cek di atas, berarti bener-bener mentok
        return True


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()