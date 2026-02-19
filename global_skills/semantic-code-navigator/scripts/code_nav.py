import os
import sys
import re
import argparse

class CodeNavigator:
    def __init__(self):
        self.patterns = {
            'python': {
                'class': r'^class\s+([a-zA-Z0-9_]+)',
                'function': r'^\s*def\s+([a-zA-Z0-9_]+)\s*\('
            },
            'typescript': {
                'class': r'class\s+([a-zA-Z0-9_]+)',
                'function': r'(?:async\s+)?function\s+([a-zA-Z0-9_]+)\s*\(|const\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\(',
                'interface': r'interface\s+([a-zA-Z0-9_]+)'
            },
            'shell': {
                'function': r'^([a-zA-Z0-9_]+)\s*\(\s*\)\s*\{'
            }
        }

    def _get_lang(self, file_path):
        ext = file_path.split('.')[-1]
        if ext in ['ts', 'tsx', 'js', 'jsx']: return 'typescript'
        if ext == 'py': return 'python'
        if ext in ['sh', 'bash']: return 'shell'
        return None

    def map_file(self, file_path):
        """Returns a summary of the symbols in the file."""
        if not os.path.exists(file_path):
            return f"Error: File {file_path} not found."
        
        lang = self._get_lang(file_path)
        if not lang:
            return "Error: Unsupported language extension."

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        summary = []
        for i, line in enumerate(lines):
            for symbol_type, pattern in self.patterns[lang].items():
                match = re.search(pattern, line)
                if match:
                    # Get the name from the correct capturing group
                    name = match.group(1)
                    summary.append({
                        'type': symbol_type,
                        'name': name,
                        'line': i + 1
                    })
        
        return summary

    def extract_symbol(self, file_path, symbol_name):
        """Extracts the code block for a specific symbol using language-aware logic."""
        if not os.path.exists(file_path):
            return f"Error: File {file_path} not found."

        lang = self._get_lang(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_idx = -1
        symbol_pattern = ""
        # Search for the symbol definition
        for i, line in enumerate(lines):
            # Check all possible patterns for this lang to find the definition line
            for s_type, pattern in self.patterns[lang].items():
                if re.search(rf"\b{symbol_name}\b", line) and re.search(pattern, line):
                    start_idx = i
                    break
            if start_idx != -1: break
        
        if start_idx == -1:
            return f"Error: Symbol {symbol_name} not found."

        # Extraction Logic
        if lang == 'python':
            return self._extract_python(lines, start_idx)
        elif lang in ['typescript', 'shell']:
            return self._extract_braced(lines, start_idx)
        
        return "".join(lines[start_idx : start_idx + 50]) # Fallback

    def _extract_python(self, lines, start_idx):
        """Extracts Python block based on indentation."""
        start_line = lines[start_idx]
        base_indent = len(start_line) - len(start_line.lstrip())
        
        extracted = [start_line]
        
        # Find the first line of the body to determine body indentation
        body_start_idx = start_idx + 1
        while body_start_idx < len(lines) and (not lines[body_start_idx].strip() or lines[body_start_idx].strip().startswith('#')):
            extracted.append(lines[body_start_idx])
            body_start_idx += 1
            
        if body_start_idx >= len(lines):
            return "".join(extracted)
            
        first_body_line = lines[body_start_idx]
        body_indent = len(first_body_line) - len(first_body_line.lstrip())
        
        # If the next non-empty line isn't more indented, it's a one-liner or empty
        if body_indent <= base_indent and lines[body_start_idx].strip():
             return "".join(extracted)

        # Continue until we find a line with indentation <= base_indent
        for i in range(body_start_idx, len(lines)):
            line = lines[i]
            if line.strip():
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= base_indent and not line.strip().startswith('#'):
                    break
            extracted.append(line)
            
        return "".join(extracted)

    def _extract_braced(self, lines, start_idx):
        """Extracts blocks enclosed in braces {}."""
        content = "".join(lines[start_idx:])
        
        # Simple brace counting
        brace_count = 0
        started = False
        end_pos = -1
        
        for i, char in enumerate(content):
            if char == '{':
                brace_count += 1
                started = True
            elif char == '}':
                brace_count -= 1
                if started and brace_count == 0:
                    end_pos = i + 1
                    break
        
        if end_pos != -1:
            return content[:end_pos]
        return "".join(lines[start_idx : start_idx + 50]) # Fallback

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic Code Navigator")
    parser.add_argument("--map", help="File to map")
    parser.add_argument("--extract", help="Symbol to extract")
    parser.add_argument("--file", help="File to extract from")
    
    args = parser.parse_args()
    nav = CodeNavigator()
    
    if args.map:
        result = nav.map_file(args.map)
        import json
        print(json.dumps(result, indent=2))
    elif args.extract and args.file:
        print(nav.extract_symbol(args.file, args.extract))