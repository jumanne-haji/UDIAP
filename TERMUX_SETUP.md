# UDIAP – Kuendesha kwenye Termux (Android)

Maelekezo kamili ya kuendesha UDIAP **bila computer**, kutumia Termux tu.

---

## 1. Install packages muhimu

Fungua Termux na andika:

```bash
pkg update -y && pkg upgrade -y
pkg install -y python nodejs git clang make libffi openssl
```

(Inachukua muda kidogo)

---

## 2. Pakua / weka project

Ikiwa una folder ya `udiap` tayari:

```bash
cd ~/storage/shared   # au mahali ulipoweka project
# au
cd ~
```

Ikiwa bado huna project, unaweza kunakili folder yote ya `udiap`.

---

## 3. Backend (FastAPI)

```bash
cd udiap/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Anzisha server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Weka terminal hii wazi** (usifunge).

Unaweza kufungua browser ya simu:
```
http://127.0.0.1:8000/docs
```
kuona API docs.

### Seed data (terminal nyingine)

Fungua tab mpya ya Termux:

```bash
cd udiap/backend
source venv/bin/activate
PYTHONPATH=. python seed.py
```

Accounts:
- `admin@udiap.ai` / `Admin@12345`
- `demo@udiap.ai` / `Demo@12345`

---

## 4. Frontend (Next.js)

Fungua **tab nyingine** ya Termux:

```bash
cd udiap/frontend

# Install node packages (inaweza kuchukua muda mrefu kwenye simu)
npm install

# Anzisha
npm run dev -- -H 0.0.0.0 -p 3000
```

Kisha fungua browser ya simu:
```
http://127.0.0.1:3000
```
au
```
http://localhost:3000
```

---

## 5. Vidokezo muhimu kwa Termux

| Tatizo | Suluhisho |
|--------|-----------|
| `npm install` inashindwa / polepole | Subiri, au fanya `npm install --legacy-peer-deps` |
| Memory inakwisha | Fungua apps nyingine, au tumia `NODE_OPTIONS=--max-old-space-size=512` |
| Port already in use | Badilisha port: `--port 3001` |
| Backend haioni database | SQLite file `udiap.db` inaundwa automatic kwenye folder ya backend |
| CORS errors | Tayari tumekubali `*` kwenye development |

---

## 6. Mpango wa terminal (mapendekezo)

- **Tab 1**: Backend (`uvicorn ...`)
- **Tab 2**: Frontend (`npm run dev ...`)
- **Tab 3**: (optional) seed / debugging

Unaweza kutumia `tmux` ndani ya Termux ili usipoteze sessions:

```bash
pkg install tmux
tmux
```

---

## 7. Kama frontend inashindwa kwenye simu

Next.js inaweza kuwa nzito sana kwa simu za kawaida. Alternatives:

1. Tumia **backend tu** + fungua `/docs` na jaribu API manually
2. Au unda version nyepesi ya HTML static baadaye

---

## Summary commands (copy-paste)

```bash
# === BACKEND ===
cd udiap/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

# === FRONTEND (tab mpya) ===
cd udiap/frontend
npm install
npm run dev -- -H 0.0.0.0 -p 3000
```

Kisha fungua: **http://127.0.0.1:3000**
