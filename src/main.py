from textnode import TextType, TextNode
from htmlnode import HTMLNode
from sitecopy import *
from pathlib import Path
import sys

def main():
    update_site()

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(basepath)

    root_dir = Path(__file__).parent.parent.resolve()
    content_dir = root_dir / "content"
    public_dir = root_dir / "public"
    template_file = root_dir / "template.html"

    generate_pages_recursive(content_dir, public_dir, template_file, basepath)

if __name__ == "__main__":
    main()
