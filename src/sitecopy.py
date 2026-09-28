import os
from pathlib import Path
import shutil
import re
from md_parser import *

def update_site():
    root_dir = Path(__file__).parent.parent.resolve()
    target_dir = root_dir / "docs"
    source_dir = root_dir / "static"
    print(f"Retrieving files from {source_dir.relative_to(root_dir)}")
    if target_dir.exists() and target_dir.is_dir():
        shutil.rmtree(target_dir)
        print(f"Successfully deleted {target_dir.relative_to(root_dir)} and all of its contents.")
    else:
        print("Directory does not exist.")

    try:
        # copytree copies the folder, subfolders, and files
        shutil.copytree(source_dir, target_dir)
        print(f"Successfully copied to: {target_dir.relative_to(root_dir)}")
    except FileExistsError:
        print(f"Error: The destination folder '{target_dir.relative_to(root_dir)}' already exists.")
    except FileNotFoundError:
        print("Error: The source folder could not be found.")

def extract_title(markdown) -> str:
    header = re.search(r"^#+\s.*", markdown).group()
    return header.strip("# ")

def generate_page(source: Path, dest: Path, template: Path, basepath: Path):
    root_dir = Path(__file__).parent.parent.resolve()
    md = None
    html = None

    if source.is_file():
        md = source.read_text(encoding="utf-8")
    else:
        print("Source file not found")

    if template.is_file():
        html = template.read_text(encoding="utf-8")
    else:
        print("Template file not found")
    
    content = markdown_to_html(md).to_html()
    title_split = html.split("{{ Title }}", 1)
    html = extract_title(md).join(title_split)
    content_split = html.split("{{ Content }}", 1)
    html = content.join(content_split)
    html = html.replace('href="/', f'href="/{basepath}')
    html = html.replace('src="/', f'src="/{basepath}')
    
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"File written succesfully: {dest.relative_to(root_dir)}")

def generate_pages_recursive(content_dir: Path, dest_dir: Path, template_file: Path, basepath: Path):
    root_dir = Path(__file__).parent.parent.resolve()
    print(root_dir)
    filepaths_to_copy = [p for p in content_dir.rglob('*') if p.is_file()]
    filepaths_to_paste = [root_dir / "public" / p.relative_to(root_dir / "content").with_suffix(".html") for p in filepaths_to_copy]
    print("\n\n")
    for i in range(len(filepaths_to_paste)):
        generate_page(filepaths_to_copy[i], filepaths_to_paste[i], template_file, basepath)
