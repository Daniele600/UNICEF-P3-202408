import re


def get_markdown_text_between_tags(filepath: str, start_tag: str, end_tag: str) -> str:
    # read the file
    with open(filepath, "r") as f:
        text = f.read()

    # define the regex pattern
    pattern = f"{start_tag}(.*?){end_tag}"
    # pattern =r"<!--_Task1_result_start-->(.*?)<!--_Task1_result_end-->"

    # search for the pattern in the text (re.DOTALL matches newlines too)
    match = re.search(pattern, text, re.DOTALL)

    # Check if a match is found and print the result
    if match:
        result = match.group(1).strip()
        return result
    else:
        return ""