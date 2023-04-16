import xml.etree.ElementTree as ET
from glob import glob
import pandas as pd
import pathlib


hierarchy = ["title", "subtitle", "chapter", "subchapter", "part", "subpart", "division", "subdivison", "article",
             "subarticle", "section", "subsection", "paragraph", "subparagraph", "item", "subitem"]





def strip_namespace(tag: str):
    _, _, tag = tag.rpartition("}")
    return tag


def parse_hierarchy(df, element, identifier=None, heading=None):
    element_tag = strip_namespace(element.tag)
    for item in element:
        item_tag = strip_namespace(item.tag)
        if "identifier" in item.attrib:
            identifier = item.attrib["identifier"]
        if element_tag == "section":
            if item_tag == "heading":
                heading = item.text
        if item_tag == "content":
            parse_content(df, item, identifier, heading)
        elif item_tag not in hierarchy:
            continue
        else:
            parse_hierarchy(df, item, identifier, heading)

def parse_content(dict_list, element, identifier: str, heading: str):
    text = ""
    for item in element:
        item_tag = strip_namespace(item.tag)
        if item_tag == "p" and item.text:
            text += item.text.strip()

    if text and len(text.split()) > 5:
        #print(heading, "|", text, identifier)
        dict_list.append({"heading": heading, "identifier": identifier, "text": text, "keywords": ""})
        with open(f"text/{len(dict_list)}.txt", "w") as f:
            f.write(text)

def parse_usc():
    merged_entries = []
    for file in glob("xml_usc/*.xml"):
        print(file)
        tree = ET.parse(file)
        root = tree.getroot()
        ls = []
        for item in root:
            tag = strip_namespace(item.tag)
            if tag == "main":
                parse_hierarchy(ls, item)

        merged_entries.extend(ls)
        df = pd.DataFrame(ls)
        if df.shape[0] > 0:
            df.to_csv(f"parsed/{pathlib.Path(file).stem}.csv", index=False)

    merged_df = pd.DataFrame(merged_entries)
    merged_df.to_csv("merged_usc.csv", index=False)

if __name__ == '__main__':
    parse_usc()