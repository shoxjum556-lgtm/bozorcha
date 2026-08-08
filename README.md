# Bozorcha — Django + DRF loyihasi (server-side render)

Sayt **Django shablonlari** (templates) orqali to'liq serverda render qilinadi —
alohida HTML/JS frontend fayli yo'q. Login sessiya (cookie) orqali, forma va tugmalar
oddiy Django formalari orqali ishlaydi.

## Tuzilishi
- `core/` — Django sozlamalari va asosiy urls
- `users/` — User, Profile modellari (custom user, JWT-based DRF API ham bor)
- `posts/` — blog post APIView misollari (3-dars, DRF API)
- `shop/` — mahsulot/savat/buyurtma modellari + DRF API (`/api/shop/...`, ixtiyoriy)
- `storefront/` — **asosiy sayt**: Django view + template'lar (ro'yxatdan o'tish,
  login, profil, mahsulotlar, savat, checkout)
- `static/css/style.css` — barcha sahifalar uchun umumiy stil

## Ishga tushirish
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata sample_products   # namunaviy mahsulotlar
python manage.py createsuperuser            # admin panel uchun (ixtiyoriy)
python manage.py runserver
```
Brauzerda oching: **http://127.0.0.1:8000/**

Admin panel: http://127.0.0.1:8000/admin/

## Sayt sahifalari (barchasi Django view orqali render qilinadi)
| URL | Nima qiladi |
|---|---|
| `/` | mahsulotlar ro'yxati, qidiruv (`?q=`), kategoriya bo'yicha filtr |
| `/register/` | ro'yxatdan o'tish (forma) |
| `/login/` | kirish (sessiya orqali) |
| `/logout/` | chiqish |
| `/profile/` | profilni ko'rish/tahrirlash + buyurtmalar tarixi |
| `/cart/` | savat — miqdorni +/− bilan o'zgartirish, o'chirish |
| `/cart/add/<product_id>/` | savatga qo'shish (POST) |
| `/checkout/` | manzil kiritib buyurtma berish → tasdiqlash sahifasi |

## Eslatma
`users/models.py`dagi `phone` maydoni `max_length=12` — bu darsdagi asl kod,
shuning uchun ro'yxatdan o'tishda telefon raqamni `+998` bilan emas, 9 xonali
formatda kiriting (masalan `901234567`), aks holda validatsiya xatosi chiqadi.

DRF API (`/api/...`) ham loyihada saqlanib qolgan — agar kelajakda mobil ilova
yoki boshqa frontend kerak bo'lsa, undan foydalanish mumkin, lekin asosiy sayt
uchun shart emas.

## Render.com'ga joylashtirish (bepul)

### 1-qadam — GitHub'ga yuklash
1. https://github.com da yangi (bo'sh) repository yarating
2. `loyiha` papkasi ichida terminalda:
   ```bash
   git init
   git add .
   git commit -m "Birinchi commit"
   git branch -M main
   git remote add origin https://github.com/FOYDALANUVCHI/REPO-NOMI.git
   git push -u origin main
   ```
   (`.env` fayli avtomatik yuklanmaydi — `.gitignore`da chiqarib tashlangan)

### 2-qadam — Render'da hisob oching
https://render.com — GitHub orqali ro'yxatdan o'ting (karta so'ramaydi)

### 3-qadam — Blueprint orqali (eng oson)
1. Render dashboard → **New** → **Blueprint**
2. Yuqorida yaratgan GitHub repo'ni tanlang — Render `render.yaml` faylini avtomatik topadi
3. **Apply** tugmasini bosing — Render o'zi web-service va bepul PostgreSQL bazasini yaratadi, `SECRET_KEY`ni ham o'zi generatsiya qiladi
4. 2-5 daqiqada loyiha `https://bozorcha.onrender.com` (yoki shunga o'xshash) manzilda tayyor bo'ladi

### 3-qadam (muqobil) — Qo'lda sozlash
Agar Blueprint ishlamasa:
1. **New** → **Web Service** → repo'ni tanlang
2. **Build Command**: `./build.sh`
3. **Start Command**: `gunicorn core.wsgi:application`
4. **Environment** bo'limida qo'shing:
   - `SECRET_KEY` — istalgan uzun tasodifiy matn
   - `DEBUG` = `False`
   - `PYTHON_VERSION` = `3.12.0`
5. Alohida **PostgreSQL** (Free) yarating, uning **Internal Database URL**'ini nusxalab, web service'ga `DATABASE_URL` nomi bilan qo'shing
6. **Create Web Service**

### 4-qadam — namunaviy mahsulotlarni yuklash
Render dashboard'da web service → **Shell** bo'limini oching va yozing:
```bash
python manage.py loaddata sample_products
python manage.py createsuperuser
```

### Eslatma
- Bepul tarif 15 daqiqa harakatsizlikdan keyin "uxlab qoladi" — birinchi so'rov 30-60 soniya sekin ochilishi mumkin, bu normal
- Bepul PostgreSQL baza 90 kundan keyin muddati tugaydi — shu vaqtga qadar yangi (pullik yoki yangi bepul) bazaga o'tkazish kerak bo'ladi
