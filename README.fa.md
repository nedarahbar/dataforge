# مستند کامل پروژه

# Smart Data Cleaning & Analysis API

**نسخه:** ۱.۰.۰  
**زبان مستند:** فارسی  
**نوع پروژه:** Backend / Portfolio / Final Project  
**مجوز:** MIT

---

## فهرست مطالب

1. [معرفی پروژه](#۱-معرفی-پروژه)
2. [بیان مسئله](#۲-بیان-مسئله)
3. [اهداف و غیرهدف‌ها](#۳-اهداف-و-غیرهدف‌ها)
4. [کاربران هدف](#۴-کاربران-هدف)
5. [سفر کاربر و Pipeline](#۵-سفر-کاربر-و-pipeline)
6. [پشته فناوری (Tech Stack)](#۶-پشته-فناوری-tech-stack)
7. [معماری نرم‌افزار](#۷-معماری-نرم‌افزار)
8. [ساختار پوشه‌ها](#۸-ساختار-پوشه‌ها)
9. [مدل‌های پایگاه‌داده](#۹-مدل‌های-پایگاه‌داده)
10. [وضعیت Dataset](#۱۰-وضعیت-dataset)
11. [Endpoints کامل API](#۱۱-endpoints-کامل-api)
12. [منطق پاک‌سازی داده](#۱۲-منطق-پاک‌سازی-داده)
13. [امتیاز کیفیت داده](#۱۳-امتیاز-کیفیت-داده)
14. [تحلیل داده](#۱۴-تحلیل-داده)
15. [مدیریت خطا](#۱۵-مدیریت-خطا)
16. [پیکربندی و امنیت](#۱۶-پیکربندی-و-امنیت)
17. [نصب و راه‌اندازی محلی](#۱۷-نصب-و-راه‌اندازی-محلی)
18. [اجرا با Docker](#۱۸-اجرا-با-docker)
19. [گردش‌کار نمونه (Example Workflow)](#۱۹-گردش‌کار-نمونه-example-workflow)
20. [دیتاست نمونه](#۲۰-دیتاست-نمونه)
21. [تست‌ها](#۲۱-تست‌ها)
22. [لاگ و مشاهده‌پذیری](#۲۲-لاگ-و-مشاهده‌پذیری)
23. [اسکرین‌شات‌ها](#۲۳-اسکرین‌شات‌ها)
24. [عیب‌یابی رایج](#۲۴-عیب‌یابی-رایج)
25. [بهبودهای آینده](#۲۵-بهبودهای-آینده)
26. [معیار پذیرش و Definition of Done](#۲۶-معیار-پذیرش-و-definition-of-done)
27. [مجوز](#۲۷-مجوز)

---

## ۱. معرفی پروژه

**Smart Data Cleaning & Analysis API** یک سرویس RESTful حرفه‌ای با **FastAPI** است که Datasetهای خام و پرخطا را دریافت می‌کند و آن‌ها را به Datasetهای ساختاریافته، پاک‌شده و قابل‌تحلیل تبدیل می‌کند.

این پروژه فقط چند Endpoint ساده نیست؛ بلکه یک Backend واقعی با موارد زیر است:

- معماری چندلایه
- جداسازی مسئولیت‌ها (Separation of Concerns)
- کد تمیز و قابل تست
- مدیریت خطای استاندارد
- ذخیره‌سازی در Database
- Configuration Management
- Dockerization
- مستندات OpenAPI / Swagger
- بیش از ۲۰ تست واقعی

### Pipeline اصلی

```text
Upload
   ↓
Validation
   ↓
Profiling
   ↓
Cleaning
   ↓
Quality Assessment
   ↓
Analysis
   ↓
Download
```

---

## ۲. بیان مسئله

در بسیاری از پروژه‌های Data Science و Business Intelligence، Dataset اولیه معمولاً مشکلاتی مثل موارد زیر دارد:

| مشکل | توضیح کوتاه |
| --- | --- |
| Missing Values | مقادیر خالی / null |
| Duplicate Records | ردیف‌های تکراری |
| Inconsistent Text | مثلاً `Tehran` و `tehran` و `TEHRAN` |
| Invalid Values | سن منفی، قیمت منفی، ایمیل نامعتبر |
| Incorrect Data Types | نوع داده اشتباه |
| Outliers | مقادیر پرت آماری |
| Formatting Errors | فرمت‌های ناسازگار تاریخ |
| Empty Rows/Columns | ردیف/ستون خالی |

اگر این مشکلات قبل از تحلیل برطرف نشوند، خروجی تحلیل می‌تواند نادرست یا گمراه‌کننده باشد.

هدف این سرویس این است که به‌صورت مستقل Dataset را بگیرد، کیفیت را بسنجد، مشکلات رایج را شناسایی/اصلاح کند و در نهایت Dataset پاک‌شده به‌همراه گزارش تحلیلی ارائه دهد.

---

## ۳. اهداف و غیرهدف‌ها

### اهداف اصلی

1. دریافت فایل CSV و Excel
2. Validation فایل
3. ثبت Dataset در Database
4. Profiling اولیه
5. شناسایی مشکلات داده
6. Cleaning بر اساس Configuration
7. مقایسه Before / After
8. محاسبه Data Quality Score
9. تحلیل Dataset پاک‌شده
10. Download نسخه Clean
11. ثبت عملیات مهم در Database
12. مدیریت خطای استاندارد
13. مستندسازی با Swagger/OpenAPI
14. حداقل ۲۰ تست واقعی
15. اجرای کامل با Docker

### غیرهدف‌ها (نسخه ۱)

- Machine Learning خودکار
- Data Warehouse
- Distributed Processing
- Real-time Streaming
- Authentication پیچیده
- Multi-tenant Architecture
- الزام Cloud Deployment
- Natural Language Query
- Schema Discovery پیشرفته
- Dashboard بصری مستقل

---

## ۴. کاربران هدف

| کاربر | نیاز |
| --- | --- |
| Data Analyst | آپلود داده خام و بررسی کیفیت قبل از تحلیل |
| Data Scientist | استفاده از Pipeline آماده برای Preprocessing |
| Backend Developer | بررسی معماری و توسعه سرویس |
| Reviewer / Instructor | Clone، اجرا، تست API و ارزیابی کیفیت |

---

## ۵. سفر کاربر و Pipeline

```text
کاربر
 │
 ├── آپلود Dataset
 ▼
اعتبارسنجی فایل
 ▼
ثبت در Database
 ▼
Profiling اولیه
 ▼
بازبینی Profile توسط کاربر
 ▼
ارسال Cleaning Configuration
 ▼
اجرای Cleaning Pipeline
 ▼
گزارش کیفیت (Quality)
 ▼
تحلیل (Analysis)
 ▼
دانلود Dataset پاک‌شده
```

---

## ۶. پشته فناوری (Tech Stack)

### الزامی

| فناوری | نقش |
| --- | --- |
| **Python 3.11+** | زبان اصلی |
| **FastAPI** | فریم‌ورک API |
| **Uvicorn** | ASGI Server |
| **Pandas** | پردازش جدولی داده |
| **NumPy** | محاسبات عددی |
| **Pydantic / pydantic-settings** | اعتبارسنجی و تنظیمات |
| **SQLAlchemy** | ORM |
| **SQLite** | پایگاه‌داده محلی |
| **Pytest** | تست |
| **Docker / Compose** | کانتینرسازی |
| **openpyxl** | پشتیبانی Excel |
| **python-multipart** | آپلود فایل |

### توصیه‌شده / استفاده‌شده در توسعه

| فناوری | نقش |
| --- | --- |
| httpx | کلاینت تست HTTP |
| pytest-cov | پوشش تست |
| ruff | Lint |
| python-dotenv | بارگذاری `.env` |

### مدیریت وابستگی‌ها

همه Dependencyها در `pyproject.toml` ثبت شده‌اند:

```bash
pip install .
pip install ".[dev]"   # همراه ابزارهای تست و توسعه
```

---

## ۷. معماری نرم‌افزار

معماری لایه‌ای است تا منطق کسب‌وکار داخل Routeها نرود.

| لایه | مسیر | مسئولیت |
| --- | --- | --- |
| **API** | `app/api/` | HTTP Request/Response، DI، اعتبارسنجی ورودی |
| **Schemas** | `app/schemas/` | مدل‌های Pydantic برای Request/Response |
| **Services** | `app/services/` | Profiling، Cleaning، Analysis، Quality، File I/O |
| **Database** | `app/database/` | Engine، Session، ORM Models |
| **Core** | `app/core/` | Config، Logging، Exceptions |
| **Utils** | `app/utils/` | ثابت‌ها و Helperها |

### اصول مهندسی

1. Separation of Concerns
2. Single Responsibility
3. DRY
4. Explicit Validation
5. Configuration به‌جای Hard-Coding
6. حفظ داده خام (Original)
7. Cleaning قابل تکرار (Reproducible)
8. تست منطق بحرانی
9. قرارداد API یکنواخت
10. خطای معنادار برای کلاینت

### چیزهایی که عمداً انجام نشده

- ریختن همه منطق داخل `main.py`
- SQL خام داخل Route
- Cleaning داخل Endpoint
- DataFrame سراسری (Global)
- مسیر فایل Hard-coded
- `except:` خالی
- Functionهای بسیار بزرگ

---

## ۸. ساختار پوشه‌ها

```text
dataforge/
├── app/
│   ├── main.py                 # نقطه ورود FastAPI
│   ├── api/
│   │   ├── datasets.py         # Endpointهای Dataset
│   │   └── analysis.py         # Endpoint کمکی تحلیل
│   ├── core/
│   │   ├── config.py           # تنظیمات از ENV
│   │   ├── exceptions.py       # خطاهای دامنه
│   │   └── logging.py          # لاگ استاندارد
│   ├── database/
│   │   ├── database.py         # Engine / Session
│   │   └── models.py           # جداول SQLAlchemy
│   ├── models/                 # Re-export دامنه
│   ├── schemas/                # Pydantic schemas
│   ├── services/
│   │   ├── file_handler.py
│   │   ├── profiler.py
│   │   ├── cleaner.py
│   │   ├── validator.py
│   │   ├── analyzer.py
│   │   ├── quality.py
│   │   └── dataset_service.py  # orchestration
│   └── utils/
├── tests/                      # Pytest
├── sample_data/
│   └── customers_dirty.csv
├── storage/
│   ├── raw/                    # فایل خام
│   └── cleaned/                # فایل پاک‌شده
├── screenshots/
├── scripts/
│   └── verify_prd.py           # چک‌لیست پذیرش
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md                   # مستند انگلیسی
├── README.fa.md                # همین مستند فارسی
├── LICENSE
└── prd.md                      # سند نیازمندی‌ها
```

---

## ۹. مدل‌های پایگاه‌داده

### جدول `datasets`

| فیلد | نوع | توضیح |
| --- | --- | --- |
| id | Integer | کلید اصلی |
| filename | String | نام فایل اصلی |
| file_type | String | csv / xlsx / xls |
| original_path | String | مسیر فایل خام |
| cleaned_path | String | مسیر فایل پاک‌شده |
| rows | Integer | تعداد ردیف |
| columns | Integer | تعداد ستون |
| status | String | وضعیت Dataset |
| created_at | DateTime | زمان ایجاد |
| updated_at | DateTime | آخرین به‌روزرسانی |

### جدول `cleaning_operations`

| فیلد | نوع |
| --- | --- |
| id | Integer |
| dataset_id | Foreign Key |
| configuration | JSON/Text |
| rows_before | Integer |
| rows_after | Integer |
| duplicates_removed | Integer |
| missing_values_filled | Integer |
| invalid_values_detected | Integer |
| outliers_detected | Integer |
| status | String |
| created_at | DateTime |

هر عملیات Cleaning برای Audit در Database ثبت می‌شود.

---

## ۱۰. وضعیت Dataset

```text
UPLOADED → PROFILED → CLEANING → CLEANED
                ↘
               FAILED
```

| وضعیت | معنی |
| --- | --- |
| `UPLOADED` | فایل آپلود و ثبت شده |
| `PROFILED` | حداقل یک‌بار Profile گرفته شده |
| `CLEANING` | Pipeline در حال اجرا |
| `CLEANED` | پاک‌سازی موفق |
| `FAILED` | خطا در پردازش |
| `DELETED` | حذف‌شده (در صورت استفاده منطقی) |

---

## ۱۱. Endpoints کامل API

Base URL پیش‌فرض: `http://localhost:8000`

| Method | Endpoint | توضیح | Status موفق |
| --- | --- | --- | --- |
| GET | `/` | اطلاعات سرویس | ۲۰۰ |
| GET | `/health` | Health check | ۲۰۰ |
| POST | `/datasets/upload` | آپلود CSV/Excel | ۲۰۱ |
| GET | `/datasets?page=1&page_size=20` | لیست با Pagination | ۲۰۰ |
| GET | `/datasets/{id}` | جزئیات Dataset | ۲۰۰ |
| GET | `/datasets/{id}/profile` | Profiling | ۲۰۰ |
| POST | `/datasets/{id}/clean` | اجرای Cleaning | ۲۰۰ |
| GET | `/datasets/{id}/quality` | گزارش کیفیت | ۲۰۰ |
| GET | `/datasets/{id}/analysis` | تحلیل داده پاک‌شده | ۲۰۰ |
| GET | `/datasets/{id}/download` | دانلود CSV پاک‌شده | ۲۰۰ |
| DELETE | `/datasets/{id}` | حذف کامل | ۲۰۴ |
| GET | `/datasets/{id}/cleaning-history` | تاریخچه Cleaning | ۲۰۰ |
| GET | `/analysis/datasets/{id}` | مسیر کمکی تحلیل | ۲۰۰ |

### مستندات تعاملی

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

### نمونه بدنه Cleaning

```json
{
  "remove_duplicates": true,
  "fill_missing": true,
  "normalize_text": true,
  "validate_values": true,
  "detect_outliers": true,
  "numeric_strategy": "median",
  "categorical_strategy": "mode"
}
```

### محدودیت آپلود

| مورد | مقدار پیش‌فرض |
| --- | --- |
| حداکثر حجم | ۵۰ MB (`52428800` بایت) |
| فرمت‌های مجاز | `csv`, `xlsx`, `xls` |
| فایل خالی | رد می‌شود |
| Extension نامعتبر | رد می‌شود |
| فایل خراب/غیرقابل Parse | رد می‌شود |

---

## ۱۲. منطق پاک‌سازی داده

### ترتیب Pipeline

```text
Load Dataset
     ↓
Schema Detection
     ↓
Missing Value Handling
     ↓
Duplicate Removal
     ↓
Text Normalization
     ↓
Invalid Value Detection
     ↓
Outlier Detection (IQR)
     ↓
Save Clean Dataset
     ↓
Generate Quality Report
```

### استراتژی Missing Values

| نوع ستون | پیش‌فرض |
| --- | --- |
| عددی | Median (مقاوم‌تر نسبت به Mean در برابر Outlier) |
| متنی/Categorical | Mode |
| ستون ۱۰۰٪ خالی | حذف خودکار نمی‌شود؛ در گزارش ثبت می‌شود |
| ستون Email | Mode فقط از ایمیل‌های معتبر (جلوگیری از پر شدن با `invalid-email`) |

### نرمال‌سازی متن

حداقل مراحل:

1. Trim فاصله ابتدا/انتها
2. حذف فاصله‌های تکراری
3. یکسان‌سازی Case
4. Canonical mapping برای دسته‌ها (مثلاً همه به `Tehran`)

**نکته مهم:** نرمال‌سازی کورکورانه روی همه ستون‌ها اعمال نمی‌شود. ستون‌هایی مثل `email`، `customer_id` و `date` محافظت شده‌اند.

### اعتبارسنجی مقادیر نامعتبر

| ستون | قانون |
| --- | --- |
| age | بین ۰ تا ۱۲۰ |
| salary / quantity / unit_price / total_sales | ≥ ۰ |
| email | فرمت ساده ایمیل |
| date | قابل Parse بودن تاریخ |

### تشخیص Outlier با روش IQR

```text
IQR = Q3 - Q1
Lower = Q1 - 1.5 × IQR
Upper = Q3 + 1.5 × IQR
```

**تصمیم نسخه ۱:** Outlierها **گزارش** می‌شوند ولی **حذف اجباری نمی‌شوند** تا Analyst تصمیم بگیرد.

### اصول داده

1. هیچ تغییری بی‌صدا و بدون گزارش انجام نشود
2. فایل خام overwrite نشود
3. Cleaning قابل تنظیم باشد
4. با Dataset و Config یکسان، نتیجه تا حد ممکن deterministic باشد
5. همیشه Summary تولید شود

### مسیر ذخیره‌سازی

```text
storage/
├── raw/
│   └── <dataset_id>_original.csv
└── cleaned/
    └── <dataset_id>_cleaned.csv
```

---

## ۱۳. امتیاز کیفیت داده

امتیاز نهایی بین ۰ تا ۱۰۰ و Clamp شده است:

```text
Final Score =
    30% Missing Score
  + 25% Duplicate Score
  + 25% Invalid Value Score
  + 20% Consistency Score
```

### تفسیر امتیاز

| بازه | تفسیر |
| --- | --- |
| ۹۰–۱۰۰ | Excellent (عالی) |
| ۷۵–۸۹ | Good (خوب) |
| ۶۰–۷۴ | Fair (متوسط) |
| ۴۰–۵۹ | Poor (ضعیف) |
| ۰–۳۹ | Critical (بحرانی) |

Endpoint کیفیت، وضعیت **قبل و بعد** Cleaning را هم برمی‌گرداند.

---

## ۱۴. تحلیل داده

تحلیل فقط روی Dataset **پاک‌شده** انجام می‌شود. اگر هنوز Clean نشده باشد:

```text
DATASET_NOT_CLEANED  →  HTTP 400
```

### تحلیل عددی

Count، Mean، Median، Min، Max، Std، Percentiles (P25/P50/P75)

### تحلیل Categorical

Unique Count، Top Categories، Frequency، Percentage

### تحلیل Business (شرطی)

اگر ستون‌های مناسب وجود داشته باشد:

- Total Sales
- Average Sales
- Top Products
- Top Customers
- Sales by Region
- Monthly Sales

اگر ستون‌ها نباشند، API Crash نمی‌کند و بخش Business خالی/Null می‌ماند.

---

## ۱۵. مدیریت خطا

فرمت استاندارد پاسخ خطا:

```json
{
  "error": {
    "code": "DATASET_NOT_FOUND",
    "message": "Dataset with id 101 was not found."
  }
}
```

### کدهای خطا

| Code | معنی تقریبی | HTTP |
| --- | --- | --- |
| `INVALID_FILE_TYPE` | پسوند/نوع فایل نامعتبر | ۴۰۰ |
| `FILE_TOO_LARGE` | حجم بیش از حد | ۴۱۳ |
| `EMPTY_FILE` | فایل خالی | ۴۰۰ |
| `INVALID_DATASET` | Parse ناموفق / بدون Header | ۴۰۰ |
| `DATASET_NOT_FOUND` | Dataset پیدا نشد | ۴۰۴ |
| `DATASET_NOT_CLEANED` | هنوز Clean نشده | ۴۰۰ |
| `PROCESSING_ERROR` | خطای پردازش داخلی | ۵۰۰ |
| `INVALID_CLEANING_CONFIGURATION` | Config نامعتبر | ۴۲۲ |
| `UNSUPPORTED_OPERATION` | عملیات پشتیبانی‌نشده | ۴۰۰ |

Stack Trace داخلی به کلاینت برگردانده نمی‌شود.

---

## ۱۶. پیکربندی و امنیت

### فایل `.env` (Commit نشود)

از روی نمونه بسازید:

```bash
cp .env.example .env
```

| متغیر | توضیح | نمونه |
| --- | --- | --- |
| `DATABASE_URL` | آدرس Database | `sqlite:///./smart_data.db` |
| `MAX_FILE_SIZE` | سقف حجم آپلود (بایت) | `52428800` |
| `STORAGE_PATH` | ریشه storage | `./storage` |
| `ALLOWED_EXTENSIONS` | پسوندهای مجاز | `csv,xlsx,xls` |
| `ENVIRONMENT` | محیط اجرا | `development` |
| `LOG_LEVEL` | سطح لاگ | `INFO` |

### نکات امنیتی نسخه ۱

- محدودیت حجم فایل
- Whitelist پسوند
- جلوگیری از Path Traversal (استفاده از basename امن)
- Validation محتوا/Parse
- عدم نمایش Stack Trace
- عدم Commit کردن Secret
- جدا نگه‌داشتن فایل خام و پاک‌شده

---

## ۱۷. نصب و راه‌اندازی محلی

### پیش‌نیازها

- Python 3.11 یا بالاتر
- pip
- (اختیاری) Git

### مراحل

```bash
# 1) کلون / ورود به پروژه
cd dataforge

# 2) ساخت محیط مجازی
python -m venv .venv

# 3) فعال‌سازی
source .venv/bin/activate
# ویندوز:
# .venv\Scripts\activate

# 4) نصب پکیج و وابستگی‌های توسعه
pip install ".[dev]"

# 5) تنظیم ENV
cp .env.example .env

# 6) اجرای سرور
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### آدرس‌های مهم بعد از اجرا

| سرویس | آدرس |
| --- | --- |
| Root | http://localhost:8000 |
| Health | http://localhost:8000/health |
| Swagger | http://localhost:8000/docs |

---

## ۱۸. اجرا با Docker

### فایل‌ها

- `Dockerfile`
- `docker-compose.yml`

### دستور

```bash
docker compose up --build
```

سرویس روی پورت **۸۰۰۰** بالا می‌آید و Volume برای `storage` و Database در نظر گرفته شده است.

سپس:

```text
http://localhost:8000/docs
```

### نکته

اگر Docker روی سیستم نصب نباشد، از روش اجرای محلی (بخش ۱۷) استفاده کنید؛ منطق برنامه یکسان است.

---

## ۱۹. گردش‌کار نمونه (Example Workflow)

فرض: سرور روی `localhost:8000` در حال اجراست.

### مرحله ۱ — آپلود

```bash
curl -X POST http://localhost:8000/datasets/upload \
  -F "file=@sample_data/customers_dirty.csv"
```

پاسخ نمونه:

```json
{
  "dataset_id": 1,
  "filename": "customers_dirty.csv",
  "file_type": "csv",
  "rows": 810,
  "columns": 11,
  "status": "UPLOADED"
}
```

### مرحله ۲ — Profile

```bash
curl http://localhost:8000/datasets/1/profile
```

### مرحله ۳ — Clean

```bash
curl -X POST http://localhost:8000/datasets/1/clean \
  -H "Content-Type: application/json" \
  -d '{
    "remove_duplicates": true,
    "fill_missing": true,
    "normalize_text": true,
    "validate_values": true,
    "detect_outliers": true
  }'
```

### مرحله ۴ — Quality

```bash
curl http://localhost:8000/datasets/1/quality
```

### مرحله ۵ — Analysis

```bash
curl http://localhost:8000/datasets/1/analysis
```

### مرحله ۶ — Download

```bash
curl -OJ http://localhost:8000/datasets/1/download
```

### مرحله ۷ — حذف (اختیاری)

```bash
curl -X DELETE http://localhost:8000/datasets/1
```

حذف شامل: رکورد Database، فایل خام، فایل پاک‌شده و تاریخچه Cleaning مرتبط است.

---

## ۲۰. دیتاست نمونه

مسیر دمو:

```text
sample_data/customers_dirty.csv
```

مسیر **داده‌های تست + سناریوهای فارسی**:

```text
test_data/
├── customers_test_dirty.csv
├── customers_test_clean.csv
├── empty.csv
├── unsupported.txt
├── no_header.csv
└── سناریوهای-تست.md
```

راهنمای کامل سناریوها و گام‌ها: [`test_data/سناریوهای-تست.md`](test_data/سناریوهای-تست.md)

حدود ۸۰۰+ ردیف در `sample_data` با ستون‌های:

```text
customer_id, name, email, age, city, region,
product, quantity, unit_price, total_sales, date
```

عمداً شامل موارد زیر است:

- Missing Values
- Duplicate Rows
- نام شهر ناسازگار (`Tehran` / `tehran` / `TEHRAN`)
- سن نامعتبر (منفی یا خیلی بزرگ)
- ایمیل نامعتبر
- quantity / unit_price منفی
- Outlier در فروش/قیمت
- فرمت‌های مختلف تاریخ

---

## ۲۱. تست‌ها

### اجرا

```bash
pytest -q
pytest --cov=app --cov-report=term-missing
```

### پوشش موضوعی

| حوزه | فایل نمونه |
| --- | --- |
| Upload | `tests/test_upload.py` |
| Validation | `tests/test_validation.py` |
| Profiling | `tests/test_profiling.py` |
| Cleaning | `tests/test_cleaning.py` |
| Quality | `tests/test_quality.py` |
| Analysis | `tests/test_analysis.py` |
| Download | `tests/test_download.py` |
| Database | `tests/test_database.py` |
| API Errors | `tests/test_errors.py` |

حداقل ۲۰ تست معنادار وجود دارد (در پیاده‌سازی فعلی معمولاً **۴۲ تست** پاس می‌شوند).

### چک‌لیست پذیرش خودکار

```bash
python scripts/verify_prd.py
```

این اسکریپت وجود فایل‌ها، Endpointها، بخش‌های README، تست‌ها و در صورت بالا بودن سرور، Workflow زنده را بررسی می‌کند.

---

## ۲۲. لاگ و مشاهده‌پذیری

رویدادهای مهم لاگ می‌شوند:

- Startup اپلیکیشن
- آپلود فایل
- شروع/پایان Cleaning
- خطای پردازش
- حذف Dataset

لاگ‌ها نباید بی‌دلیل محتوای حساس Dataset را چاپ کنند.

برای آینده معماری طوری است که بتوان Metrics، Prometheus، Request ID و Structured Logging اضافه کرد.

---

## ۲۳. اسکرین‌شات‌ها

پوشه:

```text
screenshots/
├── swagger-overview.png
├── upload.png
├── profile.png
├── cleaning.png
├── quality.png
└── analysis.png
```

![نمای Swagger](screenshots/swagger-overview.png)

---

## ۲۴. عیب‌یابی رایج

| مشکل | راه‌حل پیشنهادی |
| --- | --- |
| `ModuleNotFoundError` | `pip install ".[dev]"` داخل venv |
| پورت ۸۰۰۰ اشغال است | `--port 8001` یا Kill کردن پروسه قبلی |
| `DATASET_NOT_CLEANED` | اول `/clean` را صدا بزنید |
| آپلود Excel شکست می‌خورد | مطمئن شوید `openpyxl` نصب است |
| فایل خیلی بزرگ | `MAX_FILE_SIZE` را در `.env` تنظیم کنید |
| تست‌ها به storage اصلی می‌نویسند | Fixtureها از tmp path استفاده می‌کنند؛ دوباره `pytest` را اجرا کنید |
| Docker پیدا نمی‌شود | از اجرای محلی Uvicorn استفاده کنید |

---

## ۲۵. بهبودهای آینده

- احراز هویت JWT / OAuth2
- PostgreSQL برای Production
- Celery / Redis برای فایل‌های بزرگ
- ذخیره در S3-compatible storage
- Profiling پیشرفته (Correlation و Distribution)
- Dashboard ویژوال
- قوانین Cleaning سفارشی توسط کاربر
- Schema Validation قراردادی
- Anomaly Detection مبتنی بر ML
- Versioning نسخه‌های مختلف Dataset

---

## ۲۶. معیار پذیرش و Definition of Done

پروژه وقتی کامل محسوب می‌شود که:

1. همه APIهای الزامی پیاده‌سازی شده باشند
2. Upload CSV/Excel کار کند
3. Profiling کامل باشد
4. Cleaning Pipeline فعال و Configurable باشد
5. Quality Score محاسبه شود
6. Analysis روی داده پاک‌شده کار کند
7. Download نسخه Clean ممکن باشد
8. Persistence با SQLAlchemy برقرار باشد
9. Error Handling استاندارد باشد
10. حداقل ۲۰ تست موفق وجود داشته باشد
11. Dockerfile و docker-compose موجود باشند
12. Swagger کامل باشد
13. README حرفه‌ای (انگلیسی و فارسی) موجود باشد
14. Sample Dataset و Screenshots در ریپو باشند
15. Secret داخل Git نباشد

### وزن پیشنهادی ارزیابی

| بخش | وزن |
| --- | --- |
| Architecture & Design | ۱۵٪ |
| API Implementation | ۱۵٪ |
| Data Cleaning Logic | ۲۰٪ |
| Profiling & Analysis | ۱۰٪ |
| Database Design | ۱۰٪ |
| Testing | ۱۵٪ |
| Docker & Deployment | ۵٪ |
| Documentation | ۵٪ |
| Git/GitHub Quality | ۵٪ |

---

## ۲۷. مجوز

این پروژه تحت مجوز **MIT** منتشر شده است. جزئیات در فایل [`LICENSE`](LICENSE).

---

## جمع‌بندی یک‌خطی

**Smart Data Cleaning & Analysis API** یک Backend تولیدی‌سبک برای تبدیل Dataset خام به داده پاک، امتیازدهی‌شده و قابل‌تحلیل است؛ با معماری تمیز، تست واقعی، Docker، و مستندات فارسی/انگلیسی کامل.

برای شروع سریع:

```bash
python -m venv .venv && source .venv/bin/activate
pip install ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

سپس مرورگر را باز کنید:

```text
http://localhost:8000/docs
```
