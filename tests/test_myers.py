"""
Test Myers Algorithm
===================

Unit tests for the Myers diff algorithm implementation.
"""

import pytest
from core.myers_algorithm import MyersDiff, DiffType, myers_diff, format_diff_unified


class TestMyersDiff:
    """Test Myers diff algorithm."""
    
    def test_identical_sequences(self):
        """Test diff of identical sequences."""
        seq_a = ["line1", "line2", "line3"]
        seq_b = ["line1", "line2", "line3"]
        
        results = myers_diff(seq_a, seq_b)
        
        assert len(results) == 1
        assert results[0].type == DiffType.EQUAL
        assert results[0].old_count == 3
    
    def test_all_different(self):
        """Test diff of completely different sequences."""
        seq_a = ["a", "b", "c"]
        seq_b = ["x", "y", "z"]
        
        results = myers_diff(seq_a, seq_b)
        
        # Should have delete and insert operations
        has_delete = any(r.type == DiffType.DELETE for r in results)
        has_insert = any(r.type == DiffType.INSERT for r in results)
        
        assert has_delete or has_insert
    
    def test_insertion(self):
        """Test insertion detection."""
        seq_a = ["line1", "line3"]
        seq_b = ["line1", "line2", "line3"]
        
        results = myers_diff(seq_a, seq_b)
        
        # Should detect insertion
        has_insert = any(r.type == DiffType.INSERT and "line2" in r.new_lines for r in results)
        assert has_insert
    
    def test_deletion(self):
        """Test deletion detection."""
        seq_a = ["line1", "line2", "line3"]
        seq_b = ["line1", "line3"]
        
        results = myers_diff(seq_a, seq_b)
        
        # Should detect deletion
        has_delete = any(r.type == DiffType.DELETE and "line2" in r.old_lines for r in results)
        assert has_delete
    
    def test_replacement(self):
        """Test replacement detection."""
        seq_a = ["line1", "old_line", "line3"]
        seq_b = ["line1", "new_line", "line3"]
        
        results = myers_diff(seq_a, seq_b)
        
        # Should detect replacement
        has_replace = any(r.type == DiffType.REPLACE for r in results)
        assert has_replace
    
    def test_ignore_case(self):
        """Test case-insensitive comparison."""
        seq_a = ["Hello World"]
        seq_b = ["hello world"]
        
        results = myers_diff(seq_a, seq_b, ignore_case=True)
        
        assert len(results) == 1
        assert results[0].type == DiffType.EQUAL
    
    def test_ignore_whitespace(self):
        """Test whitespace-insensitive comparison."""
        seq_a = ["hello   world"]
        seq_b = ["hello world"]
        
        results = myers_diff(seq_a, seq_b, ignore_whitespace=True)
        
        assert len(results) == 1
        assert results[0].type == DiffType.EQUAL
    
    def test_empty_sequences(self):
        """Test empty sequences."""
        results = myers_diff([], [])
        assert len(results) == 0 or (len(results) == 1 and results[0].type == DiffType.EQUAL)
    
    def test_one_empty_sequence(self):
        """Test one empty sequence."""
        seq_a = ["line1", "line2"]
        seq_b = []
        
        results = myers_diff(seq_a, seq_b)
        
        # Should have deletions
        has_delete = any(r.type == DiffType.DELETE for r in results)
        assert has_delete
    
    def test_unified_diff_format(self):
        """Test unified diff format generation."""
        seq_a = ["line1", "line2", "line3"]
        seq_b = ["line1", "modified", "line3"]
        
        results = myers_diff(seq_a, seq_b)
        unified = format_diff_unified(results, "file_a.txt", "file_b.txt")
        
        assert "---" in unified
        assert "+++" in unified
    
    def test_long_common_prefix(self):
        """Test sequences with long common prefix."""
        seq_a = ["line1", "line2", "line3", "old"]
        seq_b = ["line1", "line2", "line3", "new"]
        
        results = myers_diff(seq_a, seq_b)
        
        # Should have equal block for common prefix
        assert results[0].type == DiffType.EQUAL
        assert results[0].old_count == 3
    
    def test_long_common_suffix(self):
        """Test sequences with long common suffix."""
        seq_a = ["old", "line1", "line2", "line3"]
        seq_b = ["new", "line1", "line2", "line3"]
        
        results = myers_diff(seq_a, seq_b)
        
        # Should have equal block for common suffix
        has_equal = any(r.type == DiffType.EQUAL and r.old_count == 3 for r in results)
        assert has_equal


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
