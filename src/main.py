from textnode import *
from enum import Enum

import shutil
import os
import pathlib 

def copy_files():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    static_dir = os.path.join(base_dir, 'static')
    public_dir = os.path.join(base_dir, 'public')

# STEP 1: Clear out the public/ directory
    if os.path.exists(public_dir):
        for item in os.listdir(public_dir):
            item_path = os.path.join(public_dir, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print("Cleared public/ folder.")
    else:
        os.makedirs(public_dir)
        print("Created public/ folder.")

# STEP 2: Copy contents of static/ to public/
    for root, dirs, files in os.walk(static_dir):
        rel_path = os.path.relpath(root, static_dir)
        dest_root = os.path.join(public_dir, rel_path)
        os.makedirs(dest_root, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {src_file} → {dest_file}")

def extract_title(markdown):
    for line in markdown.split("\n"):
        stripped_line = line.strip()
        if stripped_line.startswith('# '):
            return stripped_line[2:].strip()
    raise Exception("No h1 Header in file")

# Generates page from the provided contents
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        from_md_content = file.read()

    with open(template_path, 'r') as file:
        template_content = file.read()

    HTML_String = markdown_to_html_node(from_md_content).to_html()
    title = extract_title(from_md_content)
    
    # Replace empty title and contents in template file
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", HTML_String)

    directory = os.path.dirname(dest_path)
    if directory:  # Only create if there's actually a directory path
        os.makedirs(directory, exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    crawl = os.listdir(dir_path_content)
    for content in crawl:
        if os.path.isfile(os.path.join(dir_path_content, content)):
            if content.endswith(".md"):
                output_html_filename = content.replace(".md", ".html")
                output_html_path = os.path.join(dest_dir_path,output_html_filename)
                generate_page(os.path.join(dir_path_content,content), template_path, output_html_path)

        else:
            os.makedirs(os.path.join(dest_dir_path, content), exist_ok=True)
            generate_pages_recursive(os.path.join(dir_path_content,content), template_path, os.path.join(dest_dir_path, content))

        


def main():
    copy_files()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()