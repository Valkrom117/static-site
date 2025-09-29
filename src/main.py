from textnode import TextNode, TextType
import os
import shutil
from markdown_to_html import markdown_to_html_node

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_static("static", "public")

    # origin_paths = ["content/index.md",
    #                 "content/blog/glorfindel/index.md",
    #                 "content/blog/majesty/index.md",
    #                 "content/blog/tom/index.md",
    #                 "content/contact/index.md"]
    
    # public_paths = ["public/index.html",
    #                 "public/blog/glorfindel/index.html",
    #                 "public/blog/majesty/index.html",
    #                 "public/blog/tom/index.html",
    #                 "public/contact/index.html"]

    # for i in range(0, len(origin_paths)):
    #     generate_page(origin_paths[i], "template.html", public_paths[i])
    generate_pages_recursive("./content", "template.html", "./public")


def copy_static(origin, target):
    if not os.path.exists(origin):
        raise Exception("Invalid origin directory")
    os.makedirs(target, exist_ok=True)
    
    filesToCopy = os.listdir(origin)
    for file in filesToCopy:
        filePath = os.path.join(origin, file)
        if os.path.isfile(filePath):
            shutil.copy(filePath, os.path.join(target, file))
        else: 
            copy_static(filePath, os.path.join(target, file))

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.lstrip()
        if line.startswith("# "): return line[1:].lstrip().rstrip()
    raise Exception("No Title header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md:
        markdown = md.read()

    with open(template_path) as temp:
        page = temp.read()

    htmlString = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    page = page.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", htmlString)

    dirpath = os.path.dirname(dest_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Invalid origin directory")
    os.makedirs(dest_dir_path, exist_ok=True)

    for name in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, name)
        dst_path = os.path.join(dest_dir_path, name)

        if os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dst_path)
        elif name.endswith(".md") and os.path.isfile(src_path):
            dest_html = os.path.join(dest_dir_path, name[:-3] + ".html")
            generate_page(src_path, template_path, dest_html)
        # else: ignore non-markdown files



main()