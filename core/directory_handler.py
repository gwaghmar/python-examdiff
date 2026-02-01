"""
Directory Handler - Directory Comparison and Operations
=======================================================

This module handles directory comparison operations including:
- Recursive directory traversal
- File filtering and matching
- Directory tree comparison
- Mass file operations (copy, delete, sync)
- Directory snapshots
"""

import os
import shutil
import fnmatch
from typing import List, Tuple, Optional, Dict, Any, Set, Callable
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import xml.etree.ElementTree as ET
import json

from core.file_handler import FileHandler, FileInfo


class FileStatus(Enum):
    """Status of a file in directory comparison."""
    IDENTICAL = "identical"           # Files are the same
    DIFFERENT = "different"           # Files differ
    LEFT_ONLY = "left_only"          # File exists only in left dir
    RIGHT_ONLY = "right_only"        # File exists only in right dir
    NEWER_LEFT = "newer_left"        # Left file is newer
    NEWER_RIGHT = "newer_right"      # Right file is newer
    ERROR = "error"                  # Error comparing files


class CompareMode(Enum):
    """Mode for comparing files."""
    CONTENT = "content"              # Compare file contents
    SIZE = "size"                    # Compare file sizes
    TIMESTAMP = "timestamp"          # Compare modification times
    SIZE_AND_TIMESTAMP = "size_and_timestamp"  # Both size and timestamp
    CONTENT_AND_SIZE = "content_and_size"      # Content and size
    HASH = "hash"                    # Compare file hashes


@dataclass
class DirectoryEntry:
    """
    Represents a file or directory in the comparison.
    """
    name: str
    relative_path: str
    is_dir: bool
    status: FileStatus
    left_path: Optional[str] = None
    right_path: Optional[str] = None
    left_info: Optional[FileInfo] = None
    right_info: Optional[FileInfo] = None
    children: List['DirectoryEntry'] = field(default_factory=list)
    
    def __repr__(self) -> str:
        return f"DirectoryEntry(name='{self.name}', status={self.status.value}, is_dir={self.is_dir})"


@dataclass
class DirectoryComparisonResult:
    """
    Result of a directory comparison.
    """
    left_root: str
    right_root: str
    entries: List[DirectoryEntry]
    total_files: int = 0
    identical_files: int = 0
    different_files: int = 0
    left_only_files: int = 0
    right_only_files: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def get_statistics(self) -> Dict[str, int]:
        """Get comparison statistics."""
        return {
            'total': self.total_files,
            'identical': self.identical_files,
            'different': self.different_files,
            'left_only': self.left_only_files,
            'right_only': self.right_only_files,
        }


