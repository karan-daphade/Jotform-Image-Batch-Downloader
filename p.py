import pandas as pd
import requests
import os
import time

# Configuration
EXCEL_FILE = 'images.xlsx'
SHEET_NAME = 0
DOWNLOAD_DIR = 'downloaded_images'
DELAY_SECONDS = 0  # Consider 0.5 if rate-limited

# Create download directory
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Read Excel file
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
print(f"Loaded {len(df)} rows from Excel.")

# Required columns
required_cols = ['Date', 'Sample Code', 'Farmer Code', 'Image']
if not all(col in df.columns for col in required_cols):
    print(f"Error: Excel must have columns: {required_cols}. Current columns: {list(df.columns)}")
    print("Tip: Rename columns in Excel if needed (e.g., 'Submission Date' to 'Date').")
    exit(1)

# Lists to track results
downloaded = []
failed = []

# Create session
session = requests.Session()

# Download loop
total = len(df)
for index, row in df.iterrows():
    sample_code = str(row['Sample Code']).strip()
    farmer_code = str(row['Farmer Code']).strip()
    link = str(row['Image']).strip()
    
    if not link or pd.isna(link):
        print(f"[{index+1}/{total}] Skipping empty link for Farmer {farmer_code}, Sample {sample_code}")
        failed.append({'Farmer Code': farmer_code, 'Sample Code': sample_code})
        continue
    
    # Dynamic filename extension from URL
    ext = link.split('.')[-1].split('?')[0].lower() if '.' in link else 'jpg'
    filename = f"{farmer_code}_{sample_code}.{ext}"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"[{index+1}/{total}] Already exists: {filename}")
        downloaded.append({'Farmer Code': farmer_code, 'Sample Code': sample_code})
        continue
    
    print(f"[{index+1}/{total}] Downloading {filename}...")
    
    try:
        response = session.get(link, timeout=30)  # No stream; load full content
        if response.status_code == 200:
            content = response.content
            content_size = len(content)
            if content_size > 1024:  # >1KB threshold
                # Check magic bytes for JPG/PNG
                is_jpg = content.startswith(b'\xff\xd8\xff')
                is_png = content[:4] == b'\x89PNG\r\n\x1a\n'  # Full PNG header
                if is_jpg or is_png:
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"  Success: Saved {filename} ({content_size} bytes)")
                    downloaded.append({'Farmer Code': farmer_code, 'Sample Code': sample_code})
                else:
                    print(f"  Failed: Not a valid image (magic bytes mismatch) for {link}")
                    print(f"    Debug: First 200 chars: {content[:200].decode('utf-8', errors='ignore')[:200]}")
                    failed.append({'Farmer Code': farmer_code, 'Sample Code': sample_code})
            else:
                print(f"  Failed: Response too small ({content_size} bytes) for {link}")
                print(f"    Debug: First 200 chars: {content.decode('utf-8', errors='ignore')[:200]}")
                failed.append({'Farmer Code': farmer_code, 'Sample Code': sample_code})
        else:
            print(f"  Failed: HTTP {response.status_code} for {link}")
            failed.append({'Farmer Code': farmer_code, 'Sample Code': sample_code})
    except Exception as e:
        print(f"  Failed: Exception {str(e)[:100]}... for {link}")
        failed.append({'Farmer Code': farmer_code, 'Sample Code': sample_code})
    
    time.sleep(DELAY_SECONDS)

# Generate CSVs
if downloaded:
    pd.DataFrame(downloaded).to_csv('downloaded.csv', index=False)
    print(f"Saved {len(downloaded)} entries to downloaded.csv")
if failed:
    pd.DataFrame(failed).to_csv('failed.csv', index=False)
    print(f"Saved {len(failed)} entries to failed.csv")

# Summary
print("\n=== SUMMARY ===")
print(f"Total attempted: {total}")
print(f"Downloaded: {len(downloaded)}")
print(f"Failed/Remaining: {len(failed)}")
if failed:
    print("Check failed.csv and console debug for details. Retry failed links manually.")