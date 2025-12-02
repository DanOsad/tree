#!/usr/bin/env python3

import os
import glob
from enum import Enum
from argparse import ArgumentParser
from pathlib import Path
from typing import List

class TreeElements(Enum):
    FILE = "├──"
    LINK = "->"
    DIRECTORY = "└──"
    LAST = "└──"

class ItemType(Enum):
    FILE = "file"
    LINK = "link"
    DIRECTORY = "directory"

class Item:
    def __init__(self, name: str):
        if not isinstance(name, Path):
            self.path = Path(name).resolve()
        else:
            self.path = name
        self.name = self.path.name

    def is_file(self) -> bool:
        return isinstance(self, File)

    def is_link(self) -> bool:
        return isinstance(self, Link)

    def is_directory(self) -> bool:
        return isinstance(self, Directory)

    @property
    def type(self) -> ItemType:
        if self.is_file():
            return ItemType.FILE
        elif self.is_link():
            return ItemType.LINK
        elif self.is_directory():
            return ItemType.DIRECTORY
        else:
            raise ValueError("Unknown item type")

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        base_repr = f'{self.type.value.capitalize()}(name="{self.name}", path="{self.path}"'
        if self.is_link():
            return f'{base_repr}, target="{self.target}")'
        elif self.is_directory():
            return f'{base_repr}, children={len(self.children) if self.children is not None else 0})'
        else:
            return f'{base_repr})'

class Link(Item):
    def __init__(self, name: str, target: str):
        super().__init__(name)
        self.target = target

    def __repr__(self) -> str:
        return f'Link(name="{self.name}", path="{self.path}", target="{self.target}")'

class File(Item):
    def __init__(self, name: str):
        super().__init__(name)

class Directory(Item):
    def __init__(self, name: str, children: List[Item] = None):
        super().__init__(name)
        self.children = children if children is not None else []

class Tree:
    def __init__(self, root: str, max_depth: int = None, exclude: List[str] = None):
        self.root = root
        self.max_depth = max_depth
        self.exclude = exclude if exclude is not None else []
        self.validate_root()

    def validate_root(self) -> None:
        if isinstance(self.root, str):
            try:
                self.root = Directory(self.root)
            except Exception as e:
                raise ValueError(f"Invalid root path: {e}")
        if not self.root.is_directory():
            raise ValueError("Root must be a directory")

    def break_condition(self, current_depth: int) -> bool:
        return (self.max_depth is None) or (current_depth < self.max_depth)

    def skip_condition(self, item: Path) -> bool:
        for pattern in self.exclude:
            if glob.fnmatch.fnmatch(item.name, pattern):
                return True
        return False

    def process_item(self, item: Path, current_depth: int) -> None:
        if self.skip_condition(item):
            return None
        if item.is_dir():
            dir_item = Directory(item)
            if self.break_condition(current_depth):
                self.traverse_tree(dir_item, current_depth + 1)
            return dir_item
        elif item.is_symlink():
            target = os.readlink(item)
            link_item = Link(item, target)
            return link_item
        else:
            file_item = File(item)
            return file_item
    
    def traverse_tree(self, root: Item, current_depth: int = 0) -> None:
        for entry in sorted(root.path.iterdir()):
            processed_item = self.process_item(entry, current_depth)
            if processed_item is not None:
                root.children.append(processed_item)

class GraphTree:
    def __init__(self, root: Item) -> None:
        self.root = root

    def draw(self, item: Item = None, prefix: str = "", is_last: bool = True) -> None:
        if item is None:
            item = self.root
            print(f"{item.name}/")
        
        if not item.is_directory() or not item.children:
            return
        
        children = [child for child in item.children if child is not None]
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            
            connector = TreeElements.LAST.value if is_last_child else TreeElements.FILE.value
            
            if child.is_directory():
                display_name = f"{child.name}/"
            else:
                display_name = child.name
            
            print(f"{prefix}{connector} {display_name}", end="")
            
            if child.is_link():
                print(f" {TreeElements.LINK.value} {child.target}")
            else:
                print()
            
            if child.is_directory():
                extension = "    " if is_last_child else "│   "
                self.draw(child, prefix + extension, is_last_child)

def get_args() -> ArgumentParser:
    parser = ArgumentParser(description="Display directory tree structure")
    parser.add_argument(
        "-d", "--depth", 
        type=int, 
        default=None, 
        help="Limit the depth of the tree"
    )
    parser.add_argument(
        "paths", 
        nargs="*",
        help="Path(s) to display the tree for (defaults to current directory)"
    )
    parser.add_argument(
        "-e", "--exclude",
        action="append",
        default=[],
        help="Patterns to exclude from the tree (can be used multiple times)"
    )
    args = parser.parse_args()
    
    if not args.paths:
        args.paths.extend([os.getcwd()])

    if not args.exclude:
        args.exclude.extend(['__pycache__', '*venv*', '.git'])
    
    return args

def main(args) -> None:
    for root_dir in args.paths:
        root_dir = Directory(root_dir)
        tree = Tree(root_dir, args.depth, args.exclude)
        tree.traverse_tree(tree.root)
        GraphTree(tree.root).draw()

if __name__ == "__main__":
    args = get_args()
    main(args)
