# Product Requirements Document (PRD)

## Smart Data Cleaning & Analysis API

**Version:** 1.0.0
**Status:** Ready for Development
**Project Type:** Final / Portfolio Project
**Backend:** Python + FastAPI
**Database:** SQLite / PostgreSQL
**Containerization:** Docker
**Testing:** Pytest
**Documentation:** OpenAPI / Swagger
**Repository:** GitHub

---

# 1. Product Overview

## 1.1 Product Name

**Smart Data Cleaning & Analysis API**

## 1.2 Product Vision

ساخت یک RESTful API حرفه‌ای برای دریافت Datasetهای خام و دارای خطا و تبدیل آن‌ها به Datasetهای ساختاریافته، پاک‌شده و قابل تحلیل.

سیستم باید یک Pipeline کامل Data Processing ارائه دهد:

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

هدف پروژه صرفاً پیاده‌سازی چند endpoint نیست؛ بلکه باید یک سیستم Backend واقعی با:

* معماری چندلایه
* Separation of Concerns
* Clean Code
* تست‌پذیری
* مدیریت خطا
* Database Persistence
* Configuration Management
* Dockerization
* API Documentation
* Version Control
* مستندات حرفه‌ای

ارائه شود.

---

# 2. Problem Statement

در بسیاری از پروژه‌های Data Science و Business Intelligence، Dataset اولیه معمولاً مشکلاتی مانند موارد زیر دارد:

* Missing Values
* Duplicate Records
* Inconsistent Text
* Invalid Values
* Incorrect Data Types
* Outliers
* Formatting Errors
* Inconsistent Categories
* Empty Rows/Columns

اگر این مشکلات قبل از تحلیل برطرف نشوند، خروجی تحلیل می‌تواند نادرست یا گمراه‌کننده باشد.

هدف این پروژه ایجاد یک سرویس مستقل است که بتواند Dataset را دریافت کرده، کیفیت آن را ارزیابی کند، مشکلات رایج را شناسایی و در صورت امکان اصلاح کند و در نهایت Dataset پاک‌شده و گزارش تحلیلی قابل استفاده تولید کند.

---

# 3. Goals

## 3.1 Primary Goals

سیستم باید بتواند:

1. فایل CSV و Excel دریافت کند.
2. فایل را Validation کند.
3. Dataset را در Database ثبت کند.
4. Dataset را Profile کند.
5. مشکلات داده را شناسایی کند.
6. Cleaning را بر اساس Configuration انجام دهد.
7. Before/After Dataset را مقایسه کند.
8. Data Quality Score محاسبه کند.
9. Dataset را تحلیل کند.
10. Dataset پاک‌شده را برای Download ارائه دهد.
11. عملیات مهم را در Database ثبت کند.
12. خطاها را به شکل استاندارد مدیریت کند.
13. API را با Swagger/OpenAPI مستند کند.
14. حداقل 20 تست واقعی داشته باشد.
15. به‌صورت کامل با Docker قابل اجرا باشد.

---

# 4. Non-Goals

نسخه اول پروژه قرار نیست موارد زیر را پیاده‌سازی کند:

* Machine Learning خودکار
* Data Warehouse
* Distributed Processing
* Real-time Streaming
* User Authentication پیچیده
* Multi-tenant Architecture
* Cloud Deployment اجباری
* Natural Language Query
* Automatic Schema Discovery پیشرفته
* Data Visualization Dashboard مستقل

این موارد می‌توانند در Future Improvements قرار بگیرند.

---

# 5. Target Users

## 5.1 Data Analyst

کاربر می‌تواند Dataset خام خود را Upload کرده و قبل از تحلیل، کیفیت و مشکلات داده را بررسی کند.

## 5.2 Data Scientist

می‌تواند از Pipeline آماده برای Data Preprocessing اولیه استفاده کند.

## 5.3 Backend Developer

می‌تواند معماری پروژه را بررسی و توسعه دهد.

## 5.4 Reviewer / Instructor

باید بتواند پروژه را Clone کرده، اجرا کند، APIها را تست کند و کیفیت معماری، تست‌ها و مستندات را ارزیابی کند.

---

# 6. User Journey

سناریوی اصلی سیستم:

```text
User
 │
 ├── Upload Dataset
 │
 ▼
File Validation
 │
 ▼
Dataset Registration
 │
 ▼
Initial Profiling
 │
 ▼
User Reviews Profile
 │
 ▼
Cleaning Configuration
 │
 ▼
Cleaning Pipeline
 │
 ▼
Quality Assessment
 │
 ▼
Analysis
 │
 ▼
Download Clean Dataset
```

---

# 7. Functional Requirements

# 7.1 Dataset Upload

### Endpoint

```http
POST /datasets/upload
```

### Supported Formats

* CSV
* XLSX
* XLS در صورت پشتیبانی کتابخانه/محیط

### Upload Requirements

سیستم باید:

* Extension فایل را بررسی کند.
* MIME Type را تا حد امکان Validation کند.
* File Size را محدود کند.
* Empty File را رد کند.
* فایل خراب را تشخیص دهد.
* Dataset دارای Header را بررسی کند.
* Dataset را Parse کند.
* تعداد Rows و Columns را محاسبه کند.
* Dataset ID یکتا ایجاد کند.
* Metadata را در Database ذخیره کند.
* فایل خام را در Storage محلی پروژه نگهداری کند.

