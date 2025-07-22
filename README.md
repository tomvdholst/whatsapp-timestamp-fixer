# WhatsApp Timestamp Fixer

A Python script that restores the **DateTimeOriginal** EXIF metadata in images shared via by extracting the timestamp from its filename.

WhatsApp often removes photo metadata, but it encodes the original date/time in the filename. This script parses the filename, reconstructs the timestamp, and restores it to the image metadata.

---

## ✅ Features

- Supports .jpg and .jpeg files.
- Supports filename patterns:
  - `WhatsApp Image 2021-03-24 at 19.52.18.jpeg`
  - `IMG-20210324-WA0001.jpg` - Time used is XXXX sec after midnight (for `-WAXXXX`) to preserve correct order in timelines.
- Supports `--dry-run`, `--verbose`, and `--quiet` modes
- Recursively processes all folders

---

## 🧰 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Usage


```bash
python whatsapp_timestamp_fixer.py [directory] [options]
```

If no directory is given, the current working directory is used.

### Options

- `--dry-run` – Simulate changes without modifying any files.
- `--verbose` – Show detailed output for all skipped/processed files.
- `--quiet` – Show only essential output (suppresses most messages).

## 🔍 Example

```bash
python whatsapp_timestamp_fixer.py ~/Downloads/whatsapp --verbose
```

Sample output:

```
📂 /home/user/Downloads/whatsapp
⏭️ [not_whatsapp.jpg] skipped - not a WhatsApp file
✅ [IMG-20210324-WA0001.jpg] success - set to 2021-03-24 00:00:01
```

## ⚠️ Notes

- Only `.jpg` and `.jpeg` files are processed.
- Files must follow WhatsApp naming conventions.
- Back up your files before use. This script modifies metadata directly.

## License

This project is licensed under the [MIT License](LICENSE).
