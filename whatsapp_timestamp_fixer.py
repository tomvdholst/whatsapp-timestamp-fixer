import sys
import os
import re
import piexif
import argparse
from datetime import datetime, timedelta

# Check if file is compatible with the script
def is_whatsapp_file(filename):
    return "WhatsApp" in filename or "-WA" in filename


# Check if file is a (compatible) image file
def is_image_file(filename):
    return filename.lower().endswith(('.jpg', '.jpeg'))

# Check if image file already has a timestamp in its metadata
def image_has_timestamp(filepath):
    try:
        # Load metadata from the file
        metadata = piexif.load(filepath)

        # Get the DateTimeOriginal tag's value
        dt = metadata.get("Exif", {}).get(piexif.ExifIFD.DateTimeOriginal)

        # Check if value is empty
        if dt:
            return True # Metadata is already present
        else:
            return False # Missing metadata

    except Exception as e:
        print(f"❌ Error reading metadata from '{filepath}': {e}")
        return False

# Extract the date from file renamed by whatsapp
def extract_datetime_from_filename(filename):
    # Extract datetime from filenames like "IMG-YYYYMMDD-WAXXXX" or "VID-YYYYMMDD-WAXXXX"
    match = re.search(r'\D+(\d{4})(\d{2})(\d{2})\D*-WA(\d{4})\D+', filename)
    if match:
        year, month, day, wa_number = match.groups()
        date = datetime.strptime(f"{year}{month}{day}", '%Y%m%d')
        # Time is not known for this naming format. Add picture number in seconds after midnight for correct timeline order.
        return date + timedelta(seconds=int(wa_number))

    # Extract datetime from filenames like "WhatsApp Image YYYY-MM-DD at hh.mm.ss" or "WhatsApp Video YYYY-MM-DD at hh.mm.ss"
    match = re.search(r'\D+(\d{4})\D(\d{2})\D(\d{2})\D+(\d{2})\D(\d{2})\D(\d{2})\D+', filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return datetime(
            int(year), int(month), int(day),
            int(hour), int(minute), int(second)
        )
    
    return None

# Set the datetime metadata tag in an image file
def set_image_datetime(filepath, dt, dry_run=False):
    try:
        # Load existing metadata or initialize an empty dictionary
        try:
            metadata = piexif.load(filepath)
        except Exception:
            metadata = {"0th": {}, "Exif": {}, "1st": {}, "GPS": {}, "Interop": {}, "thumbnail": None}

        # Format datetime string to EXIF format (YYYY:MM:DD HH:MM:SS)
        datetime_string = dt.strftime('%Y:%m:%d %H:%M:%S').encode("utf-8")

        # Set DateTimeOriginal
        metadata['Exif'][piexif.ExifIFD.DateTimeOriginal] = datetime_string
        # Set DateTimeDigitized
        metadata['Exif'][piexif.ExifIFD.DateTimeDigitized] = datetime_string
        # Set DateTime (0th IFD)
        metadata['0th'][piexif.ImageIFD.DateTime] = datetime_string

        # Write the metadata back to the file
        if not dry_run:
            metadata_bytes = piexif.dump(metadata) # Convert metadata to bytes
            piexif.insert(metadata_bytes, filepath)
        return True

    except Exception as e:
        print(f"❌ Failed to set DateTimeOriginal for '{filepath}': {e}")
        return False

def main():
    # Handle parser arguments
    parser = argparse.ArgumentParser(description="Fix date and time metadata in images shared via WhatsApp by retrieving the timestamp from its filename.")
    parser.add_argument("directory", nargs="?", default=os.getcwd(), help="Directory to process (default: current working directory)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without modifying files")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--verbose', action='store_true', help='Show detailed output')
    group.add_argument('--quiet', action='store_true', help='Suppress most output')
    args = parser.parse_args()

    # Use first argument as path, or use current working directory if none is given
    directory = args.directory

    # Check if path is valid
    if not os.path.isdir(directory):
        print(f"❌ Error: '{directory}' is not a directory.")
        return
    
    # Walk through all subdirectories and files
    for current_dir, _, files in os.walk(directory):
        if not args.quiet:
            print("📂", current_dir)
        
        for filename in files:
            # Check if file is a WhatsApp file
            if not is_whatsapp_file(filename):
                if args.verbose:
                    print("⏭️ [", filename, "] skipped - not a WhatsApp file")
                continue

            # Check if file is compatible
            if not is_image_file(filename):
                if args.verbose:
                    print("⏭️ [", filename, "] skipped - not an image file")
                continue

            # Get full path to file
            filepath = os.path.join(current_dir, filename)

            # Check if timestamp in metadata is already filled in
            if image_has_timestamp(filepath):
                if args.verbose:
                    print("⏭️ [", filename, "] skipped - metadata already present")
                continue

            # Retrieve datetime from file name
            date = extract_datetime_from_filename(filename)
            if not date:
                if args.verbose:
                    print("⏭️ [", filename, "] skipped - could not extract date from filename.")
                continue

            # Fix metadata
            if set_image_datetime(filepath, date, args.dry_run):
                if not args.quiet:
                    status = "✅ DRY-RUN" if args.dry_run else "✅"
                    print(f"{status} [", filename, "] success - set to", date)

    # Wait for user input before exiting if running in a terminal
    if sys.stdin.isatty():
        input("Press Enter to exit...")

# Run script
if __name__ == "__main__":
    main()