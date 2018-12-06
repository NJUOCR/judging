def secure_filename(filename: str) -> str:
    return filename.replace(' ', '_').strip()
