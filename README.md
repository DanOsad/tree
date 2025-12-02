# Tree - Directory Structure Visualizer

A Python-based directory tree visualization tool that displays the hierarchical structure of directories and files in a clear, graphical format.

## Features

- **Recursive directory traversal** with configurable depth limits
- **Visual tree structure** using box-drawing characters
- **Pattern-based exclusion** to filter out unwanted files/directories
- **Symlink detection** showing link targets
- **Directory indicators** with `/` suffix
- **Color-coded output** (inherits from terminal)

## Installation

No installation required - just ensure Python 3 is installed on your system.

```bash
chmod +x tree.py
```

## Usage

```bash
./tree.py [OPTIONS] [PATHS...]
```

### Arguments

- `PATHS` - One or more directories to visualize (defaults to current directory if not specified)

### Options

- `-d, --depth DEPTH` - Limit the depth of the tree traversal (unlimited by default)
- `-e, --exclude PATTERN` - Exclude files/directories matching the glob pattern (can be used multiple times)
- `-h, --help` - Show help message

## Examples

### Basic Usage

Display tree for current directory:
```bash
./tree.py
```

Display tree for specific directory:
```bash
./tree.py /path/to/directory
```

### Multiple Directories

Visualize multiple directories:
```bash
./tree.py /path/one /path/two /path/three
```

### Depth Limiting

Show only 2 levels deep:
```bash
./tree.py -d 2
```

Show only top-level contents (depth 1):
```bash
./tree.py -d 1 /path/to/directory
```

### Excluding Patterns

Exclude Python cache files:
```bash
./tree.py -e "__pycache__" -e "*.pyc"
```

Exclude multiple patterns:
```bash
./tree.py -e "*venv*" -e ".git" -e "node_modules" -d 3
```

### Combined Options

Show tree with depth limit and exclusions:
```bash
./tree.py create_project/ -d 2 -e "__pycache__" -e "*venv*" -e ".git"
```

## Output Format

The tool uses standard tree visualization characters:

- `├──` - Non-last item in a directory
- `└──` - Last item in a directory
- `│` - Vertical line showing tree continuation
- `->` - Symlink indicator
- `/` - Directory suffix

### Example Output

```
project/
├── .env
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── utils/
│       ├── helpers.py
│       └── config.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── requirements.txt
└── setup.py -> ../setup/setup.py
```

## How It Works

1. **Tree Building**: Recursively traverses the file system starting from the root directory
2. **Filtering**: Applies exclusion patterns using glob matching
3. **Depth Control**: Stops traversal when maximum depth is reached
4. **Rendering**: Uses depth-first traversal to draw the tree with proper indentation and connectors

## File Structure

The tool consists of several classes:

- `Item` - Base class for file system items
- `File` - Represents regular files
- `Directory` - Represents directories with children
- `Link` - Represents symbolic links
- `Tree` - Handles directory traversal and tree building
- `GraphTree` - Handles tree rendering and visualization

## Limitations

- Symbolic link loops are not explicitly detected (Python's path resolution handles this)
- Very deep directory structures may hit Python's recursion limit
- No color output (uses terminal defaults)
- Excludes are based on name matching only, not full paths

## Troubleshooting

**RecursionError**: If you encounter recursion depth errors, use the `-d` flag to limit depth:
```bash
./tree.py -d 5
```

**Permission Denied**: Some directories may not be readable. The tool will skip these silently.

**Too Much Output**: Use exclusion patterns and depth limits to reduce output:
```bash
./tree.py -d 3 -e ".*" -e "__*" -e "node_modules"
```

## License

This tool is provided as-is for internal use.

## Author

Created for directory structure visualization and documentation purposes.
