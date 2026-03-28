import ast
import os

def insert_logging(filepath):
    print(f"Adding logging to {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"Skipping {filepath} due to parsing error: {e}")
        return

    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.body:
                continue
                
            first_stmt = node.body[0]
            
            # Check if docstring
            if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Constant) and isinstance(first_stmt.value.value, str):
                if len(node.body) > 1:
                    target_lineno = node.body[1].lineno - 1
                    col_offset = node.body[1].col_offset
                else:
                    target_lineno = first_stmt.end_lineno
                    col_offset = node.col_offset + 4 # fall back to standard indent
            else:
                target_lineno = first_stmt.lineno - 1
                col_offset = first_stmt.col_offset
                
            functions.append({
                'name': node.name,
                'target_lineno': target_lineno,
                'col_offset': col_offset
            })
                
    if not functions:
        return
        
    lines = source.split('\n')
    
    functions.sort(key=lambda x: x['target_lineno'], reverse=True)
    
    for f in functions:
        indent = " " * f['col_offset']
        # Insert them in reverse order to maintain correct ordering when inserting at same index
        lines.insert(f['target_lineno'], f"{indent}print(f'DEBUG: Executing {{__name__}}.{f['name']}')")
        lines.insert(f['target_lineno'], f"{indent}logger.info(f'Observability: {{__name__}}.{f['name']} was called')")
        
    insert_pos = 0
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == '__future__':
            insert_pos = max(insert_pos, node.end_lineno)
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            insert_pos = max(insert_pos, node.end_lineno)
            
    logger_setup = [
        "import logging",
        "try:",
        "    from utils.logger import get_logger",
        "    logger = get_logger(__name__)",
        "except (ImportError, ModuleNotFoundError):",
        "    logger = logging.getLogger(__name__)",
        "    if not logger.handlers:",
        "        logger.addHandler(logging.StreamHandler())",
        "        logger.setLevel(logging.INFO)"
    ]
    
    for line in reversed(logger_setup):
        lines.insert(insert_pos, line)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        if 'venv' in dirs:
            dirs.remove('venv')
        for file in files:
            p = os.path.join(root, file).replace('\\', '/')
            if file.endswith('.py') and file != 'add_logging.py' and not p.endswith('utils/logger.py'):
                insert_logging(os.path.join(root, file))