### Suggested File Size Limit

```text
Maximum: 50 MB
```

این مقدار باید قابل Configuration باشد.

### Success Response

```json
{
  "dataset_id": 101,
  "filename": "customers_dirty.xlsx",
  "file_type": "xlsx",
  "rows": 12500,
  "columns": 8,
  "status": "uploaded"
}
```

### HTTP Status

```text
201 Created
```

---

# 7.2 Dataset Listing

### Endpoint

```http
GET /datasets
```

کاربر باید بتواند Datasetهای ثبت‌شده را مشاهده کند.

### Requirements

خروجی باید حداقل شامل:

* ID
* Filename
* File Type
* Rows
* Columns
* Status
* Created At
* Updated At

باشد.

### Pagination

API باید از Pagination پشتیبانی کند.

Example:

```http
GET /datasets?page=1&page_size=20
```

---

# 7.3 Dataset Details

### Endpoint

```http
GET /datasets/{dataset_id}
```

اطلاعات کامل Dataset را برمی‌گرداند.

اگر Dataset وجود نداشته باشد:

```http
404 Not Found
```

---

# 7.4 Dataset Profiling

### Endpoint

```http
GET /datasets/{dataset_id}/profile
```

هدف این endpoint ارائه تصویری از وضعیت Dataset قبل از Cleaning است.

## Required Dataset-Level Metrics

* Number of Rows
* Number of Columns
* Duplicate Rows
* Total Missing Values
* Total Invalid Values

## Required Column-Level Metrics

برای هر ستون:

* Column Name
* Data Type
* Missing Count
* Missing Percentage
* Unique Count
* Unique Percentage
* Minimum
* Maximum
* Mean
* Median
* Standard Deviation

برای ستون‌های غیرعددی، Metrics نامرتبط می‌توانند `null` باشند.

### Example

```json
{
  "dataset_id": 101,
  "rows": 1000,
  "columns": 8,
  "duplicate_rows": 25,
  "total_missing_values": 42,
  "columns_profile": [
    {
      "name": "age",
      "dtype": "int64",
      "missing_count": 5,
      "missing_percentage": 0.5,
      "unique_count": 73,
      "min": 18,
      "max": 92,
      "mean": 39.8,
      "median": 37,
      "std": 14.2
    }
  ]
}
```

---

# 7.5 Data Cleaning

### Endpoint

```http
POST /datasets/{dataset_id}/clean
```

Cleaning باید Configuration-driven باشد و تمام عملیات به‌صورت Hard-coded اجرا نشوند.

### Request

```json
{
  "remove_duplicates": true,
  "fill_missing": true,
  "normalize_text": true,
  "validate_values": true,
  "detect_outliers": true
}
```

---

# 8. Cleaning Pipeline

Cleaning Pipeline باید دارای مراحل مشخص و قابل تست باشد.

ترتیب پیشنهادی:

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
Outlier Detection
     ↓
Final Validation
     ↓
Save Clean Dataset
     ↓
Generate Quality Report
```

---

# 9. Missing Value Strategy

## 9.1 Numeric Columns

در حالت پیش‌فرض:

```text
Missing → Median
```

دلیل استفاده از Median این است که نسبت به Outlierها مقاوم‌تر از Mean است.

## 9.2 Categorical/Text Columns

در حالت پیش‌فرض:

```text
Missing → Mode
```

## 9.3 Completely Empty Columns

اگر ستونی 100٪ Missing باشد، سیستم باید آن را به‌عنوان ستون مشکل‌دار گزارش کند.

رفتار پیش‌فرض پیشنهادی:

```text
Do not automatically delete
```

بلکه در Quality Report ثبت شود.

## 9.4 Configuration

Strategy باید قابل توسعه باشد.

مثلاً:

```json
{
  "fill_missing": true,
  "numeric_strategy": "median",
  "categorical_strategy": "mode"
}
```

---

# 10. Duplicate Detection

سیستم باید Duplicate Rows را شناسایی و در صورت فعال بودن گزینه:

```json
{
  "remove_duplicates": true
}
```

حذف کند.

### Requirements

* تعداد Duplicateهای قبل از Cleaning ثبت شود.
* تعداد حذف‌شده ثبت شود.
* Dataset بعد از Cleaning دوباره بررسی شود.
* Duplicate Count بعد از Cleaning در صورت فعال بودن گزینه باید صفر باشد.

---

# 11. Text Normalization

هدف این بخش تبدیل مقادیر متنی مشابه به یک مقدار استاندارد است.

### Example

ورودی:

```text
tehran
Tehran
TEHRAN
 Tehran
