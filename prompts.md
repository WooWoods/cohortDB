I am planning to build a database for my data, for the convenience of searching, browsing and downloading of sepcific samples, you can refer to @/raw_reportedAges.csv and @/methyl_qc.xlsx for my data, and for @/methyl_qc.xlsx, I have split it into seprate csv file in @/methyl_sheets, one csv file a sheet, the prefix is the sheet name. I suppose that each sheet saved in a table in the database, connected by "Sample", and the user could query by one or multi samples at a time, upon the backend recieved that query, it will retrieve  data from all the tables and generate a new xlsx file as the format of @/methyl_qc.xlsx for downloading. And we need an endpoint for adding data to database, it will accept raw_reportedAges.csv and methyl_qc.xlsx. comes with a plan to design the System Architecture of my project first

### System Architecture and Design Plan

This plan outlines a robust and scalable architecture for your project using modern, efficient technologies as per your preferences.

---

#### 1. Core Technology Stack

- __Backend Framework:__ __FastAPI__. It's a high-performance Python framework perfect for building APIs. Its automatic data validation and documentation features will accelerate development.
- __Database:__ __SQLite__ for initial development due to its simplicity (it's just a file). For production, I recommend __PostgreSQL__ for better scalability, concurrency, and robustness.
- __ORM (Object-Relational Mapper):__ __Peewee__, as you requested. It's a simple, expressive ORM that will work well with either SQLite or PostgreSQL.
- __Data Validation:__ __Pydantic__. It's integrated into FastAPI and allows for clear, type-hinted data validation for API requests.
- __Data Processing & Excel Handling:__ __Pandas__. It is the ideal tool for reading, parsing, and manipulating the data from your `.csv` and `.xlsx` files, and for generating the final Excel reports.

---

#### 2. Database Schema Design

The database will consist of multiple tables, one for each sheet in `methyl_qc.xlsx` and one for `raw_reportedAges.csv`. The `Sample` column will serve as the primary key or a unique identifier to link all tables.

__Table Naming and Column Cleanup:__ I recommend cleaning up the original column names to make them valid database identifiers (e.g., removing special characters and spaces).

Here is a proposed schema for a few of the tables:

1. __`ReportedAges` Table__ (from `raw_reportedAges.csv`)

   - `sample`: TEXT (Primary Key)
   - `gender`: TEXT
   - `age`: INTEGER
   - `sample_date`: DATE
   - ... and so on for the other columns.

2. __`BsRate` Table__ (from `bsrate.csv`)

   - `sample`: TEXT (Primary Key, Foreign Key to `ReportedAges.sample`)
   - `puc19_vector`: REAL
   - `lambda_dna_conversion_rate`: REAL

3. __`Coverage` Table__ (from `coverage.csv`)

   - `sample`: TEXT (Primary Key, Foreign Key to `ReportedAges.sample`)
   - `pct_v2_sites_5x`: REAL
   - `pct_v2_sites_15x`: REAL
   - ... and so on.

4. __`Fastp` Table__ (from `fastp.csv`)

   - __Note:__ This table requires special handling. Columns like `total_reads` contain two values separated by a `|`. I propose splitting these into two separate columns.
   - `sample`: TEXT (Primary Key, Foreign Key to `ReportedAges.sample`)
   - `total_reads_r1`: BIGINT
   - `total_reads_r2`: BIGINT
   - `total_bases_r1`: BIGINT
   - `total_bases_r2`: BIGINT
   - ... and so on for all pipe-separated columns.

This pattern will be repeated for all the CSV files in the `methyl_sheets` directory.

---

#### 3. API Endpoint Design

I suggest creating two main endpoints under a versioned API path (e.g., `/api/v1/`).

__A. Data Ingestion Endpoint__

- __Endpoint:__ `POST /api/v1/data/upload`

- __Request Format:__ `multipart/form-data`

- __Files:__

  1. `ages_file`: The `raw_reportedAges.csv` file.
  2. `qc_file`: The `methyl_qc.xlsx` file.

- __Workflow:__

  1. The endpoint receives the two files.
  2. __QC File Processing:__ It uses Pandas (`pd.ExcelFile`) to read the `methyl_qc.xlsx` file without loading it all into memory at once.
  3. It iterates through each sheet, cleans the column names, and uses the Peewee ORM to perform an "upsert" operation (update if the sample exists, insert if it doesn't) into the corresponding table.
  4. __Ages File Processing:__ It reads `raw_reportedAges.csv` and performs an "upsert" into the `ReportedAges` table.
  5. The process will be wrapped in a database transaction to ensure data integrity. If any sheet fails to process, the entire operation is rolled back.

- __Response:__ A JSON response indicating success or failure, including details about how many rows were added or updated.

__B. Data Query and Download Endpoint__

- __Endpoint:__ `GET /api/v1/data/download`

- __Query Parameters:__
  - `samples`: A comma-separated string of sample IDs (e.g., `?samples=CAP41WGS_MO026,CAP41WGS_MO028`).

- __Workflow:__

  1. The endpoint receives the list of sample IDs.
  2. It performs a database query for each sheet/table, selecting only the rows corresponding to the requested sample IDs.
  3. It uses Pandas to create an in-memory Excel file (`io.BytesIO`).
  4. For each table's data, it adds a sheet to the Excel file, ensuring the sheet names match the original `methyl_qc.xlsx`.
  5. It returns the Excel file as a `StreamingResponse` from FastAPI, which allows the user's browser to download it directly.

---

#### 4. Proposed Project Structure

A well-organized project structure is key for maintainability. I recommend the following:

```javascript
cohortDB/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app instance and API routers
│   ├── crud.py          # Database interaction logic (Create, Read, Update)
│   ├── database.py      # Database connection setup
│   ├── models.py        # Peewee ORM models (database schema)
│   ├── schemas.py       # Pydantic schemas (API data shapes)
│   └── services/
│       ├── __init__.py
│       └── file_handler.py # Logic for parsing uploads and generating downloads
├── requirements.txt     # Project dependencies
└── .env                 # Environment variables (e.g., database URL)
```

---

This architecture provides a solid foundation for your project. It is scalable, maintainable, and uses modern best practices.


the logic of upload file for frontend and backend are not keep in line. you should update front according to backend, keep backend as it is. the logic is that, backend "/data/upload" endpoint accept one file a time, and judge file type by its' suffix, so you don't need a `await uploadSingleFile(agesFile, "ages_file")` function in @/frontend/src/services/api.ts , just a `uploadData` function is enough, what ever the file is, leave that work to the backend, consider about this carefully

"INFO:     172.20.20.65:64079 - "POST /api/v1/data/upload HTTP/1.1" 500 Internal Server Error", error of backend, and I checked that problem may be at "ages_schema = schemas.ReportedAgesSchema(**row_data)", I guess if it is because of `nan` in some rows of upload file, which is acceptable, while the code of @/backend/schemas.py didn't handle the `nan`, review the backend code to solve this

The front-end data display logic needs to be modified. Currently, upon entering the page, it immediately requests "/data/filter", but at this point, the page's `filter` request is empty, so no data is displayed, leading to a poor user experience. The correct logic should be to display data upon entering the page, either by extracting the first 20 entries from the database or by dynamic loading, where more data is loaded as the user scrolls down the page. The "/data/filter" request should only be made when the user fills out the filter form.