"""
Diff Engine - Main Interface for File and Directory Comparison
==============================================================

This module provides a high-level interface to the Myers diff algorithm and
additional diff functionality including three-way diffs, word-level diffs,
and character-level diffs.
"""

from typing import List, Tuple, Optional, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum
import difflib
import re

from core.myers_algorithm import MyersDiff, DiffResult, DiffType


@dataclass
class WordDiff:
    """Represents a word-level difference within a line."""
    type: DiffType
    word: str
    start_pos: int
    end_pos: int


@dataclass
class CharDiff:
    """Represents a character-level difference within a line."""
    type: DiffType
    char: str
    position: int


class DiffEngine:
    """
    Main diff engine providing various comparison capabilities.
    
    This class wraps the Myers algorithm and provides additional functionality
    for line-level, word-level, and character-level differences.
    """

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the diff engine with options.
        
        Args:
            options: Dictionary of comparison options
                - ignore_case: bool
                - ignore_whitespace: bool
                - ignore_blank_lines: bool
                - ignore_leading_whitespace: bool
                - ignore_trailing_whitespace: bool
                - ignore_comments: bool
                - comment_patterns: List[str] (regex patterns)
                - ignore_line_patterns: List[str] (regex patterns)
                - fuzzy_matching: bool
                - moving_block_detection: bool
        """
        self.options = options or {}
        
    def compare_lines(self, lines_a: List[str], lines_b: List[str]) -> List[DiffResult]:
        """
        Compare two sequences of lines using Myers' algorithm.
        
        Args:
            lines_a: First sequence of lines
            lines_b: Second sequence of lines
            
        Returns:
            List of DiffResult objects
        """
        # Apply preprocessing based on options
        processed_a = self._preprocess_lines(lines_a)
        processed_b = self._preprocess_lines(lines_b)
        
        # Perform Myers diff
        differ = MyersDiff(
            processed_a,
            processed_b,
            ignore_case=self.options.get('ignore_case', False),
            ignore_whitespace=self.options.get('ignore_whitespace', False),
            ignore_blank_lines=self.options.get('ignore_blank_lines', False)
        )
        
        results = differ.compute()
        
        # Apply post-processing
        if self.options.get('fuzzy_matching', False):
            results = self._apply_fuzzy_matching(results, lines_a, lines_b)
        
        if self.options.get('moving_block_detection', False):
            results = self._detect_moving_blocks(results, lines_a, lines_b)
        
        return results
    
    def _preprocess_lines(self, lines: List[str]) -> List[str]:
        """
        Preprocess lines based on ignore options.
        
        Args:
            lines: Input lines
            
        Returns:
            Preprocessed lines
        """
        processed = []
        
        for line in lines:
            # Skip blank lines if requested
            if self.options.get('ignore_blank_lines', False) and not line.strip():
                continue
            
            # Ignore leading whitespace
            if self.options.get('ignore_leading_whitespace', False):
                line = line.lstrip()
            
            # Ignore trailing whitespace
            if self.options.get('ignore_trailing_whitespace', False):
                line = line.rstrip()
            
            # Ignore comments
            if self.options.get('ignore_comments', False):
                line = self._remove_comments(line)
            
            # Ignore lines matching patterns
            ignore_patterns = self.options.get('ignore_line_patterns', [])
            if ignore_patterns and self._matches_any_pattern(line, ignore_patterns):
                continue
            
            processed.append(line)
        
        return processed
    
    def _remove_comments(self, line: str) -> str:
        """
        Remove comments from a line based on comment patterns.
        
        Args:
            line: Input line
            
        Returns:
            Line with comments removed
        """
        comment_patterns = self.options.get('comment_patterns', [
            r'//.*$',      # C++ style
            r'#.*$',       # Python style
            r'/\*.*?\*/',  # C style
        ])
        
        for pattern in comment_patterns:
            line = re.sub(pattern, '', line)
        
        return line
    
    def _matches_any_pattern(self, line: str, patterns: List[str]) -> bool:
        """
        Check if line matches any of the given regex patterns.
        
        Args:
            line: Input line
            patterns: List of regex patterns
            
        Returns:
            True if line matches any pattern
        """
        for pattern in patterns:
            if re.search(pattern, line):
                return True
        return False
    
    def _apply_fuzzy_matching(self, results: List[DiffResult],
                             lines_a: List[str], lines_b: List[str]) -> List[DiffResult]:
        """
        Apply fuzzy matching to align similar but not identical lines.
        
        This uses the SequenceMatcher ratio to find lines that are similar
        enough to be considered modifications rather than delete+insert.
        
        Args:
            results: Initial diff results
            lines_a: Original lines from sequence A
            lines_b: Original lines from sequence B
            
        Returns:
            Modified diff results with fuzzy matching applied
        """
        threshold = 0.6  # Similarity threshold (60%)
        modified_results = []
        
        i = 0
        while i < len(results):
            result = results[i]
            
            # Look for consecutive DELETE and INSERT
            if (i < len(results) - 1 and
                result.type == DiffType.DELETE and
                results[i + 1].type == DiffType.INSERT):
                
                next_result = results[i + 1]
                
                # Check if they're similar enough
                old_text = '\n'.join(result.old_lines)
                new_text = '\n'.join(next_result.new_lines)
                
                matcher = difflib.SequenceMatcher(None, old_text, new_text)
                if matcher.ratio() >= threshold:
                    # Merge into REPLACE
                    modified_results.append(DiffResult(
                        type=DiffType.REPLACE,
                        old_start=result.old_start,
                        old_count=result.old_count,
                        new_start=next_result.new_start,
                        new_count=next_result.new_count,
                        old_lines=result.old_lines,
                        new_lines=next_result.new_lines
                    ))
                    i += 2
                    continue
            
            modified_results.append(result)
            i += 1
        
        return modified_results
    
    def _detect_moving_blocks(self, results: List[DiffResult],
                             lines_a: List[str], lines_b: List[str]) -> List[DiffResult]:
        """
        Detect blocks of code that have been moved within the file.
        
        This looks for DELETE and INSERT blocks that contain identical content
        but appear in different locations.
        
        Args:
            results: Initial diff results
            lines_a: Original lines from sequence A
            lines_b: Original lines from sequence B
            
        Returns:
            Modified diff results with moved blocks detected
        """
        # Build a map of deleted and inserted blocks
        deleted_blocks: List[Tuple[int, List[str]]] = []
        inserted_blocks: List[Tuple[int, List[str]]] = []
        
        for result in results:
            if result.type == DiffType.DELETE:
                deleted_blocks.append((result.old_start, result.old_lines))
            elif result.type == DiffType.INSERT:
                inserted_blocks.append((result.new_start, result.new_lines))
        
        # Find matching blocks
        moves: Dict[int, int] = {}  # Map from delete index to insert index
        
        for i, (del_pos, del_lines) in enumerate(deleted_blocks):
            for j, (ins_pos, ins_lines) in enumerate(inserted_blocks):
                if j in moves.values():
                    continue  # Already matched
                
                if del_lines == ins_lines:
                    moves[i] = j
                    break
        
        # For now, just return original results
        # Full implementation would modify result types to indicate moves
        return results
    
    def compare_words(self, line_a: str, line_b: str) -> List[WordDiff]:
        """
        Compare two lines at word level.
        
        Args:
            line_a: First line
            line_b: Second line
            
        Returns:
            List of WordDiff objects
        """
        # Split into words (including whitespace)
        words_a = re.findall(r'\S+|\s+', line_a)
        words_b = re.findall(r'\S+|\s+', line_b)
        
        # Use difflib for word-level diff
        matcher = difflib.SequenceMatcher(None, words_a, words_b)
        
        word_diffs = []
        pos_a = 0
        pos_b = 0
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for i in range(i1, i2):
                    word_diffs.append(WordDiff(
                        type=DiffType.EQUAL,
                        word=words_a[i],
                        start_pos=pos_a,
                        end_pos=pos_a + len(words_a[i])
                    ))
                    pos_a += len(words_a[i])
                pos_b += sum(len(w) for w in words_b[j1:j2])
            
            elif tag == 'delete':
                for i in range(i1, i2):
                    word_diffs.append(WordDiff(
                        type=DiffType.DELETE,
                        word=words_a[i],
                        start_pos=pos_a,
                        end_pos=pos_a + len(words_a[i])
                    ))
                    pos_a += len(words_a[i])
            
            elif tag == 'insert':
                for j in range(j1, j2):
                    word_diffs.append(WordDiff(
                        type=DiffType.INSERT,
                        word=words_b[j],
                        start_pos=pos_b,
                        end_pos=pos_b + len(words_b[j])
                    ))
                    pos_b += len(words_b[j])
            
            elif tag == 'replace':
                # Add deletes
                for i in range(i1, i2):
                    word_diffs.append(WordDiff(
                        type=DiffType.DELETE,
                        word=words_a[i],
                        start_pos=pos_a,
                        end_pos=pos_a + len(words_a[i])
                    ))
                    pos_a += len(words_a[i])
                
                # Add inserts
                for j in range(j1, j2):
                    word_diffs.append(WordDiff(
                        type=DiffType.INSERT,
                        word=words_b[j],
                        start_pos=pos_b,
                        end_pos=pos_b + len(words_b[j])
                    ))
                    pos_b += len(words_b[j])
        
        return word_diffs
    
    def compare_chars(self, str_a: str, str_b: str) -> List[CharDiff]:
        """
        Compare two strings at character level.
        
        Args:
            str_a: First string
            str_b: Second string
            
        Returns:
            List of CharDiff objects
        """
        matcher = difflib.SequenceMatcher(None, str_a, str_b)
        
        char_diffs = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for i in range(i1, i2):
                    char_diffs.append(CharDiff(
                        type=DiffType.EQUAL,
                        char=str_a[i],
                        position=i
                    ))
            
            elif tag == 'delete':
                for i in range(i1, i2):
                    char_diffs.append(CharDiff(
                        type=DiffType.DELETE,
                        char=str_a[i],
                        position=i
                    ))
            
            elif tag == 'insert':
                for j in range(j1, j2):
                    char_diffs.append(CharDiff(
                        type=DiffType.INSERT,
                        char=str_b[j],
                        position=j
                    ))
            
            elif tag == 'replace':
                for i in range(i1, i2):
                    char_diffs.append(CharDiff(
                        type=DiffType.DELETE,
                        char=str_a[i],
                        position=i
                    ))
                for j in range(j1, j2):
                    char_diffs.append(CharDiff(
                        type=DiffType.INSERT,
                        char=str_b[j],
                        position=j
                    ))
        
        return char_diffs
    
    def three_way_merge(self, base_lines: List[str],
                       yours_lines: List[str],
                       theirs_lines: List[str]) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Perform a three-way merge.
        
        Args:
            base_lines: Base version lines
            yours_lines: Your version lines
            theirs_lines: Their version lines
            
        Returns:
            Tuple of (merged_lines, conflicts)
            - merged_lines: The merged result
            - conflicts: List of conflict information
        """
        # Compare base with yours
        yours_diff = self.compare_lines(base_lines, yours_lines)
        
        # Compare base with theirs
        theirs_diff = self.compare_lines(base_lines, theirs_lines)
        
        # Merge the changes
        merged_lines = []
        conflicts = []
        
        # Build change maps
        yours_changes = self._build_change_map(yours_diff)
        theirs_changes = self._build_change_map(theirs_diff)
        
        # Process each line from base
        i = 0
        while i < len(base_lines):
            yours_change = yours_changes.get(i)
            theirs_change = theirs_changes.get(i)
            
            if yours_change is None and theirs_change is None:
                # No changes from either side
                merged_lines.append(base_lines[i])
                i += 1
            
            elif yours_change is not None and theirs_change is None:
                # Only yours changed
                merged_lines.extend(yours_change['new_lines'])
                i += yours_change['old_count'] or 1
            
            elif yours_change is None and theirs_change is not None:
                # Only theirs changed
                merged_lines.extend(theirs_change['new_lines'])
                i += theirs_change['old_count'] or 1
            
            else:
                # Both changed - potential conflict
                if yours_change['new_lines'] == theirs_change['new_lines']:
                    # Same change on both sides
                    merged_lines.extend(yours_change['new_lines'])
                else:
                    # Conflict!
                    conflict = {
                        'line': i,
                        'base_lines': base_lines[i:i + max(yours_change['old_count'], theirs_change['old_count'])],
                        'yours_lines': yours_change['new_lines'],
                        'theirs_lines': theirs_change['new_lines']
                    }
                    conflicts.append(conflict)
                    
                    # Add conflict markers
                    merged_lines.append("<<<<<<< YOURS")
                    merged_lines.extend(yours_change['new_lines'])
                    merged_lines.append("=======")
                    merged_lines.extend(theirs_change['new_lines'])
                    merged_lines.append(">>>>>>> THEIRS")
                
                i += max(yours_change.get('old_count', 1), theirs_change.get('old_count', 1))
        
        return merged_lines, conflicts
    
    def _build_change_map(self, diff_results: List[DiffResult]) -> Dict[int, Dict[str, Any]]:
        """
        Build a map of line numbers to changes.
        
        Args:
            diff_results: List of DiffResult objects
            
        Returns:
            Dictionary mapping line numbers to change information
        """
        change_map = {}
        
        for result in diff_results:
            if result.type != DiffType.EQUAL:
                change_map[result.old_start] = {
                    'type': result.type,
                    'old_count': result.old_count,
                    'new_lines': result.new_lines
                }
        
        return change_map


def create_diff_engine(options: Optional[Dict[str, Any]] = None) -> DiffEngine:
    """
    Factory function to create a DiffEngine instance.
    
    Args:
        options: Comparison options
        
    Returns:
        DiffEngine instance
    """
    return DiffEngine(options)