tehran 
```

خروجی:

```text
Tehran
```

### Normalization Steps

حداقل:

1. Trim whitespace
2. Normalize repeated spaces
3. Case normalization
4. Category standardization

### Recommended Approach

برای مقادیر categorical پرتکرار، سیستم می‌تواند از canonical mapping استفاده کند.

Example:

```python
{
    "tehran": "Tehran",
    "TEHRAN": "Tehran",
    "tehran ": "Tehran"
}
```

### Important Requirement

Text normalization نباید به‌صورت کورکورانه روی تمام ستون‌ها اعمال شود.

برای مثال Email و ID ممکن است قواعد متفاوتی داشته باشند.

---

# 12. Email Validation

در صورت شناسایی ستون‌های Email، سیستم می‌تواند Format Validation انجام دهد.

Example:

```text
valid@example.com
```

معتبر است.

اما:

```text
invalid-email
```

نامعتبر است.

سیستم باید Invalid Email را گزارش کند.

در نسخه اول، Validation ساده کافی است و نیاز به Email Verification واقعی وجود ندارد.

---

# 13. Invalid Value Detection

سیستم باید امکان تعریف Rules برای داده‌های غیرمنطقی داشته باشد.

### Example: Age

Valid Range:

```text
0 <= age <= 120
```

بنابراین:

```text
-10
250
```

Invalid هستند.

### Example Rules

برای Dataset نمونه:

| Column   | Rule               |
| -------- | ------------------ |
| age      | 0–120              |
| salary   | >= 0               |
| quantity | >= 0               |
| email    | valid email format |
| date     | valid date         |

Rules باید در یک بخش مشخص از Service Layer پیاده‌سازی شوند تا توسعه آن‌ها ساده باشد.

---

# 14. Outlier Detection

حداقل یک روش آماری باید پیاده‌سازی شود.

## Required Method

### IQR Method

فرمول:

```text
IQR = Q3 - Q1
```

Lower Bound:

```text
Q1 - 1.5 × IQR
```

Upper Bound:

```text
Q3 + 1.5 × IQR
```

هر مقدار خارج از این محدوده به‌عنوان Outlier علامت‌گذاری می‌شود.

### Important

در نسخه اول:

**Outlier الزاماً حذف نشود.**

بهتر است ابتدا به‌عنوان کیفیت/هشدار گزارش شود.

این تصمیم باید در README توضیح داده شود.

---

# 15. Cleaning Result

Response عملیات Cleaning باید شامل Summary باشد.

Example:

```json
{
  "dataset_id": 101,
  "status": "cleaned",
  "rows_before": 12500,
  "rows_after": 12455,
  "duplicates_removed": 45,
  "missing_values_filled": 132,
  "invalid_values_detected": 7,
  "outliers_detected": 23
}
```

---

# 16. Cleaning History

هر عملیات Cleaning باید در Database ثبت شود.

حداقل:

* Cleaning ID
* Dataset ID
* Configuration
* Rows Before
* Rows After
* Duplicates Removed
* Missing Values Filled
* Invalid Values
* Outliers
* Created At
* Status

این قابلیت امکان Audit و بررسی Pipeline را فراهم می‌کند.

---

# 17. Data Quality Report

### Endpoint

```http
GET /datasets/{dataset_id}/quality
```

گزارش باید وضعیت Dataset را قبل و بعد از Cleaning مقایسه کند.

### Example

```json
{
  "dataset_id": 101,
  "before": {
    "rows": 12500,
    "missing_values": 132,
    "duplicates": 45,
    "invalid_values": 7
  },
  "after": {
    "rows": 12455,
    "missing_values": 12,
    "duplicates": 0,
    "invalid_values": 0
  },
  "quality_score": 94.7
}
```

---

# 18. Data Quality Score

سیستم باید یک Score بین 0 تا 100 تولید کند.

## Proposed Formula

Score از چهار مؤلفه تشکیل شود:

```text
Missing Score
Duplicate Score
Invalid Score
Consistency Score
```

مثلاً:

```text
Final Score =
    30% Missing Score
  + 25% Duplicate Score
  + 25% Invalid Value Score
  + 20% Consistency Score
