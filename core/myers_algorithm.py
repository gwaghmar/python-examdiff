"""
Myers' Diff Algorithm Implementation
=====================================

This module implements Eugene Myers' O(ND) difference algorithm, which is the
foundation of many modern diff tools (including GNU diff, Git, etc.).

The algorithm finds the Shortest Edit Script (SES) - the minimum number of
insertions and deletions needed to transform one sequence into another.

References:
- Myers, Eugene W. "An O(ND) difference algorithm and its variations."
  Algorithmica 1.1-4 (1986): 251-266.

Algorithm Overview:
------------------
The algorithm works by finding the longest common subsequence (LCS) using a
graph-based approach. It represents the problem as a path through an edit graph
where:
- Moving right = inserting from sequence B
- Moving down = deleting from sequence A  
- Moving diagonally = matching elements (no edit)

The algorithm explores the edit graph in increasing "edit distance" (D) until
it finds a path from (0,0) to (N,M) where N and M are the lengths of the sequences.

Time Complexity: O((N+M)D) where D is the edit distance
Space Complexity: O(N+M)
"""

from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class DiffType(Enum):
    """Type of difference between two sequences."""
    EQUAL = "equal"      # Lines are identical
    INSERT = "insert"    # Line exists only in sequence B
    DELETE = "delete"    # Line exists only in sequence A
    REPLACE = "replace"  # Line was modified


@dataclass
class DiffResult:
    """
    Represents a single difference operation.
    
    Attributes:
        type: Type of operation (EQUAL, INSERT, DELETE, REPLACE)
        old_start: Starting line number in sequence A (0-indexed)
        old_count: Number of lines affected in sequence A
        new_start: Starting line number in sequence B (0-indexed)
        new_count: Number of lines affected in sequence B
        old_lines: Lines from sequence A
        new_lines: Lines from sequence B
    """
    type: DiffType
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    old_lines: List[str]
    new_lines: List[str]

    def __repr__(self) -> str:
        return (f"DiffResult(type={self.type.value}, "
                f"old=[{self.old_start}:{self.old_start+self.old_count}], "
                f"new=[{self.new_start}:{self.new_start+self.new_count}])")


