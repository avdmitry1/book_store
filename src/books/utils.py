import hashlib


def hash_book_info(book_title: str, publisher_name: str) -> str:
    # Concatenate the book title and publisher name with a separator
    combined_info = f"{book_title} | {publisher_name}"

    # Encode the concatenated string into bytes using UTF-8 encoding
    combined_info_bytes = combined_info.encode("utf-8")

    # Compute the SHA-256 hash of the byte-encoded string
    # and return the hexadecimal digest of the hash
    return hashlib.sha256(combined_info_bytes).hexdigest()