```

هر component بین 0 تا 100 باشد.

### Missing Score

هرچه درصد Missing کمتر باشد، امتیاز بیشتر است.

### Duplicate Score

هرچه درصد Duplicate کمتر باشد، امتیاز بیشتر است.

### Invalid Score

هرچه تعداد Invalid کمتر باشد، امتیاز بیشتر است.

### Consistency Score

مواردی مانند:

* inconsistent categories
* malformed emails
* invalid formats

در این بخش لحاظ شوند.

### Constraints

```text
0 <= Quality Score <= 100
```

Score نباید به دلیل خطای محاسباتی از این محدوده خارج شود.

---

# 19. Quality Score Interpretation

| Score  | Interpretation |
| ------ | -------------- |
| 90–100 | Excellent      |
| 75–89  | Good           |
| 60–74  | Fair           |
| 40–59  | Poor           |
| 0–39   | Critical       |

این دسته‌بندی باید در README مستند شود.

---

# 20. Data Analysis

### Endpoint

```http
GET /datasets/{dataset_id}/analysis
```

Analysis فقط روی Dataset پاک‌شده انجام شود.

اگر Dataset هنوز Cleaning نشده باشد، سیستم باید Response مناسبی برگرداند یا رفتار آن در API Documentation به‌وضوح مشخص شود.

---

# 21. Numeric Analysis

برای Numeric Columns:

* Count
* Mean
* Median
* Minimum
* Maximum
* Standard Deviation
* Percentiles

مثلاً:

```json
{
  "age": {
    "count": 12455,
    "mean": 38.4,
    "median": 36,
    "min": 18,
    "max": 82,
    "std": 11.7
  }
}
```

---

# 22. Categorical Analysis

برای Categorical Columns:

* Unique Count
* Top Categories
* Frequency
* Percentage

Example:

```json
{
  "city": {
    "unique_count": 12,
    "top_categories": [
      {
        "value": "Tehran",
        "count": 4200,
        "percentage": 33.7
      },
      {
        "value": "Shiraz",
        "count": 1800,
        "percentage": 14.4
      }
    ]
  }
}
```

---

# 23. Dataset-Specific Business Analysis

Dataset نمونه بهتر است یک Dataset فروش/مشتری باشد تا امکان تحلیل Business-oriented نیز وجود داشته باشد.

در صورت وجود ستون‌های مناسب، سیستم می‌تواند موارد زیر را محاسبه کند:

* Total Sales
* Average Sales
* Top Products
* Top Customers
* Sales by Region
* Monthly Sales

این تحلیل‌ها باید Conditional باشند.

یعنی اگر Dataset ستون‌های مربوطه را نداشت، API نباید Crash کند.

---

# 24. Download

### Endpoint

```http
GET /datasets/{dataset_id}/download
```

کاربر باید Dataset پاک‌شده را دریافت کند.

### Supported Output

حداقل:

```text
CSV
```

و ترجیحاً:

```text
Excel
```

### Requirements

* Filename مناسب باشد.
* Content-Type صحیح باشد.
* Dataset دانلودشده باید نسخه Clean شده باشد.

---

# 25. Delete Dataset

### Endpoint

```http
DELETE /datasets/{dataset_id}
```

حذف باید:

* Database Record
* Raw File
* Cleaned File
* Cleaning History مرتبط

را مدیریت کند.

### Success

```http
204 No Content
```

یا در صورت نیاز:

```http
200 OK
```

---

# 26. API Endpoints

| Method | Endpoint                  | Purpose                |
| ------ | ------------------------- | ---------------------- |
| POST   | `/datasets/upload`        | Upload Dataset         |
| GET    | `/datasets`               | List Datasets          |
| GET    | `/datasets/{id}`          | Dataset Details        |
| GET    | `/datasets/{id}/profile`  | Dataset Profiling      |
| POST   | `/datasets/{id}/clean`    | Run Cleaning           |
| GET    | `/datasets/{id}/quality`  | Quality Report         |
| GET    | `/datasets/{id}/analysis` | Data Analysis          |
| GET    | `/datasets/{id}/download` | Download Clean Dataset |
| DELETE | `/datasets/{id}`          | Delete Dataset         |

---

# 27. API Error Handling

تمام Errorها باید استاندارد باشند.

### Standard Error Response

```json
{
  "error": {
    "code": "DATASET_NOT_FOUND",
    "message": "Dataset with id 101 was not found."
  }
}
```

### Error Codes

پیشنهاد:

```text
INVALID_FILE_TYPE
FILE_TOO_LARGE
EMPTY_FILE
INVALID_DATASET
DATASET_NOT_FOUND
DATASET_NOT_CLEANED
PROCESSING_ERROR
INVALID_CLEANING_CONFIGURATION
UNSUPPORTED_OPERATION
```

### HTTP Status Mapping

| Status | Use Case              |
| ------ | --------------------- |
| 400    | Bad Request           |
| 404    | Resource Not Found    |
| 413    | File Too Large        |
| 422    | Validation Error      |
| 500    | Internal Server Error |

Internal Python Exceptions نباید مستقیماً به Client نمایش داده شوند.

---

# 28. Database Requirements

Database:

```text
SQLite
```

برای Local Development و Evaluation مناسب است.

ساختار باید به‌گونه‌ای باشد که Migration به PostgreSQL در آینده ساده باشد.

ORM:

```text
SQLAlchemy
```

---

# 29. Dataset Model

Table:

```text
datasets
```

Fields:

| Field         | Type     | Description        |
| ------------- | -------- | ------------------ |
| id            | Integer  | Primary Key        |
| filename      | String   | Original filename  |
| file_type     | String   | csv/xlsx           |
| original_path | String   | Raw file path      |
| cleaned_path  | String   | Clean file path    |
| rows          | Integer  | Original row count |
| columns       | Integer  | Column count       |
| status        | String   | Dataset status     |
| created_at    | DateTime | Creation timestamp |
| updated_at    | DateTime | Last update        |

---

# 30. Cleaning Operation Model

Table:

```text
cleaning_operations
```

Fields:

| Field                   | Type        |
| ----------------------- | ----------- |
| id                      | Integer     |
| dataset_id              | Foreign Key |
| configuration           | JSON/Text   |
| rows_before             | Integer     |
| rows_after              | Integer     |
| duplicates_removed      | Integer     |
| missing_values_filled   | Integer     |
| invalid_values_detected | Integer     |
| outliers_detected       | Integer     |
| status                  | String      |
| created_at              | DateTime    |

---

# 31. Dataset Status

Dataset باید State مشخص داشته باشد.

پیشنهاد:

```text
UPLOADED
PROFILED
CLEANING
CLEANED
FAILED
DELETED
```

State Transition:

```text
UPLOADED
   ↓
PROFILED
   ↓
CLEANING
   ↓
