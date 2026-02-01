"""
File Handler - File I/O Operations with Encoding Detection
==========================================================

This module handles all file operations including:
- Reading files with encoding detection
- Writing files
- Binary file comparison
- File metadata extraction
- Large file handling with chunking
"""

import os
import mmap
from typing import List, Tuple, Optional, Dict, Any, BinaryIO
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import chardet
import hashlib


class FileType(Enum):
    """Type of file."""
    TEXT = "text"
    BINARY = "binary"
    IMAGE = "image"
    UNKNOWN = "unknown"


class Encoding(Enum):
    """Common file encodings."""
    UTF8 = "utf-8"
    UTF16LE = "utf-16-le"
    UTF16BE = "utf-16-be"
    ASCII = "ascii"
    LATIN1 = "latin-1"
    CP1252 = "cp1252"
    UNKNOWN = "unknown"


@dataclass
class FileInfo:
    """Information about a file."""
    path: str
    size: int
    modified_time: float
    encoding: str
    file_type: FileType
    line_count: int
    hash_md5: str
    hash_sha256: str
    
    def __repr__(self) -> str:
        return (f"FileInfo(path='{self.path}', size={self.size}, "
                f"type={self.file_type.value}, encoding={self.encoding})")


class FileHandler:
    """
    Handles file operations with encoding detection and binary support.
    """
    
    # Maximum file size for in-memory operations (100 MB)
    MAX_MEMORY_SIZE = 100 * 1024 * 1024
    
    # Chunk size for large file operations (10 MB)
    CHUNK_SIZE = 10 * 1024 * 1024
    
    # Binary file signatures
    BINARY_SIGNATURES = {
        b'\x89PNG': 'image/png',
        b'\xFF\xD8\xFF': 'image/jpeg',
        b'GIF87a': 'image/gif',
        b'GIF89a': 'image/gif',
        b'\x42\x4D': 'image/bmp',
        b'%PDF': 'application/pdf',
        b'\x50\x4B\x03\x04': 'application/zip',
        b'\x1F\x8B': 'application/gzip',
    }
    
    def __init__(self, encoding: Optional[str] = None):
        """
        Initialize file handler.
        
        Args:
            encoding: Force specific encoding (None for auto-detect)
        """
        self.forced_encoding = encoding
    
    def read_file(self, filepath: str) -> Tuple[List[str], FileInfo]:
        """
        Read a file and return its lines and metadata.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Tuple of (lines, file_info)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Get file info
        file_info = self.get_file_info(filepath)
        
        # Determine if binary
        if file_info.file_type == FileType.BINARY:
            # For binary files, read as hex lines
            lines = self._read_binary_as_hex(filepath)
        else:
            # Read as text
            encoding = self.forced_encoding or file_info.encoding
            
            try:
                if file_info.size > self.MAX_MEMORY_SIZE:
                    lines = self._read_large_file(filepath, encoding)
                else:
                    with open(filepath, 'r', encoding=encoding, errors='replace') as f:
                        lines = f.read().splitlines()
            except Exception as e:
                # Fallback to binary mode
                lines = self._read_binary_as_hex(filepath)
                file_info.file_type = FileType.BINARY
        
        file_info.line_count = len(lines)
        return lines, file_info
    
    def write_file(self, filepath: str, lines: List[str], 
                   encoding: str = 'utf-8') -> None:
        """
        Write lines to a file.
        
        Args:
            filepath: Path to the file
            lines: Lines to write
            encoding: File encoding
            
        Raises:
            PermissionError: If file can't be written
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        
        with open(filepath, 'w', encoding=encoding, errors='replace') as f:
            f.write('\n'.join(lines))
    
    def get_file_info(self, filepath: str) -> FileInfo:
        """
        Get detailed information about a file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            FileInfo object
        """
        stat = os.stat(filepath)
        
        # Detect encoding and file type
        encoding, file_type = self._detect_encoding_and_type(filepath)
        
        # Calculate hashes
        md5_hash, sha256_hash = self._calculate_hashes(filepath)
        
        return FileInfo(
            path=filepath,
            size=stat.st_size,
            modified_time=stat.st_mtime,
            encoding=encoding,
            file_type=file_type,
            line_count=0,  # Will be set when file is read
            hash_md5=md5_hash,
            hash_sha256=sha256_hash
        )
    
    def _detect_encoding_and_type(self, filepath: str) -> Tuple[str, FileType]:
        """
        Detect file encoding and type.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Tuple of (encoding, file_type)
        """
        # Read first chunk to detect
        try:
            with open(filepath, 'rb') as f:
                raw_data = f.read(min(8192, os.path.getsize(filepath)))
            
            # Check for binary signatures
            for signature, mime_type in self.BINARY_SIGNATURES.items():
                if raw_data.startswith(signature):
                    if 'image' in mime_type:
                        return 'binary', FileType.IMAGE
                    return 'binary', FileType.BINARY
            
            # Try to detect encoding
            if self.forced_encoding:
                encoding = self.forced_encoding
            else:
                result = chardet.detect(raw_data)
                encoding = result['encoding'] or 'utf-8'
                
                # Normalize encoding name
                encoding = encoding.lower().replace('_', '-')
            
            # Check if file is text
            try:
                raw_data.decode(encoding)
                return encoding, FileType.TEXT
            except (UnicodeDecodeError, LookupError):
                # Check if it's mostly printable ASCII
                printable_ratio = sum(32 <= b < 127 or b in (9, 10, 13) 
                                     for b in raw_data) / len(raw_data)
                if printable_ratio > 0.75:
                    return 'latin-1', FileType.TEXT
                else:
                    return 'binary', FileType.BINARY
                    
        except Exception:
            return 'binary', FileType.UNKNOWN
    
    def _read_large_file(self, filepath: str, encoding: str) -> List[str]:
        """
        Read a large file in chunks.
        
        Args:
            filepath: Path to the file
            encoding: File encoding
            
        Returns:
            List of lines
        """
        lines = []
        
        with open(filepath, 'r', encoding=encoding, errors='replace') as f:
            buffer = ""
            while True:
                chunk = f.read(self.CHUNK_SIZE)
                if not chunk:
                    if buffer:
                        lines.append(buffer)
                    break
                
                buffer += chunk
                
                # Split by lines
                parts = buffer.split('\n')
                lines.extend(parts[:-1])
                buffer = parts[-1]
        
        return lines
    
    def _read_binary_as_hex(self, filepath: str, 
                           bytes_per_line: int = 16) -> List[str]:
        """
        Read binary file as hexadecimal lines.
        
        Args:
            filepath: Path to the file
            bytes_per_line: Number of bytes to show per line
            
        Returns:
            List of hex dump lines
        """
        lines = []
        
        with open(filepath, 'rb') as f:
            offset = 0
            while True:
                chunk = f.read(bytes_per_line)
                if not chunk:
                    break
                
                # Format: "00000000: 48 65 6C 6C 6F 20 57 6F  72 6C 64 0A              |Hello World.|"
                hex_part = ' '.join(f'{b:02X}' for b in chunk)
                hex_part = hex_part.ljust(bytes_per_line * 3)
                
                # ASCII part
                ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
                
                line = f"{offset:08X}: {hex_part} |{ascii_part}|"
                lines.append(line)
                
                offset += bytes_per_line
        
        return lines
    
    def compare_binary(self, filepath_a: str, filepath_b: str) -> List[Tuple[int, int, int]]:
        """
        Compare two binary files byte by byte.
        
        Args:
            filepath_a: First file path
            filepath_b: Second file path
            
        Returns:
            List of (offset, byte_a, byte_b) for differences
        """
        differences = []
        
        with open(filepath_a, 'rb') as f1, open(filepath_b, 'rb') as f2:
            offset = 0
            
            while True:
                chunk1 = f1.read(self.CHUNK_SIZE)
                chunk2 = f2.read(self.CHUNK_SIZE)
                
                if not chunk1 and not chunk2:
                    break
                
                # Compare chunks
                max_len = max(len(chunk1), len(chunk2))
                for i in range(max_len):
                    byte1 = chunk1[i] if i < len(chunk1) else None
                    byte2 = chunk2[i] if i < len(chunk2) else None
                    
                    if byte1 != byte2:
                        differences.append((offset + i, byte1, byte2))
                
                offset += max_len
        
        return differences
    
    def _calculate_hashes(self, filepath: str) -> Tuple[str, str]:
        """
        Calculate MD5 and SHA256 hashes of a file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Tuple of (md5_hash, sha256_hash)
        """
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        
        try:
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    md5.update(chunk)
                    sha256.update(chunk)
            
            return md5.hexdigest(), sha256.hexdigest()
        except Exception:
            return '', ''
    
    def are_files_identical(self, filepath_a: str, filepath_b: str) -> bool:
        """
        Quick check if two files are identical using hashes.
        
        Args:
            filepath_a: First file path
            filepath_b: Second file path
            
        Returns:
            True if files are identical
        """
        # First check size
        size_a = os.path.getsize(filepath_a)
        size_b = os.path.getsize(filepath_b)
        
        if size_a != size_b:
            return False
        
        # Then check hash
        info_a = self.get_file_info(filepath_a)
        info_b = self.get_file_info(filepath_b)
        
        return info_a.hash_sha256 == info_b.hash_sha256


def read_file_lines(filepath: str, encoding: Optional[str] = None) -> List[str]:
    """
    Convenience function to read file lines.
    
    Args:
        filepath: Path to the file
        encoding: Optional encoding (auto-detected if None)
        
    Returns:
        List of lines
    """
    handler = FileHandler(encoding)
    lines, _ = handler.read_file(filepath)
    return lines


def write_file_lines(filepath: str, lines: List[str], 
                    encoding: str = 'utf-8') -> None:
    """
    Convenience function to write file lines.
    
    Args:
        filepath: Path to the file
        lines: Lines to write
        encoding: File encoding
    """
    handler = FileHandler()
    handler.write_file(filepath, lines, encoding)
