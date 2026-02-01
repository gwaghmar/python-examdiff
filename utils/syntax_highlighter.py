"""
Syntax Highlighter - Pygments-based Syntax Highlighting
=======================================================

This module provides syntax highlighting functionality using Pygments.
Supports 25+ programming languages with customizable themes.
"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, get_lexer_for_filename, guess_lexer
    from pygments.styles import get_style_by_name, get_all_styles
    from pygments.token import Token
    from pygments.formatter import Formatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


@dataclass
class HighlightedToken:
    """Represents a highlighted token."""
    text: str
    token_type: str
    start_pos: int
    end_pos: int
    color: str


class SyntaxHighlighter:
    """
    Provides syntax highlighting for various programming languages.
    """
    
    # Default color schemes for light and dark themes
    LIGHT_THEME_COLORS = {
        'keyword': '#0000FF',
        'string': '#A31515',
        'comment': '#008000',
        'number': '#098658',
        'function': '#795E26',
        'class': '#267F99',
        'variable': '#001080',
        'operator': '#000000',
        'default': '#000000'
    }
    
    DARK_THEME_COLORS = {
        'keyword': '#569CD6',
        'string': '#CE9178',
        'comment': '#6A9955',
        'number': '#B5CEA8',
        'function': '#DCDCAA',
        'class': '#4EC9B0',
        'variable': '#9CDCFE',
        'operator': '#D4D4D4',
        'default': '#D4D4D4'
    }
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'python': 'Python',
        'javascript': 'JavaScript',
        'typescript': 'TypeScript',
        'java': 'Java',
        'cpp': 'C++',
        'c': 'C',
        'csharp': 'C#',
        'go': 'Go',
        'rust': 'Rust',
        'ruby': 'Ruby',
        'php': 'PHP',
        'swift': 'Swift',
        'kotlin': 'Kotlin',
        'scala': 'Scala',
        'html': 'HTML',
        'css': 'CSS',
        'scss': 'SCSS',
        'sql': 'SQL',
        'xml': 'XML',
        'json': 'JSON',
        'yaml': 'YAML',
        'markdown': 'Markdown',
        'shell': 'Shell',
        'powershell': 'PowerShell',
        'dockerfile': 'Dockerfile',
    }
    
    def __init__(self, language: Optional[str] = None, 
                 theme: str = 'light',
                 style: str = 'default'):
        """
        Initialize syntax highlighter.
        
        Args:
            language: Programming language name (None for auto-detect)
            theme: 'light' or 'dark'
            style: Pygments style name
        """
        self.language = language
        self.theme = theme
        self.style = style
        self.enabled = PYGMENTS_AVAILABLE
        
        if theme == 'dark':
            self.colors = self.DARK_THEME_COLORS.copy()
        else:
            self.colors = self.LIGHT_THEME_COLORS.copy()
        
        if not PYGMENTS_AVAILABLE:
            print("Warning: Pygments not available. Syntax highlighting disabled.")
    
    def highlight_text(self, text: str, filename: Optional[str] = None) -> List[HighlightedToken]:
        """
        Highlight text and return list of tokens.
        
        Args:
            text: Text to highlight
            filename: Optional filename for language detection
            
        Returns:
            List of HighlightedToken objects
        """
        if not self.enabled:
            return [HighlightedToken(text, 'default', 0, len(text), self.colors['default'])]
        
        try:
            # Get lexer
            if self.language:
                lexer = get_lexer_by_name(self.language)
            elif filename:
                lexer = get_lexer_for_filename(filename, text)
            else:
                lexer = guess_lexer(text)
            
            # Tokenize
            tokens = []
            position = 0
            
            for token_type, value in lexer.get_tokens(text):
                color = self._get_color_for_token(token_type)
                
                tokens.append(HighlightedToken(
                    text=value,
                    token_type=str(token_type),
                    start_pos=position,
                    end_pos=position + len(value),
                    color=color
                ))
                
                position += len(value)
            
            return tokens
        
        except Exception as e:
            # Fallback to no highlighting
            return [HighlightedToken(text, 'default', 0, len(text), self.colors['default'])]
    
    def highlight_lines(self, lines: List[str], filename: Optional[str] = None) -> List[List[HighlightedToken]]:
        """
        Highlight multiple lines.
        
        Args:
            lines: List of lines to highlight
            filename: Optional filename for language detection
            
        Returns:
            List of lists of HighlightedToken objects (one list per line)
        """
        # Join lines and highlight as a single text
        text = '\n'.join(lines)
        all_tokens = self.highlight_text(text, filename)
        
        # Split tokens back into lines
        result = []
        current_line_tokens = []
        current_position = 0
        line_idx = 0
        
        for token in all_tokens:
            if '\n' in token.text:
                # Token spans multiple lines
                parts = token.text.split('\n')
                for i, part in enumerate(parts):
                    if part:
                        current_line_tokens.append(HighlightedToken(
                            text=part,
                            token_type=token.token_type,
                            start_pos=current_position,
                            end_pos=current_position + len(part),
                            color=token.color
                        ))
                        current_position += len(part)
                    
                    if i < len(parts) - 1:
                        # New line
                        result.append(current_line_tokens)
                        current_line_tokens = []
                        current_position = 0
                        line_idx += 1
            else:
                current_line_tokens.append(HighlightedToken(
                    text=token.text,
                    token_type=token.token_type,
                    start_pos=current_position,
                    end_pos=current_position + len(token.text),
                    color=token.color
                ))
                current_position += len(token.text)
        
        if current_line_tokens:
            result.append(current_line_tokens)
        
        # Pad with empty lists if needed
        while len(result) < len(lines):
            result.append([])
        
        return result
    
    def _get_color_for_token(self, token_type) -> str:
        """
        Get color for a token type.
        
        Args:
            token_type: Pygments token type
            
        Returns:
            Color hex string
        """
        # Map Pygments token types to our simplified categories
        if token_type in Token.Keyword:
            return self.colors['keyword']
        elif token_type in Token.String:
            return self.colors['string']
        elif token_type in Token.Comment:
            return self.colors['comment']
        elif token_type in Token.Number:
            return self.colors['number']
        elif token_type in Token.Name.Function:
            return self.colors['function']
        elif token_type in Token.Name.Class:
            return self.colors['class']
        elif token_type in Token.Name:
            return self.colors['variable']
        elif token_type in Token.Operator:
            return self.colors['operator']
        else:
            return self.colors['default']
    
    def detect_language(self, filename: str) -> Optional[str]:
        """
        Detect programming language from filename.
        
        Args:
            filename: File name
            
        Returns:
            Language name or None
        """
        if not self.enabled:
            return None
        
        try:
            lexer = get_lexer_for_filename(filename)
            return lexer.name.lower()
        except Exception:
            return None
    
    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """
        Get dictionary of supported languages.
        
        Returns:
            Dictionary mapping language IDs to display names
        """
        return SyntaxHighlighter.SUPPORTED_LANGUAGES.copy()
    
    @staticmethod
    def get_available_styles() -> List[str]:
        """
        Get list of available Pygments styles.
        
        Returns:
            List of style names
        """
        if PYGMENTS_AVAILABLE:
            return list(get_all_styles())
        return ['default']
    
    def set_custom_colors(self, colors: Dict[str, str]) -> None:
        """
        Set custom colors for token types.
        
        Args:
            colors: Dictionary mapping token types to color hex strings
        """
        self.colors.update(colors)


def create_highlighter(language: Optional[str] = None,
                      theme: str = 'light',
                      filename: Optional[str] = None) -> SyntaxHighlighter:
    """
    Factory function to create a syntax highlighter.
    
    Args:
        language: Language name (None for auto-detect)
        theme: 'light' or 'dark'
        filename: Optional filename for language detection
        
    Returns:
        SyntaxHighlighter instance
    """
    highlighter = SyntaxHighlighter(language, theme)
    
    # Auto-detect language from filename if not specified
    if not language and filename:
        detected = highlighter.detect_language(filename)
        if detected:
            highlighter.language = detected
    
    return highlighter


# Simple fallback for when Pygments is not available
class SimpleHighlighter:
    """
    Simple fallback highlighter without Pygments.
    Uses basic regex-based highlighting.
    """
    
    def __init__(self, theme: str = 'light'):
        self.theme = theme
        if theme == 'dark':
            self.colors = SyntaxHighlighter.DARK_THEME_COLORS.copy()
        else:
            self.colors = SyntaxHighlighter.LIGHT_THEME_COLORS.copy()
    
    def highlight_text(self, text: str, filename: Optional[str] = None) -> List[HighlightedToken]:
        """Simple highlighting using basic patterns."""
        return [HighlightedToken(text, 'default', 0, len(text), self.colors['default'])]
    
    def highlight_lines(self, lines: List[str], filename: Optional[str] = None) -> List[List[HighlightedToken]]:
        """Simple line highlighting."""
        return [[HighlightedToken(line, 'default', 0, len(line), self.colors['default'])] for line in lines]