CLEANED
```

در صورت Error:

```text
UPLOADED → FAILED
```

---

# 32. Project Architecture

معماری پیشنهادی:

```text
smart-data-api/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── datasets.py
│   │   └── analysis.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── models/
│   │   ├── dataset.py
│   │   └── cleaning.py
│   │
│   ├── schemas/
│   │   ├── dataset.py
│   │   ├── cleaning.py
│   │   ├── profile.py
│   │   ├── quality.py
│   │   └── analysis.py
│   │
│   ├── services/
│   │   ├── file_handler.py
│   │   ├── profiler.py
│   │   ├── cleaner.py
│   │   ├── validator.py
│   │   ├── analyzer.py
│   │   └── quality.py
│   │
│   └── utils/
│       ├── constants.py
│       └── helpers.py
│
├── tests/
│   ├── conftest.py
│   ├── test_upload.py
│   ├── test_validation.py
│   ├── test_profiling.py
│   ├── test_cleaning.py
│   ├── test_quality.py
│   ├── test_analysis.py
│   ├── test_download.py
│   └── test_database.py
│
├── sample_data/
│   └── customers_dirty.csv
│
├── storage/
│   ├── raw/
│   └── cleaned/
│
├── screenshots/
│   ├── swagger.png
│   ├── upload.png
│   ├── profile.png
│   └── quality.png
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

---

# 33. Layer Responsibilities

## API Layer

مسئول:

* HTTP Request
* HTTP Response
* Dependency Injection
* Input Validation

نباید شامل Business Logic سنگین باشد.

## Service Layer

مسئول:

* Profiling
* Cleaning
* Analysis
* Quality Calculation
* File Processing

## Repository / Database Layer

مسئول:

* CRUD
* Persistence
* Queries

## Schema Layer

مسئول:

* Pydantic Models
* Request Validation
* Response Serialization

---

# 34. Technology Stack

## Required

```text
Python 3.11+
FastAPI
Pandas
NumPy
Pydantic
SQLAlchemy
SQLite
Pytest
Docker
Git
GitHub
```

## Recommended

```text
Uvicorn
openpyxl
httpx
python-multipart
pytest-cov
ruff
```

در صورت نیاز:

```text
Alembic
```

برای Database Migration.

---

# 35. Dependency Management

مدیریت Dependencyها باید با:

```text
pyproject.toml
```

انجام شود.

از نصب دستی Libraryها بدون ثبت آن‌ها در پروژه جلوگیری شود.

---

# 36. Configuration

Configuration نباید Hard-coded باشد.

موارد پیشنهادی:

```text
DATABASE_URL
MAX_FILE_SIZE
STORAGE_PATH
ALLOWED_EXTENSIONS
ENVIRONMENT
LOG_LEVEL
```

Example:

```env
DATABASE_URL=sqlite:///./smart_data.db
MAX_FILE_SIZE=52428800
STORAGE_PATH=./storage
ENVIRONMENT=development
LOG_LEVEL=INFO
```

فایل:

```text
.env
```

نباید Commit شود.

باید:

```text
.env.example
```

در Repository قرار گیرد.

---

# 37. Security Requirements

حتی اگر Authentication در Scope نسخه اول نیست، موارد زیر باید رعایت شوند:

* محدودیت حجم فایل
* Whitelist Extension
* جلوگیری از Path Traversal
* عدم استفاده مستقیم از Filename برای ساخت مسیر ناامن
* Validation فایل
* عدم نمایش Stack Trace
* عدم ذخیره Secret در Git
* مدیریت مناسب Temporary Files

---

# 38. Logging

سیستم باید Logging استاندارد داشته باشد.

حداقل Eventها:

* Application startup
* File upload
* Cleaning started
* Cleaning completed
* Processing error
* Dataset deletion

Log نباید اطلاعات حساس Dataset را بی‌دلیل چاپ کند.

---

# 39. Testing Strategy

حداقل:

```text
20 tests
```

اما هدف بهتر:

```text
25–35 meaningful tests
```

---

# 40. Required Test Coverage

## Upload

* Valid CSV upload
* Valid Excel upload
* Invalid extension
* Empty file
* File too large
* Malformed file

## Validation

* Invalid age
* Invalid email
* Unsupported file

## Profiling

* Row count
* Column count
* Missing values
* Duplicate count
* Numeric statistics
* Categorical statistics

## Cleaning

* Duplicate removal
* Numeric missing value filling
* Categorical missing value filling
* Text normalization
* Invalid value detection
* Outlier detection

## Quality

* Quality score range
* Quality score calculation
* Before/After comparison

## Analysis

* Numeric analysis
* Categorical analysis
* Dataset-specific analysis

## Download

* Clean file download
* Missing dataset download error

## Database

* Dataset creation
* Dataset retrieval
* Dataset deletion
* Cleaning operation persistence

## API Errors

* 404
* 422
* 400
* Processing error

---

# 41. Testing Tools

پیشنهاد:

```text
pytest
pytest-cov
httpx
FastAPI TestClient
```

تست‌ها باید تا حد امکان مستقل باشند.

Database تست باید از Database اصلی پروژه جدا باشد.

---

# 42. Test Quality

صرفاً افزایش تعداد Test قابل قبول نیست.

هر Test باید:

