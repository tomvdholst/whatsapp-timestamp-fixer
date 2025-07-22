# WhatsApp Timestamp Fixer

A Python script that restores the **DateTimeOriginal** EXIF metadata in images shared via by extracting the timestamp from its filename.

WhatsApp often removes photo metadata, but it encodes the original date/time in the filename. This script parses the filename, reconstructs the timestamp, and restores it to the image metadata.

---

## ✅ Features

- Supports .jpg and .jpeg files.
- Supports filename patterns:
  - `IMG-20210324-WA0001.jpg`
    - Time used is XXXX (for `-WAXXXX`) seconds after midnight to preserve correct order in timelines.
  - `WhatsApp Image 2021-03-24 at 19.52.18.jpeg`
- Supports `--dry-run`, `--verbose`, and `--quiet` modes
- Recursively processes all folders

---

## 🧰 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
