import sys
import re
import os
import subprocess
import codecs
import argparse
import glob

"""
limitation:
process all filenames with dash -> space   *-*.md

https://forum.obsidian.md/t/github-wiki-kinda-works-to-host-the-wiki/2980
"""

parser = argparse.ArgumentParser(description="Publish an Obsidian wiki to GitHub")
parser.add_argument('--no-push', action='store_true')

args = parser.parse_args()

print("--------PY 2---------")
branch = subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True)
print("--------PY 3---------")

if branch != b"obsidian\n":
    print("not on obsidian branch, exiting")
    sys.exit(0)

print("--------PY 4---------")
header, *filenames = subprocess.check_output("git log -1 --stat --oneline --name-only",
                                              shell=True).splitlines()
print("--------PY 5---------")
subprocess.run("git stash -u", shell=True)
print("--------PY 6---------")
subprocess.run("git checkout master&&git reset --hard obsidian", shell=True)

def get(x, i):
    return x[i] if len(x) > i else None

def transformLink(filename, match):
    link : str = match.group(1).split("#")
    text = match.group(2)
    
    file = get(link, 0)
    paragraph = get(link, 1)
    if not file:
        file = os.path.basename(filename)
        file = file.removesuffix(".md")
    file = file.replace("(", "\(")
    file = file.replace(")", "\)")
    
    if paragraph:
        paragraph = re.sub(r"[\(\)]", "", paragraph)
        link = file + "#" + paragraph
    else:
        link = file

    link = link.replace(" ", "-")
    return f"[[{text}\|{link}]]"

def transformCallback(filename):
    return lambda match: transformLink(filename, match)

try:
    print("--------PY 7 FILES---------")
    for filename in glob.glob("**/*.md", recursive=True):
        print(filename)
        with open(filename, mode="r+", encoding="utf-8") as file:
            text = file.read()
            ntext = re.sub(r"!\[\[(.+)\]\]", r"[[/images/\1]]", text)  # ![[imagename]] --> [[/images/imagename]]
            ntext = re.sub(r"\[\[(.+?)\\?\|(.+?)\]\]", transformCallback(filename), ntext)  # [[fn|linkTitle]] -> [[linkTitle\|fn]]
            ntext = re.sub(r"(?<!^)(?<!\s)(?=\n)(?!=\n)", "  ", ntext)  #two spaces at the end of same-paragraph line breaks
            if ntext != text:
                file.seek(0)
                file.write(ntext)

    print("--------PY 8 END FILES--------")
    subprocess.run("git add -A && git commit -m replace", shell=True)
    print("--------PY 9---------")
    if not args.no_push:
        subprocess.run("git push -f", shell=True)
finally:
    subprocess.run("git checkout obsidian&&git stash pop", shell=True)
    print("--------PY 10---------")