* هدف مشخص داشته باشد.
* نام معنادار داشته باشد.
* یک رفتار مشخص را بررسی کند.
* قابل تکرار باشد.
* وابسته به Test دیگر نباشد.

Example:

```text
test_cleaner_fills_numeric_missing_values_with_median
```

بهتر از:

```text
test_cleaning_1
```

است.

---

# 43. Docker Requirements

پروژه باید با Docker اجرا شود.

## Dockerfile

باید:

* Python Base Image مناسب داشته باشد.
* Dependencies را نصب کند.
* Application را اجرا کند.
* Port را expose کند.

مثلاً:

```text
8000
```

## Docker Compose

پیشنهاد:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./storage:/app/storage
      - ./smart_data.db:/app/smart_data.db
```

---

# 44. Local Execution

کاربر باید بتواند پروژه را بدون Docker نیز اجرا کند.

Example:

```bash
git clone <repository>
cd smart-data-api

python -m venv .venv

source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

سپس:

```bash
pip install .
```

و:

```bash
uvicorn app.main:app --reload
```

---

# 45. Docker Execution

اجرای پروژه باید تا حد امکان ساده باشد:

```bash
docker compose up --build
```

پس از اجرا:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 46. API Documentation

FastAPI باید OpenAPI Documentation تولید کند.

Documentation باید شامل:

* Endpoint Description
* Request Body
* Response Schema
* HTTP Status Codes
* Error Responses
* Example Payloads

باشد.

Swagger UI باید بدون نیاز به ابزار خارجی قابل استفاده باشد.

---

# 47. Sample Dataset

پروژه باید Dataset واقعی‌نما داشته باشد.

نام پیشنهادی:

```text
customers_dirty.csv
```

حداقل ستون‌ها:

```text
customer_id
name
email
age
city
region
product
quantity
unit_price
total_sales
date
```

Dataset باید عمداً شامل موارد زیر باشد:

### Missing Values

```text
age = null
email = null
city = null
```

### Duplicate Rows

حداقل چند Row تکراری.

### Inconsistent Text

```text
Tehran
tehran
TEHRAN
 Tehran
```

### Invalid Values

```text
age = -5
age = 250
quantity = -2
unit_price = -100
```

### Outliers

مثلاً:

```text
normal salary/sales values
+
one extremely large value
```

### Formatting Errors

مثلاً:

```text
2026-01-01
01/02/2026
2026/03/10
```

---

# 48. Sample Dataset Size

برای Repository بهتر است Dataset نمونه کوچک باشد:

```text
500–2,000 rows
```

تا:

* GitHub Repository سنگین نشود.
* تست‌ها سریع اجرا شوند.
* Demo آسان باشد.

---

# 49. Performance Requirements

نسخه اول برای Datasetهای متوسط طراحی می‌شود.

Target:

```text
<= 50 MB file
```

سیستم باید برای Dataset نمونه در زمان معقول پاسخ دهد.

از نگه‌داشتن DataFrameهای بزرگ در Memory بیش از زمان لازم جلوگیری شود.

---

# 50. API Response Consistency

Responseهای API باید ساختار قابل پیش‌بینی داشته باشند.

تمام Responseهای اصلی باید Pydantic Schema داشته باشند.

از برگرداندن مستقیم Objectهای داخلی یا DataFrame خودداری شود.

---

# 51. Data Processing Principles

اصول اصلی:

### Principle 1 — Never silently modify data

سیستم باید بداند چه چیزی تغییر کرده است.

### Principle 2 — Keep original data

Raw Dataset نباید با Cleaned Dataset overwrite شود.

### Principle 3 — Make cleaning configurable

کاربر باید مشخص کند چه عملیات‌هایی اجرا شوند.

### Principle 4 — Make cleaning reproducible

با داشتن Dataset و Configuration یکسان، نتیجه باید تا حد امکان deterministic باشد.

### Principle 5 — Report everything

Cleaning باید Summary تولید کند.

---

# 52. Original vs Cleaned Files

سیستم باید دو نسخه را نگهداری کند:

```text
storage/
├── raw/
│   └── <dataset_id>_original.csv
│
└── cleaned/
    └── <dataset_id>_cleaned.csv
```

Dataset خام نباید حذف یا overwrite شود.

---

# 53. API Validation Rules

Pydantic باید برای Cleaning Configuration استفاده شود.

Example:

```json
{
  "remove_duplicates": true,
  "fill_missing": true,
  "normalize_text": true,
  "validate_values": true,
  "detect_outliers": true
}
```

مقادیر نامعتبر باید با:

```text
422 Unprocessable Entity
```

برگردانده شوند.

---

# 54. Architecture Quality Requirements

کد باید:

* Modular
* Testable
* Maintainable
* Readable
* Extensible

باشد.

موارد زیر قابل قبول نیست:

```text
❌ همه Logic در main.py
❌ SQL مستقیم داخل Routeها
❌ Data Cleaning داخل Endpoint
❌ Global DataFrame
❌ Hard-coded file paths
❌ Bare except
❌ تکرار شدید کد
❌ Functionهای بسیار بزرگ
```

---

# 55. Code Quality

پیشنهاد می‌شود:

* Type Hints
* Docstrings برای Logicهای مهم
* Meaningful Naming
* Small Functions
* Single Responsibility
* Dependency Injection