class MyersDiff:
    """
    Implementation of Myers' diff algorithm.
    
    This class provides methods to compute the differences between two sequences
    using the Myers' O(ND) algorithm.
    """

    def __init__(self, seq_a: List[str], seq_b: List[str],
                 ignore_case: bool = False,
                 ignore_whitespace: bool = False,
                 ignore_blank_lines: bool = False):
        """
        Initialize the Myers diff calculator.
        
        Args:
            seq_a: First sequence (list of lines)
            seq_b: Second sequence (list of lines)
            ignore_case: Whether to ignore case when comparing
            ignore_whitespace: Whether to ignore whitespace differences
            ignore_blank_lines: Whether to ignore blank lines
        """
        self.seq_a = seq_a
        self.seq_b = seq_b
        self.ignore_case = ignore_case
        self.ignore_whitespace = ignore_whitespace
        self.ignore_blank_lines = ignore_blank_lines
        
        # Preprocess sequences based on ignore options
        self.processed_a = self._preprocess_sequence(seq_a)
        self.processed_b = self._preprocess_sequence(seq_b)
        
        self.n = len(self.processed_a)
        self.m = len(self.processed_b)

    def _preprocess_sequence(self, seq: List[str]) -> List[str]:
        """
        Preprocess sequence based on ignore options.
        
        Args:
            seq: Input sequence
            
        Returns:
            Processed sequence
        """
        processed = []
        for line in seq:
            # Skip blank lines if requested
            if self.ignore_blank_lines and not line.strip():
                continue
            
            # Process line based on options
            if self.ignore_whitespace:
                line = ' '.join(line.split())  # Normalize whitespace
            
            if self.ignore_case:
                line = line.lower()
            
            processed.append(line)
        
        return processed

    def compute(self) -> List[DiffResult]:
        """
        Compute the differences between the two sequences.
        
        Returns:
            List of DiffResult objects representing the differences
        """
        # Find the shortest edit script using Myers' algorithm
        edit_path = self._find_shortest_edit_script()
        
        # Convert the edit path to diff results
        diff_results = self._build_diff_results(edit_path)
        
        return diff_results

    def _find_shortest_edit_script(self) -> List[Tuple[int, int]]:
        """
        Find the shortest edit script using Myers' algorithm.
        
        This is the core of the algorithm. It explores the edit graph in
        increasing edit distance until it finds a path from start to end.
        
        Returns:
            List of (x, y) coordinates representing the path through the edit graph
        """
        n, m = self.n, self.m
        max_d = n + m  # Maximum possible edit distance
        
        # V stores the furthest reaching x-coordinate for each k-diagonal
        # k = x - y (diagonal number in the edit graph)
        # We use offset to handle negative indices: V[k] is stored at v[k + max_d]
        v = {1: 0}
        
        # Store the path for backtracking
        trace: List[Dict[int, int]] = []
        
        # Iterate through increasing edit distances
        for d in range(max_d + 1):
            trace.append(v.copy())
            
            # Explore all possible k-diagonals for this edit distance
            # k ranges from -d to d in steps of 2
            for k in range(-d, d + 1, 2):
                # Determine whether to move down or right
                # Move down if we're at the top edge OR if moving down gives us
                # a further x-coordinate than moving right
                if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                    # Move down (delete from A)
                    x = v.get(k + 1, 0)
                else:
                    # Move right (insert from B)
                    x = v.get(k - 1, 0) + 1
                
                y = x - k
                
                # Follow diagonal as far as possible (matching elements)
                while x < n and y < m and self._lines_equal(x, y):
                    x += 1
                    y += 1
                
                v[k] = x
                
                # Check if we've reached the end
                if x >= n and y >= m:
                    return self._backtrack(trace, d)
        
        # Should never reach here if inputs are valid
        return [(0, 0), (n, m)]

    def _lines_equal(self, x: int, y: int) -> bool:
        """
        Check if lines at positions x and y are equal.
        
        Args:
            x: Index in sequence A
            y: Index in sequence B
            
        Returns:
            True if lines are equal, False otherwise
        """
        return self.processed_a[x] == self.processed_b[y]

    def _backtrack(self, trace: List[Dict[int, int]], d: int) -> List[Tuple[int, int]]:
        """
        Backtrack through the trace to find the actual path.
        
        Args:
            trace: The trace of V values at each edit distance
            d: The final edit distance
            
        Returns:
            List of (x, y) coordinates representing the path
        """
        x, y = self.n, self.m
        path = [(x, y)]
        
        # Work backwards from d to 0
        for depth in range(d, 0, -1):
            v = trace[depth]
            k = x - y
            
            # Determine if we came from k-1 (right move) or k+1 (down move)
            if k == -depth or (k != depth and v.get(k - 1, -1) < v.get(k + 1, -1)):
                prev_k = k + 1
            else:
                prev_k = k - 1
            
            prev_x = v[prev_k]
            prev_y = prev_x - prev_k
            
            # Follow diagonal back
            while x > prev_x and y > prev_y:
                x -= 1
                y -= 1
                path.append((x, y))
            
            # Add the edit move
            if depth > 0:
                if x > prev_x:
                    # Came from right (insert)
                    path.append((prev_x, y))
                    x = prev_x
                else:
                    # Came from down (delete)
                    path.append((x, prev_y))
                    y = prev_y
        
        path.reverse()

        # Ensure the path always includes the origin and destination even when
        # there were zero edits (e.g., identical sequences). Without this the
        # diff builder can emit an empty result set for equal inputs.
        if not path or path[0] != (0, 0):
            path.insert(0, (0, 0))
        if path[-1] != (self.n, self.m):
            path.append((self.n, self.m))
        return path

    def _build_diff_results(self, path: List[Tuple[int, int]]) -> List[DiffResult]:
        """
        Build DiffResult objects from the edit path.
        
        Args:
            path: List of (x, y) coordinates through the edit graph
            
        Returns:
            List of DiffResult objects
        """
        results: List[DiffResult] = []
        
        i = 0
        while i < len(path) - 1:
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            
            # Diagonal move (equal lines)
            if x2 > x1 and y2 > y1:
                # Start of equal block
                equal_start_x = x1
                equal_start_y = y1
                
                # Find end of equal block
                j = i + 1
                while j < len(path) - 1:
                    x_next, y_next = path[j]
                    x_after, y_after = path[j + 1]
                    if x_after == x_next + 1 and y_after == y_next + 1:
                        j += 1
                    else:
                        break
                
                equal_end_x = path[j][0]
                equal_end_y = path[j][1]
                
                results.append(DiffResult(
                    type=DiffType.EQUAL,
                    old_start=equal_start_x,
                    old_count=equal_end_x - equal_start_x,
                    new_start=equal_start_y,
                    new_count=equal_end_y - equal_start_y,
                    old_lines=self.seq_a[equal_start_x:equal_end_x],
                    new_lines=self.seq_b[equal_start_y:equal_end_y]
                ))
                
                i = j
            
            # Right move (insert)
            elif x2 == x1 and y2 > y1:
                results.append(DiffResult(
                    type=DiffType.INSERT,
                    old_start=x1,
                    old_count=0,
                    new_start=y1,
                    new_count=1,
                    old_lines=[],
                    new_lines=self.seq_b[y1:y2]
                ))
                i += 1
            
            # Down move (delete)
            elif x2 > x1 and y2 == y1:
                results.append(DiffResult(
                    type=DiffType.DELETE,
                    old_start=x1,
                    old_count=1,
                    new_start=y1,
                    new_count=0,
                    old_lines=self.seq_a[x1:x2],
                    new_lines=[]
                ))
                i += 1
            
            else:
                i += 1
        
        # Merge consecutive inserts and deletes into replaces
        return self._merge_replace_operations(results)

    def _merge_replace_operations(self, results: List[DiffResult]) -> List[DiffResult]:
        """
        Merge consecutive DELETE and INSERT operations into REPLACE operations.
        
        Args:
            results: List of DiffResult objects
            
        Returns:
            List of DiffResult objects with merged REPLACE operations
        """
        merged: List[DiffResult] = []
        i = 0
        
        while i < len(results):
            if i < len(results) - 1:
                current = results[i]
                next_result = results[i + 1]
                
                # Check if current is DELETE and next is INSERT
                if current.type == DiffType.DELETE and next_result.type == DiffType.INSERT:
                    # Merge into REPLACE
                    merged.append(DiffResult(
                        type=DiffType.REPLACE,
                        old_start=current.old_start,
                        old_count=current.old_count,
                        new_start=next_result.new_start,
                        new_count=next_result.new_count,
                        old_lines=current.old_lines,
                        new_lines=next_result.new_lines
                    ))
                    i += 2
                    continue
            
            merged.append(results[i])
            i += 1
        
        return merged


