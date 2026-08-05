# UDIAP — Deployment Guide (Simu ya Android, bila PC)

Hatua zote hapa chini unafanya wewe kupitia **browser ya simu** (Chrome) na app ya
**GitHub** (au Termux ukipenda). Sina uwezo wa ku-login kwenye akaunti zako, hivyo
sehemu za "click Deploy" ni lazima uzifanye mwenyewe — nimekuandalia kila thamani
utakayohitaji kubandika.

---

## Hatua 0 — Kabla ya kuanza
Umeshapokea kutoka kwangu faili zilizorekebishwa:
- `.gitignore` (mzizi wa project)
- `backend/requirements.txt` (imeongezwa `asyncpg`, `psycopg2-binary`, `gunicorn`)
- `backend/app/core/config.py` (inarekebisha DATABASE_URL moja kwa moja iwe async-compatible)
- `render.yaml` (blueprint ya Render — backend + Postgres)

Pakua zip iliyorekebishwa (nitakupa link chini ya ujumbe huu) na uibadilishe na ya zamani.

---

## Hatua 1 — Pandisha GitHub (kupitia simu)
1. Fungua **github.com** kwenye Chrome, ingia kwenye akaunti yako.
2. Bonyeza **+ → New repository** → jina `udiap` → **Private** (pendekezo, kwa sababu ina secrets/logic ya biashara) → Create.
3. Kwenye repo tupu, tumia kitufe **"uploading an existing file"** → chagua faili zote kutoka kwenye folder uliyopakua (unaweza ku-drag kutoka File Manager ya Android) → Commit.
   - Njia mbadala (rahisi zaidi ukiwa na faili nyingi): sakinisha app ya **"Working Copy"** (au **Termux + git**) kwenye Android, `git init`, `git remote add origin ...`, `git push`.

✅ Hakikisha `.env` halijapanda kwenye GitHub — `.gitignore` mpya inalizuia hilo moja kwa moja.

---

## Hatua 2 — Deploy Backend + Database (Render)
1. Fungua **render.com** → ingia (unaweza signup kwa GitHub moja kwa moja).
2. **New → Blueprint** → unganisha repo yako ya `udiap` → Render itasoma `render.yaml` moja kwa moja na kuonyesha: `udiap-backend` (web service) + `udiap-db` (Postgres).
3. Bonyeza **Apply**. Render itafanya yote:
   - Kuunda Postgres database
   - Kuunganisha `DATABASE_URL` moja kwa moja kwenye backend
   - Kutengeneza `SECRET_KEY` yenyewe (random, salama)
4. Baada ya build kukamilika (dakika 3-5), utapata URL kama:
   `https://udiap-backend.onrender.com`
5. Fungua `https://udiap-backend.onrender.com/health` — inatakiwa ionyeshe `{"status":"healthy"}`.
6. Fungua `https://udiap-backend.onrender.com/docs` — hii ndiyo **API documentation URL** (Swagger, auto-generated na FastAPI).

⚠️ Kumbuka kurudi kwenye Render dashboard → Environment → `CORS_ORIGINS` → badilisha kutoka placeholder kwenda URL halisi ya frontend (Hatua 3) mara utakapoipata.

---

## Hatua 3 — Deploy Frontend (Vercel)
1. Fungua **vercel.com** → Login na GitHub.
2. **Add New → Project** → chagua repo `udiap` → kwenye "Root Directory" chagua `frontend`.
3. Kwenye **Environment Variables**, ongeza:
   - `NEXT_PUBLIC_API_URL` = `https://udiap-backend.onrender.com/api`
4. Bonyeza **Deploy**. Baada ya dakika 1-3 utapata URL kama:
   `https://udiap.vercel.app`

Rudi Render → `CORS_ORIGINS` → weka `["https://udiap.vercel.app"]` → Save (backend ita-restart yenyewe).

---

## Hatua 4 — Seed Data (admin + demo user)
Render ina **Shell** tab kwenye dashboard ya service (haihitaji PC):
1. Fungua `udiap-backend` service → tab **Shell**.
2. Andika: `python -m seed`
3. Hii itaunda:
   - Admin: `admin@udiap.ai` / `Admin@12345`
   - Demo: `demo@udiap.ai` / `Demo@12345`

⚠️ **Lazima ubadilishe password hizi baada ya login ya kwanza** — ni default za wazi kabisa kwenye source code, si salama kwa production ya kweli.

---

## Hatua 5 — Uthibitisho (checklist ya kweli, si dhana)
Fungua `https://udiap.vercel.app` kwenye simu na uthibitishe kwa macho:
- [ ] Landing page inapakia
- [ ] Register → akaunti mpya inatengenezwa
- [ ] Login (demo@udiap.ai / Demo@12345) → dashboard inaonekana
- [ ] Assessment inafunguka na inakubali majibu
- [ ] Report inatengenezwa baada ya assessment
- [ ] Analytics page inaonyesha data
- [ ] Login kama admin → admin panel inafunguka

---

## Ukweli kuhusu "AI Reports"
Nimeangalia `report_generator.py`: kwa sasa **si LLM-powered** — ni rule-based
(scoring + thresholds zilizowekwa kwa mkono), ingawa architecture iko tayari kwa
kuunganisha LLM baadaye (`OPENAI_API_KEY` ipo kwenye config kama placeholder,
haitumiki popote bado). Hii ina maana:
- Reports zitafanya kazi **bila** OPENAI_API_KEY.
- Kama unataka reports za kweli za AI (kutumia GPT/Claude kuchambua majibu),
  hiyo ni kazi ya ziada ambayo bado haijafanyika — niambie ukitaka niongeze.

---

## Mapungufu yaliyobaki (kwa uwazi)
- **Free tier za Render**: backend "inalala" baada ya dakika 15 bila trafiki —
  request ya kwanza baada ya hapo inachukua ~30-50 sekunde kuamka. Kwa demo ni sawa;
  kwa production ya kweli utahitaji paid plan ($7/mo) ili isilale.
- **Hakuna automated tests** — folder `tests/` ipo tupu. Sikuandika tests mpya
  kwa sababu hukuomba hilo; niambie ukihitaji.
- Sijaweza kufanya `npm run build` mwenyewe (mazingira yangu ya sasa hayana
  network access), kwa hiyo build errors zozote za Next.js zitaonekana wakati
  Vercel inajaribu ku-build — nikitumia link ya build log utakayonitumia, naweza
  kuzitatua haraka.