استفاده شود.

---

# 56. Git Strategy

Git History باید نشان دهد پروژه مرحله‌به‌مرحله توسعه یافته است.

Commitهای پیشنهادی:

```text
chore: initialize project structure
feat: add dataset upload endpoint
feat: add dataset validation
feat: implement dataset profiling
feat: add duplicate detection
feat: add missing value handling
feat: implement text normalization
feat: add invalid value validation
feat: implement IQR outlier detection
feat: add cleaning pipeline
feat: implement quality scoring
feat: add dataset analysis
feat: add cleaned dataset download
feat: add database persistence
test: add upload and validation tests
test: add cleaning service tests
test: add quality and analysis tests
docs: add API documentation
docs: add project README
chore: add Docker support
refactor: improve service layer separation
```

از Commitهای بی‌معنا مانند:

```text
update
final
changes
test
fix stuff
```

به‌عنوان Commit اصلی استفاده نشود.

---

# 57. GitHub Repository

Repository باید Public باشد مگر اینکه شرایط پروژه خلاف آن باشد.

Repository Name:

```text
smart-data-cleaning-api
```

Description پیشنهادی:

```text
A production-style FastAPI service for dataset validation,
profiling, cleaning, quality assessment, analysis, and export.
```

---

# 58. README Requirements

README باید شامل بخش‌های زیر باشد:

```text
# Smart Data Cleaning & Analysis API

## Project Overview

## Problem Statement

## Features

## Architecture

## Project Structure

## Technologies

## Installation

## Running Locally

## Running with Docker

## API Documentation

## API Endpoints

## Example Workflow

## Data Cleaning Strategy

## Data Quality Score

## Sample Dataset

## Testing

## Screenshots

## Error Handling

## Future Improvements

## License
```

---

# 59. README Example Workflow

README باید یک سناریوی کامل را نشان دهد:

### Step 1 — Upload

```http
POST /datasets/upload
```

### Step 2 — Profile

```http
GET /datasets/1/profile
```

### Step 3 — Clean

```http
POST /datasets/1/clean
```

### Step 4 — Quality

```http
GET /datasets/1/quality
```

### Step 5 — Analysis

```http
GET /datasets/1/analysis
```

### Step 6 — Download

```http
GET /datasets/1/download
```

---

# 60. Swagger Screenshots

حداقل Screenshots زیر در Repository قرار گیرند:

```text
screenshots/
├── swagger-overview.png
├── upload.png
├── profile.png
├── cleaning.png
├── quality.png
└── analysis.png
```

README باید این تصاویر را نمایش دهد.

---

# 61. Example End-to-End Scenario

ورودی:

```text
customers_dirty.csv
```

Dataset دارای:

```text
10,000 rows
12 columns
```

مشکلات:

```text
35 duplicate rows
120 missing values
8 invalid ages
17 inconsistent city names
12 outliers
```

پس از Cleaning:

```text
Rows:
10,000 → 9,965

Duplicates:
35 → 0

Missing:
120 → 15

Invalid:
8 → 0

Outliers:
12 detected
```

Quality:

```text
94.7 / 100
```

سپس کاربر می‌تواند:

```text
Analysis
+
Clean Dataset Download
```

را دریافت کند.

---

# 62. Observability

برای نسخه اول Logging کافی است.

اما Architecture باید به‌گونه‌ای باشد که در آینده بتوان موارد زیر را اضافه کرد:

* Metrics
* Prometheus
* Request IDs
* Structured Logging
* Monitoring

---

# 63. Future Improvements

موارد زیر می‌توانند در Future Roadmap قرار بگیرند:

### Authentication

JWT / OAuth2

### PostgreSQL

برای Production

### Background Processing

Celery / Redis برای Datasetهای بزرگ.

### Cloud Storage

S3-compatible storage.

### Advanced Profiling

Correlation Matrix و Distribution Analysis.

### Visualization

Charts و Dashboard.

### Custom Cleaning Rules

کاربر بتواند Rules دلخواه تعریف کند.

### Schema Validation

تعریف Schema برای Dataset.

### ML-based Anomaly Detection

Isolation Forest و سایر روش‌ها.

### Data Versioning

نگهداری Versionهای مختلف Dataset.

---

# 64. Acceptance Criteria

پروژه زمانی قابل قبول است که تمام موارد زیر برقرار باشند.

## Upload

* [ ] CSV قابل Upload باشد.
* [ ] Excel قابل Upload باشد.
* [ ] فایل نامعتبر Reject شود.
* [ ] محدودیت حجم وجود داشته باشد.
* [ ] Dataset در Database ثبت شود.
* [ ] Dataset ID ایجاد شود.

## Profiling

* [ ] Row count
* [ ] Column count
* [ ] Data types
* [ ] Missing values
* [ ] Missing percentages
* [ ] Unique counts
* [ ] Duplicate count
* [ ] Numeric statistics

## Cleaning

* [ ] Missing values handled
* [ ] Duplicates removed
* [ ] Text normalized
* [ ] Invalid values detected
* [ ] Outliers detected
* [ ] Cleaning configurable

## Quality

* [ ] Before/After report
* [ ] Score between 0 and 100
* [ ] Score documented

## Analysis