def myers_diff(seq_a: List[str], seq_b: List[str], **options) -> List[DiffResult]:
    """
    Convenience function to compute diff using Myers' algorithm.
    
    Args:
        seq_a: First sequence
        seq_b: Second sequence
        **options: Additional options (ignore_case, ignore_whitespace, etc.)
        
    Returns:
        List of DiffResult objects
    """
    differ = MyersDiff(seq_a, seq_b, **options)
    return differ.compute()


def format_diff_unified(results: List[DiffResult], 
                       filename_a: str = "a",
                       filename_b: str = "b",
                       context_lines: int = 3) -> str:
    """
    Format diff results as unified diff format (like `diff -u`).
    
    Args:
        results: List of DiffResult objects
        filename_a: Name of first file
        filename_b: Name of second file
        context_lines: Number of context lines to show
        
    Returns:
        Unified diff format string
    """
    output = []
    output.append(f"--- {filename_a}")
    output.append(f"+++ {filename_b}")
    
    for result in results:
        if result.type == DiffType.EQUAL:
            continue
        
        # Create hunk header
        old_start = result.old_start + 1  # 1-indexed
        new_start = result.new_start + 1  # 1-indexed
        output.append(f"@@ -{old_start},{result.old_count} +{new_start},{result.new_count} @@")
        
        # Add lines
        if result.type == DiffType.DELETE or result.type == DiffType.REPLACE:
            for line in result.old_lines:
                output.append(f"-{line}")
        
        if result.type == DiffType.INSERT or result.type == DiffType.REPLACE:
            for line in result.new_lines:
                output.append(f"+{line}")
    
    return "\n".join(output)
