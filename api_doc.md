# CohortDB API Documentation

This document provides detailed information about the CohortDB API endpoints, designed for frontend integration.

---

## 1. Upload Data

- **Endpoint:** `/api/v1/data/upload`
- **Method:** `POST`
- **Description:** Uploads and processes two files: one with age-related data and another with quality control (QC) data. The server will parse these files and store the data in the database.

### Input

- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `ages_file` (file, required): The file containing the age and sample metadata.
  - `qc_file` (file, required): The Excel file containing various QC metrics across multiple sheets.

### Output

- **Success (200 OK):**
  ```json
  {
    "message": "Files uploaded and processed successfully"
  }
  ```
- **Error (500 Internal Server Error):**
  ```json
  {
    "detail": "A specific error message describing the issue during file processing."
  }
  ```

---

## 2. Download Data

- **Endpoint:** `/api/v1/data/download`
- **Method:** `GET`
- **Description:** Downloads an Excel file containing all associated data for a specified list of samples.

### Input

- **Query Parameters:**
  - `samples` (string, required): A comma-separated string of sample names to be included in the report.
    - **Example:** `?samples=sample1,sample2,sample3`

### Output

- **Success (200 OK):**
  - An Excel file (`.xlsx`) named `cohort_data.xlsx` is returned as a streaming response. The file will contain multiple sheets, each corresponding to a different data table (e.g., ReportedAges, BsRate, Coverage).
- **Error (500 Internal Server Error):**
  ```json
  {
    "detail": "A specific error message describing the issue."
  }
  ```

---

## 3. Filter Data

- **Endpoint:** `/api/v1/data/filter`
- **Method:** `POST`
- **Description:** Filters samples based on a set of criteria and returns all associated data for the matching samples.

### Input

- **Content-Type:** `application/json`
- **Body:** A JSON object that adheres to the `FilterSchema`.
  - **`filters`**: A dictionary where each key is a filterable field and its value is a two-element array `[operator, value]`.

- **Filterable Fields:**
  - `lambda_dna_conversion_rate` (float)
  - `pct_selected_bases` (float)
  - `fold_80_base_penalty` (float)
  - `percent_duplication` (float)

- **Supported Operators:**
  - `">="`: Greater than or equal to
  - `"<="`: Less than or equal to
  - `">"`: Greater than
  - `"<"`: Less than
  - `"=="`: Equal to

- **Example Request Body:**
  ```json
  {
    "filters": {
      "percent_duplication": ["<", 0.2],
      "lambda_dna_conversion_rate": [">=", 0.99]
    }
  }
  ```

### Output

- **Success (200 OK):**
  - A JSON object where each key corresponds to a data table name. The value for each key is an array of objects, with each object representing a sample's record from that table. All records belong to the samples that matched the filter criteria.

- **Example Response Body:**
  ```json
  {
    "ReportedAges": [
      {
        "sample": "sample1",
        "gender": "M",
        "age": 55,
        "cfdna": 0.12,
        "...": "..."
      }
    ],
    "BsRate": [
      {
        "sample": "sample1",
        "puc19vector": 0.98,
        "lambda_dna_conversion_rate": 0.995
      }
    ],
    "Coverage": [
      {
        "sample": "sample1",
        "pct_v2_sites_5x": 0.95,
        "...": "..."
      }
    ],
    "Fastp": [
        // ... array of Fastp records for matching samples
    ],
    "Markdup": [
        // ... array of Markdup records for matching samples
    ],
    "PicardAlignmentSummary": [
        // ... array of PicardAlignmentSummary records
    ],
    "PicardGcBias": [
        // ... array of PicardGcBias records
    ],
    "PicardGcBiasSummary": [
        // ... array of PicardGcBiasSummary records
    ],
    "PicardHs": [
        // ... array of PicardHs records
    ],
    "PicardInsertSize": [
        // ... array of PicardInsertSize records
    ],
    "PicardQualityYield": [
        // ... array of PicardQualityYield records
    ],
    "Screen": [
        // ... array of Screen records
    ]
  }
  ```

- **Error (500 Internal Server Error):**
  ```json
  {
    "detail": "A specific error message describing the issue."
  }