* [ ] Numeric analysis
* [ ] Categorical analysis
* [ ] Useful business analysis where applicable

## Download

* [ ] Clean Dataset downloadable
* [ ] Correct Content-Type
* [ ] Correct filename

## Database

* [ ] Dataset metadata persisted
* [ ] Cleaning operations persisted

## API

* [ ] Swagger available
* [ ] Correct HTTP status codes
* [ ] Standardized errors

## Testing

* [ ] Minimum 20 tests
* [ ] Core services covered
* [ ] API endpoints covered
* [ ] Database operations covered

## Docker

* [ ] Dockerfile exists
* [ ] docker-compose.yml exists
* [ ] `docker compose up --build` works

## GitHub

* [ ] Meaningful commit history
* [ ] Professional README
* [ ] Sample dataset
* [ ] Screenshots
* [ ] `.gitignore`
* [ ] `.env.example`

---

# 65. Definition of Done

Project فقط زمانی Done محسوب می‌شود که:

1. تمام Required APIها پیاده‌سازی شده باشند.
2. Upload CSV/Excel کار کند.
3. Dataset Profiling کامل باشد.
4. Cleaning Pipeline فعال باشد.
5. Cleaning Configuration از طریق API دریافت شود.
6. Quality Score محاسبه شود.
7. Analysis API کار کند.
8. Clean Dataset قابل Download باشد.
9. اطلاعات در SQLAlchemy Database ذخیره شوند.
10. Error Handling استاندارد باشد.
11. حداقل 20 تست موفق وجود داشته باشد.
12. Docker Build بدون Error انجام شود.
13. Docker Compose پروژه را اجرا کند.
14. Swagger کامل باشد.
15. README حرفه‌ای باشد.
16. Sample Dataset در Repository وجود داشته باشد.
17. Screenshots در README قرار گرفته باشند.
18. Git History شامل Commitهای معنادار باشد.
19. هیچ Secret یا فایل غیرضروری در Repository نباشد.
20. یک فرد جدید بتواند Repository را Clone کرده و با دنبال کردن README پروژه را اجرا کند.

---

# 66. Evaluation Criteria

پیشنهاد برای ارزیابی نهایی:

| بخش                           |      وزن |
| ----------------------------- | -------: |
| Architecture & Design         |      15% |
| API Implementation            |      15% |
| Data Cleaning Logic           |      20% |
| Data Profiling & Analysis     |      10% |
| Database Design               |      10% |
| Testing                       |      15% |
| Docker & Deployment Readiness |       5% |
| Documentation / README        |       5% |
| Git/GitHub Quality            |       5% |
| **Total**                     | **100%** |

---

# 67. Quality Bar

پروژه نباید صرفاً به‌عنوان یک پروژه دانشجویی حداقلی پیاده‌سازی شود.

معیار مطلوب:

```text
Student Project
        ↓
Clean Architecture
        ↓
Production-style API
        ↓
Testable Services
        ↓
Documented Decisions
        ↓
Professional GitHub Repository
```

تمرکز اصلی باید روی **کیفیت تصمیم‌های مهندسی** باشد، نه تعداد Libraryها.

---

# 68. Engineering Principles

اصول کلیدی پروژه:

```text
1. Separation of Concerns
2. Single Responsibility
3. Don't Repeat Yourself
4. Explicit Validation
5. Configuration over Hard-Coding
6. Preserve Original Data
7. Reproducible Cleaning
8. Test Critical Logic
9. Consistent API Contracts
10. Meaningful Error Handling
11. Documentation First
12. Clean Git History
```

---

# 69. Final Deliverable

خروجی نهایی باید یک GitHub Repository کامل باشد:

```text
smart-data-cleaning-api/
```

که پس از Clone بتوان آن را با یکی از روش‌های زیر اجرا کرد:

```bash
docker compose up --build
```

یا:

```bash
pip install .
uvicorn app.main:app --reload
```

و سپس API از طریق:

```text
http://localhost:8000/docs
```

در دسترس باشد.

کاربر باید بتواند این Workflow را بدون تغییر در Source Code اجرا کند:

```text
                    ┌──────────────┐
                    │ Upload CSV/XLSX │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  Validation  │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Profiling  │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Cleaning   │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │Quality Report│
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Analysis   │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Download   │
                    └──────────────┘
```

---

# 70. Final Product Statement

**Smart Data Cleaning & Analysis API** یک سرویس Backend برای تبدیل Dataset خام و دارای خطا به Dataset پاک‌شده، ارزیابی‌شده و قابل تحلیل است.

این پروژه باید نشان دهد که توسعه‌دهنده توانایی انجام یک چرخه کامل Software Engineering را دارد:

```text
Problem Analysis
      ↓
Requirements
      ↓
Architecture
      ↓
Implementation
      ↓
Data Processing
      ↓
Database Design
      ↓
Testing
      ↓
Containerization
      ↓
Documentation
      ↓
Git/GitHub Delivery
```

موفقیت پروژه فقط با «کار کردن API» سنجیده نمی‌شود؛ بلکه **معماری، کیفیت کد، قابلیت تست، منطق Data Cleaning، طراحی API، مدیریت خطا، مستندسازی و کیفیت Repository** بخش جدایی‌ناپذیر محصول نهایی هستند.