class DirectoryHandler:
    """
    Handles directory comparison and operations.
    """
    
    def __init__(self, 
                 compare_mode: CompareMode = CompareMode.CONTENT,
                 recursive: bool = True,
                 include_patterns: Optional[List[str]] = None,
                 exclude_patterns: Optional[List[str]] = None,
                 ignore_hidden: bool = False):
        """
        Initialize directory handler.
        
        Args:
            compare_mode: Mode for comparing files
            recursive: Whether to compare subdirectories
            include_patterns: File patterns to include (e.g., ['*.py', '*.txt'])
            exclude_patterns: File patterns to exclude (e.g., ['*.pyc', '__pycache__'])
            ignore_hidden: Whether to ignore hidden files/directories
        """
        self.compare_mode = compare_mode
        self.recursive = recursive
        self.include_patterns = include_patterns or ['*']
        self.exclude_patterns = exclude_patterns or []
        self.ignore_hidden = ignore_hidden
        self.file_handler = FileHandler()
    
    def compare_directories(self, left_dir: str, right_dir: str,
                          progress_callback: Optional[Callable[[str], None]] = None) -> DirectoryComparisonResult:
        """
        Compare two directories.
        
        Args:
            left_dir: Path to left directory
            right_dir: Path to right directory
            progress_callback: Optional callback for progress updates
            
        Returns:
            DirectoryComparisonResult object
        """
        if not os.path.isdir(left_dir):
            raise NotADirectoryError(f"Not a directory: {left_dir}")
        if not os.path.isdir(right_dir):
            raise NotADirectoryError(f"Not a directory: {right_dir}")
        
        result = DirectoryComparisonResult(
            left_root=left_dir,
            right_root=right_dir,
            entries=[]
        )
        
        # Build file trees
        left_tree = self._build_file_tree(left_dir, progress_callback)
        right_tree = self._build_file_tree(right_dir, progress_callback)
        
        # Compare trees
        entries = self._compare_trees(left_dir, right_dir, left_tree, right_tree, 
                                     progress_callback)
        
        result.entries = entries
        
        # Calculate statistics
        self._calculate_statistics(result)
        
        return result
    
    def _build_file_tree(self, root_dir: str, 
                        progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, Any]:
        """
        Build a tree structure of files and directories.
        
        Args:
            root_dir: Root directory path
            progress_callback: Optional progress callback
            
        Returns:
            Dictionary representing the file tree
        """
        tree: Dict[str, Any] = {}
        
        if self.recursive:
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Filter hidden directories
                if self.ignore_hidden:
                    dirnames[:] = [d for d in dirnames if not d.startswith('.')]
                    filenames = [f for f in filenames if not f.startswith('.')]
                
                # Filter by exclude patterns
                dirnames[:] = [d for d in dirnames if not self._matches_exclude(d)]
                filenames = [f for f in filenames if not self._matches_exclude(f)]
                
                # Filter by include patterns
                filenames = [f for f in filenames if self._matches_include(f)]
                
                rel_path = os.path.relpath(dirpath, root_dir)
                
                for filename in filenames:
                    if progress_callback:
                        progress_callback(f"Scanning: {filename}")
                    
                    full_path = os.path.join(dirpath, filename)
                    rel_file_path = os.path.join(rel_path, filename) if rel_path != '.' else filename
                    tree[rel_file_path] = full_path
        else:
            # Non-recursive: only top-level files
            try:
                for entry in os.scandir(root_dir):
                    if entry.is_file():
                        if self.ignore_hidden and entry.name.startswith('.'):
                            continue
                        if not self._matches_exclude(entry.name) and self._matches_include(entry.name):
                            tree[entry.name] = entry.path
            except PermissionError:
                pass
        
        return tree
    
    def _matches_include(self, filename: str) -> bool:
        """Check if filename matches any include pattern."""
        return any(fnmatch.fnmatch(filename, pattern) for pattern in self.include_patterns)
    
    def _matches_exclude(self, filename: str) -> bool:
        """Check if filename matches any exclude pattern."""
        return any(fnmatch.fnmatch(filename, pattern) for pattern in self.exclude_patterns)
    
    def _compare_trees(self, left_root: str, right_root: str,
                      left_tree: Dict[str, str], right_tree: Dict[str, str],
                      progress_callback: Optional[Callable[[str], None]] = None) -> List[DirectoryEntry]:
        """
        Compare two file trees.
        
        Args:
            left_root: Left root directory
            right_root: Right root directory
            left_tree: Left file tree
            right_tree: Right file tree
            progress_callback: Optional progress callback
            
        Returns:
            List of DirectoryEntry objects
        """
        entries: List[DirectoryEntry] = []
        
        # Get all relative paths
        all_paths = sorted(set(left_tree.keys()) | set(right_tree.keys()))
        
        for rel_path in all_paths:
            if progress_callback:
                progress_callback(f"Comparing: {rel_path}")
            
            left_path = left_tree.get(rel_path)
            right_path = right_tree.get(rel_path)
            
            # Determine status
            if left_path and right_path:
                status = self._compare_files(left_path, right_path)
                left_info = self.file_handler.get_file_info(left_path)
                right_info = self.file_handler.get_file_info(right_path)
            elif left_path:
                status = FileStatus.LEFT_ONLY
                left_info = self.file_handler.get_file_info(left_path)
                right_info = None
            else:
                status = FileStatus.RIGHT_ONLY
                left_info = None
                right_info = self.file_handler.get_file_info(right_path)
            
            entry = DirectoryEntry(
                name=os.path.basename(rel_path),
                relative_path=rel_path,
                is_dir=False,
                status=status,
                left_path=left_path,
                right_path=right_path,
                left_info=left_info,
                right_info=right_info
            )
            
            entries.append(entry)
        
        return entries
    
    def _compare_files(self, left_path: str, right_path: str) -> FileStatus:
        """
        Compare two files based on the compare mode.
        
        Args:
            left_path: Left file path
            right_path: Right file path
            
        Returns:
            FileStatus indicating the comparison result
        """
        try:
            if self.compare_mode == CompareMode.SIZE:
                left_size = os.path.getsize(left_path)
                right_size = os.path.getsize(right_path)
                return FileStatus.IDENTICAL if left_size == right_size else FileStatus.DIFFERENT
            
            elif self.compare_mode == CompareMode.TIMESTAMP:
                left_mtime = os.path.getmtime(left_path)
                right_mtime = os.path.getmtime(right_path)
                if abs(left_mtime - right_mtime) < 1:  # Within 1 second
                    return FileStatus.IDENTICAL
                elif left_mtime > right_mtime:
                    return FileStatus.NEWER_LEFT
                else:
                    return FileStatus.NEWER_RIGHT
            
            elif self.compare_mode == CompareMode.SIZE_AND_TIMESTAMP:
                left_size = os.path.getsize(left_path)
                right_size = os.path.getsize(right_path)
                left_mtime = os.path.getmtime(left_path)
                right_mtime = os.path.getmtime(right_path)
                
                if left_size != right_size:
                    return FileStatus.DIFFERENT
                
                if abs(left_mtime - right_mtime) < 1:
                    return FileStatus.IDENTICAL
                elif left_mtime > right_mtime:
                    return FileStatus.NEWER_LEFT
                else:
                    return FileStatus.NEWER_RIGHT
            
            elif self.compare_mode == CompareMode.HASH:
                left_info = self.file_handler.get_file_info(left_path)
                right_info = self.file_handler.get_file_info(right_path)
                return FileStatus.IDENTICAL if left_info.hash_sha256 == right_info.hash_sha256 else FileStatus.DIFFERENT
            
            else:  # CONTENT or CONTENT_AND_SIZE
                # First check size
                left_size = os.path.getsize(left_path)
                right_size = os.path.getsize(right_path)
                if left_size != right_size:
                    return FileStatus.DIFFERENT
                
                # Then check content
                if self.file_handler.are_files_identical(left_path, right_path):
                    return FileStatus.IDENTICAL
                else:
                    return FileStatus.DIFFERENT
        
        except Exception:
            return FileStatus.ERROR
    
    def _calculate_statistics(self, result: DirectoryComparisonResult) -> None:
        """Calculate statistics for the comparison result."""
        for entry in result.entries:
            if not entry.is_dir:
                result.total_files += 1
                
                if entry.status == FileStatus.IDENTICAL:
                    result.identical_files += 1
                elif entry.status == FileStatus.DIFFERENT:
                    result.different_files += 1
                elif entry.status == FileStatus.LEFT_ONLY:
                    result.left_only_files += 1
                elif entry.status == FileStatus.RIGHT_ONLY:
                    result.right_only_files += 1
    
    def copy_left_to_right(self, entry: DirectoryEntry) -> bool:
        """
        Copy a file from left to right.
        
        Args:
            entry: DirectoryEntry to copy
            
        Returns:
            True if successful
        """
        try:
            if entry.left_path and entry.right_path:
                os.makedirs(os.path.dirname(entry.right_path), exist_ok=True)
                shutil.copy2(entry.left_path, entry.right_path)
                return True
        except Exception:
            return False
        return False
    
    def copy_right_to_left(self, entry: DirectoryEntry) -> bool:
        """
        Copy a file from right to left.
        
        Args:
            entry: DirectoryEntry to copy
            
        Returns:
            True if successful
        """
        try:
            if entry.right_path and entry.left_path:
                os.makedirs(os.path.dirname(entry.left_path), exist_ok=True)
                shutil.copy2(entry.right_path, entry.left_path)
                return True
        except Exception:
            return False
        return False
    
    def delete_left(self, entry: DirectoryEntry) -> bool:
        """
        Delete a file from left directory.
        
        Args:
            entry: DirectoryEntry to delete
            
        Returns:
            True if successful
        """
        try:
            if entry.left_path and os.path.exists(entry.left_path):
                os.remove(entry.left_path)
                return True
        except Exception:
            return False
        return False
    
    def delete_right(self, entry: DirectoryEntry) -> bool:
        """
        Delete a file from right directory.
        
        Args:
            entry: DirectoryEntry to delete
            
        Returns:
            True if successful
        """
        try:
            if entry.right_path and os.path.exists(entry.right_path):
                os.remove(entry.right_path)
                return True
        except Exception:
            return False
        return False
    
    def synchronize(self, result: DirectoryComparisonResult,
                   direction: str = 'left_to_right') -> Dict[str, int]:
        """
        Synchronize directories.
        
        Args:
            result: DirectoryComparisonResult
            direction: 'left_to_right' or 'right_to_left'
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            'copied': 0,
            'deleted': 0,
            'errors': 0
        }
        
        for entry in result.entries:
            if entry.is_dir:
                continue
            
            try:
                if direction == 'left_to_right':
                    if entry.status == FileStatus.LEFT_ONLY or entry.status == FileStatus.DIFFERENT:
                        if self.copy_left_to_right(entry):
                            stats['copied'] += 1
                        else:
                            stats['errors'] += 1
                    elif entry.status == FileStatus.RIGHT_ONLY:
                        if self.delete_right(entry):
                            stats['deleted'] += 1
                        else:
                            stats['errors'] += 1
                else:  # right_to_left
                    if entry.status == FileStatus.RIGHT_ONLY or entry.status == FileStatus.DIFFERENT:
                        if self.copy_right_to_left(entry):
                            stats['copied'] += 1
                        else:
                            stats['errors'] += 1
                    elif entry.status == FileStatus.LEFT_ONLY:
                        if self.delete_left(entry):
                            stats['deleted'] += 1
                        else:
                            stats['errors'] += 1
            except Exception:
                stats['errors'] += 1
        
        return stats
    
    def save_snapshot(self, result: DirectoryComparisonResult, 
                     filepath: str) -> None:
        """
        Save comparison result as XML snapshot.
        
        Args:
            result: DirectoryComparisonResult
            filepath: Path to save snapshot
        """
        root = ET.Element('DirectoryComparison')
        root.set('timestamp', result.timestamp.isoformat())
        root.set('left', result.left_root)
        root.set('right', result.right_root)
        
        # Add statistics
        stats = ET.SubElement(root, 'Statistics')
        for key, value in result.get_statistics().items():
            stat = ET.SubElement(stats, 'Stat')
            stat.set('name', key)
            stat.set('value', str(value))
        
        # Add entries
        entries_elem = ET.SubElement(root, 'Entries')
        for entry in result.entries:
            entry_elem = ET.SubElement(entries_elem, 'Entry')
            entry_elem.set('name', entry.name)
            entry_elem.set('path', entry.relative_path)
            entry_elem.set('status', entry.status.value)
            entry_elem.set('is_dir', str(entry.is_dir))
            
            if entry.left_path:
                entry_elem.set('left_path', entry.left_path)
            if entry.right_path:
                entry_elem.set('right_path', entry.right_path)
        
        # Write to file
        tree = ET.ElementTree(root)
        ET.indent(tree, space='  ')
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
    
    def load_snapshot(self, filepath: str) -> DirectoryComparisonResult:
        """
        Load comparison result from XML snapshot.
        
        Args:
            filepath: Path to snapshot file
            
        Returns:
            DirectoryComparisonResult
        """
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        result = DirectoryComparisonResult(
            left_root=root.get('left', ''),
            right_root=root.get('right', ''),
            entries=[],
            timestamp=datetime.fromisoformat(root.get('timestamp', datetime.now().isoformat()))
        )
        
        # Load entries
        entries_elem = root.find('Entries')
        if entries_elem is not None:
            for entry_elem in entries_elem.findall('Entry'):
                entry = DirectoryEntry(
                    name=entry_elem.get('name', ''),
                    relative_path=entry_elem.get('path', ''),
                    is_dir=entry_elem.get('is_dir', 'False') == 'True',
                    status=FileStatus(entry_elem.get('status', 'identical')),
                    left_path=entry_elem.get('left_path'),
                    right_path=entry_elem.get('right_path')
                )
                result.entries.append(entry)
        
        # Recalculate statistics
        self._calculate_statistics(result)
        
        return result
