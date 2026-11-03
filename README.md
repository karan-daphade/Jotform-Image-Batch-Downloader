# Jotform Image Batch Downloader

An automated Python script designed to parse Jotform (or form submission) export data from Excel (`images.xlsx`), validate image links, download the images, and systematically rename them based on sample and farmer identification codes.

---

## 📌 Features

- **Automated Batch Ingestion**: Reads records from an Excel workbook (`images.xlsx`).
- **Structured File Naming**: Saves images using the format `{Farmer Code}_{Sample Code}.{extension}` for organized archival and sample identification.
- **Header & Integrity Validation**:
  - Validates HTTP response status (`200 OK`).
  - Enforces minimum file size (> 1 KB) to prevent saving blank files or error payloads.
  - Inspects file magic bytes (JPEG `0xFF 0xD8 0xFF` and PNG magic bytes) to ensure received responses are genuine images and not HTML error pages.
- **Idempotency & Skip Support**: Automatically skips images that have already been downloaded to save bandwidth and execution time.
- **Audit Reports**:
  - `downloaded.csv`: Detailed log of successfully downloaded items.
  - `failed.csv`: Log of empty, failed, or invalid items for manual review and retries.

---

## 📂 Project Structure

```text
├── downloaded_images/    # Directory where images are saved
├── images.xlsx           # Source Excel file containing image URLs
├── p.py                  # Main execution script
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules for cached data and images
└── README.md             # Project documentation
```

---

## 📋 Excel Requirements

Your `images.xlsx` must contain at least the following column headers:

| Column Header | Description | Example |
| :--- | :--- | :--- |
| `Date` | Submission or collection date | `2026-01-15` |
| `Sample Code` | Identification code for the sample | `SMP-1042` |
| `Farmer Code` | Identification code for the farmer | `FRM-0089` |
| `Image` | Direct URL to the submitted image | `https://www.jotform.com/uploads/.../photo.jpg` |

> **Note**: If your column names differ (for example, `Submission Date`), rename the columns in Excel or adjust `required_cols` in `p.py`.

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python 3.8 or higher installed on your system.

### 2. Setup Virtual Environment (Recommended)

In your terminal or PowerShell:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Run the Script

Ensure your `images.xlsx` is placed in the project root folder, then execute:

```bash
python p.py
```

---

## ⚙️ Configuration

You can configure options directly at the top of [p.py](file:///d:/New%20folder/Jotform%20image/p.py):

```python
EXCEL_FILE = 'images.xlsx'       # Path to input Excel file
SHEET_NAME = 0                   # Sheet index or name
DOWNLOAD_DIR = 'downloaded_images' # Target output directory
DELAY_SECONDS = 0                # Pause between downloads (e.g. 0.5 to prevent rate limits)
```

---

## 📤 Moving This Project to GitHub

Follow these steps to initialize Git and push this repository to GitHub:

1. **Initialize Git repository**:
   ```bash
   git init
   ```

2. **Stage files and commit**:
   ```bash
   git add .
   git commit -m "Initial commit: Jotform image batch downloader"
   ```

3. **Create a new repository on GitHub**:
   - Go to [GitHub New Repository](https://github.com/new).
   - Enter your repository name (e.g., `jotform-image-downloader`).
   - Leave "Initialize this repository with a README" **unchecked** (we already have one).
   - Click **Create repository**.

4. **Link local repository and push**:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git
   git push -u origin main
   ```

> **Security Tip**: If your `images.xlsx` contains private or proprietary farmer details, you may want to exclude it from public repositories by uncommenting `images.xlsx` in [.gitignore](file:///d:/New%20folder/Jotform%20image/.gitignore) and providing an `images.example.xlsx` template instead.

