def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Split text into chunks of `chunk_size` characters with `chunk_overlap` overlap.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
        
        # Prevent infinite loops if overlap is configured larger than or equal to chunk_size
        if chunk_size <= chunk_overlap:
            break
            
    return chunks
