import json
from pathlib import Path


def muat(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def terpenuhi(aturan, memori):
    """mode "dan" = semua ada di memori, "atau" = salah satu ada,
    "tidak" = tidak satu pun ada (hanya untuk fakta dasar yang sudah dijawab)."""
    if aturan["mode"] == "tidak":
        return not any(k in memori for k in aturan["jika"])
    cek = all if aturan["mode"] == "dan" else any
    return cek(k in memori for k in aturan["jika"])


def fakta_dasar(aturan):
    """Fakta yang ditanyakan ke user: muncul di 'jika' tetapi bukan hasil aturan mana pun."""
    hasil = {r["maka"] for r in aturan}
    urut = []
    for r in aturan:
        for k in r["jika"]:
            if k not in hasil and k not in urut:
                urut.append(k)
    return urut


def tanya(fakta):
    """Tanya y/t untuk tiap fakta dasar; kembalikan daftar fakta yang dijawab 'y'."""
    print("Jawab y/t.")
    memori = []
    for i, f in enumerate(fakta, 1):
        while True:
            jawab = input(f"{i}. Apakah {f}? (y/t) > ").strip().lower()
            if jawab in ("y", "ya"):
                jawab = "y"
                break
            if jawab in ("t", "tidak", "n"):
                jawab = "t"
                break
            print("   Jawab dengan y atau t.")
        if jawab == "y":
            memori.append(f)
    return memori


def bertentangan(fakta_awal):
    """Satu faktor (elevasi, suhu, lereng, pH) hanya boleh punya satu kelas.
    Kembalikan faktor yang dijawab 'y' pada lebih dari satu kelas."""
    per_faktor = {}
    for f in fakta_awal:
        per_faktor.setdefault(f.split()[0], []).append(f)
    return {k: v for k, v in per_faktor.items() if len(v) > 1}


def forward_chaining(aturan, fakta_awal):
    """Sesuai pseudocode: ulangi ambil aturan pertama yang syaratnya terpenuhi
    dan hasilnya belum ada di memori, tambahkan hasilnya, catat jejaknya."""
    memori = list(fakta_awal)
    jejak = {}  # fakta hasil -> (id aturan, kondisi yang terpenuhi)
    siklus = 0
    while True:
        cocok = [r for r in aturan if r["maka"] not in memori and terpenuhi(r, memori)]
        siklus += 1
        if not cocok:
            print(f"Siklus {siklus}: tidak ada aturan baru, berhenti")
            break
        r = cocok[0]
        if r["mode"] == "tidak":
            kond = ["tidak ada yang dijawab y: " + "; ".join(r["jika"])]
        else:
            kond = [k for k in r["jika"] if k in memori]
        jejak[r["maka"]] = (r["id"], kond)
        memori.append(r["maka"])
        print(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
    return memori, jejak


def jelaskan(nama, jejak, indent=1, sudah=None):
    """Telusuri alasan sebuah fakta sampai ke fakta awal."""
    sudah = set() if sudah is None else sudah
    pad = "  " * indent
    id_r, kondisi = jejak[nama]
    if nama in sudah:
        return [f"{pad}{nama}  (sudah dijelaskan di atas)"]
    sudah.add(nama)
    baris = [f"{pad}{nama}  <- {id_r} ({', '.join(kondisi)})"]
    for k in kondisi:
        if k in jejak:
            baris += jelaskan(k, jejak, indent + 1, sudah)
    return baris


def main():
    data = muat(Path(__file__).parent / "rules.json")
    aturan = data["aturan"]

    print(data["judul"])
    fakta_awal = tanya(fakta_dasar(aturan))

    print("\nFakta awal:", ", ".join(fakta_awal) if fakta_awal else "(tidak ada)")
    print()
    konflik = bertentangan(fakta_awal)
    if konflik:
        print("Jawaban bertentangan: satu faktor hanya boleh punya satu kelas.")
        for faktor, kelas in konflik.items():
            print(f"  {faktor}: " + " | ".join(kelas))
        print("Inferensi tidak dijalankan.")
        memori, jejak = list(fakta_awal), {}
    else:
        memori, jejak = forward_chaining(aturan, fakta_awal)

    dipakai = {k for r in aturan for k in r["jika"]}
    kesimpulan = [f for f in jejak if f not in dipakai]  # hasil akhir, tidak dipakai aturan lain

    print()
    if not kesimpulan:
        print("Kesimpulan: tidak ada kesimpulan yang dapat ditarik dari fakta tersebut")
    for n, k in enumerate(kesimpulan, 1):
        label = "Kesimpulan" if len(kesimpulan) == 1 else f"Kesimpulan {n}"
        print(f"{label}: {k}")
        print("Alasan:")
        print("\n".join(jelaskan(k, jejak)))
        print()

    print("Catatan:", data["batas"])


if __name__ == "__main__":
    main()