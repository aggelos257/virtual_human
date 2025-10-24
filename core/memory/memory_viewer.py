# ==========================================================
# tools/memory_viewer.py
# Επαγγελματικό εργαλείο προβολής και διαχείρισης μνήμης Ζένιας
# - Προβολή facts / interactions / προφίλ / προτιμήσεων
# - Αναζήτηση με embeddings ή TF-IDF ή keyword fallback
# - Εξαγωγή / Διαγραφή / Backup
# ==========================================================
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Προσθήκη ρίζας project για σωστά imports
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from core.memory.memory_manager import MemoryManager


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def divider(title: str = ""):
    print("=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)


def show_interactions(mem: MemoryManager, limit: int = 20):
    divider(f"🗣️ Τελευταίες {limit} συνομιλίες")
    data = mem.get_recent(limit)
    if not data:
        print("(Καμία συνομιλία αποθηκευμένη ακόμα.)")
        return
    for d in data:
        print(f"[{d['ts']}] ({d['role']}) → {d['text']}")
    print()


def show_facts(mem: MemoryManager, limit: int = 20):
    divider(f"💾 Γεγονότα / Μνήμες (έως {limit})")
    facts = mem.list_facts(limit)
    if not facts:
        print("(Καμία αποθηκευμένη μνήμη ακόμα.)")
        return
    for f in facts:
        ts = f['ts']
        txt = f['text']
        w = f.get('weight', 0.0)
        tags = ", ".join(f.get('tags', []))
        print(f"[{ts}] ({w:.2f}) {txt}")
        if tags:
            print(f"   Tags: {tags}")
    print()


def show_profile(mem: MemoryManager):
    divider("👤 Προφίλ Χρήστη")
    name = mem.get_user_name() or "(Άγνωστο)"
    print(f"Όνομα: {name}")

    cur = mem._exec("SELECT key, value, updated_at FROM profile")
    rows = cur.fetchall()
    if len(rows) > 1:
        print("\nΆλλα στοιχεία προφίλ:")
        for k, v, ts in rows:
            if k == "user_name":
                continue
            try:
                val = json.loads(v)
            except Exception:
                val = v
            print(f" - {k}: {val} (τελευταία ενημέρωση {ts})")
    print()


def show_preferences(mem: MemoryManager):
    divider("⚙️ Προτιμήσεις Χρήστη")
    cur = mem._exec("SELECT key, value, updated_at FROM preferences")
    rows = cur.fetchall()
    if not rows:
        print("(Δεν υπάρχουν αποθηκευμένες προτιμήσεις.)")
        return
    for k, v, ts in rows:
        try:
            val = json.loads(v)
        except Exception:
            val = v
        print(f"- {k}: {val} (τελευταία ενημέρωση {ts})")
    print()


def search_memories(mem: MemoryManager):
    query = input("🔎 Ερώτημα αναζήτησης: ").strip()
    if not query:
        return
    divider(f"Αποτελέσματα αναζήτησης για: {query}")
    hits = mem.search(query=query, top_k=10)
    if not hits:
        print("(Δεν βρέθηκαν αποτελέσματα.)")
        return
    for h in hits:
        kind = h.get("kind", "?")
        score = h.get("score", 0.0)
        text = h.get("text", "")
        ts = h.get("ts", "")
        print(f"[{kind.upper()} | {score:.2f} | {ts}] {text}")
    print()


def export_memory(mem: MemoryManager):
    out_dir = BASE_DIR / "data"
    out_dir.mkdir(exist_ok=True)
    filename = f"zenia_memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path = out_dir / filename
    mem.export_json(str(out_path))
    print(f"✅ Εξαγωγή ολοκληρώθηκε: {out_path}")


def delete_all(mem: MemoryManager):
    confirm = input("⚠️ Θέλεις να διαγράψεις ΟΛΗ τη μνήμη; (ναι/όχι): ").strip().lower()
    if confirm in ("ναι", "yes", "y"):
        mem.wipe_all(confirm=True)
    else:
        print("❎ Ακύρωση διαγραφής.")


def main():
    mem = MemoryManager()
    while True:
        clear_console()
        print("🧠  ZENIA MEMORY VIEWER")
        print("=" * 70)
        print("1️⃣  Προβολή πρόσφατων συνομιλιών")
        print("2️⃣  Προβολή γεγονότων (facts)")
        print("3️⃣  Προβολή προφίλ")
        print("4️⃣  Προβολή προτιμήσεων")
        print("5️⃣  Αναζήτηση στη μνήμη")
        print("6️⃣  Εξαγωγή/Backup")
        print("7️⃣  Διαγραφή όλων των δεδομένων")
        print("0️⃣  Έξοδος")
        print("=" * 70)

        choice = input("Επιλογή: ").strip()
        clear_console()

        if choice == "1":
            show_interactions(mem)
        elif choice == "2":
            show_facts(mem)
        elif choice == "3":
            show_profile(mem)
        elif choice == "4":
            show_preferences(mem)
        elif choice == "5":
            search_memories(mem)
        elif choice == "6":
            export_memory(mem)
        elif choice == "7":
            delete_all(mem)
        elif choice == "0":
            print("👋 Έξοδος από το Memory Viewer.")
            break
        else:
            print("Μη έγκυρη επιλογή.")

        input("\nΠάτησε Enter για συνέχεια...")


if __name__ == "__main__":
    main()
