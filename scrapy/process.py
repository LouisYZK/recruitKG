import re


def clean_doc(doc):
    pattern = re.compile(r'[\u4e00-\u9fa5 A-Z a-z 0-9]+')
    filter_data = re.findall(pattern,doc)
    cleaned_doc = ''.join(filter_data)
    return cleaned_doc