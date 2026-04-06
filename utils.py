from pathlib import Path


def read_index(topic: str):
    try:
        with open(f"./wikis/{topic}/index.md", "r") as f:
            index = f.read()
            return index
    except FileNotFoundError:
        print(f"Index file for {topic} not found")
        return "No index file found"
    except PermissionError:
        print(f"Permission denied for {topic} index")


def update_index(topic: str, new_index: str):
    try:
        with open(f"./wikis/{topic}/index.md", "w") as f:
            f.write(new_index)
        return "Index updated"
    except PermissionError:
        print(f"Permission denied for update to {topic} index")
        return f"Permission denied for update to {topic} index"


def get_topics():
    return [f.name for f in Path("./wikis").iterdir() if f.is_dir()]


def add_content_file(topic: str, content: str, filename: str):
    try:
        with open(f"./wikis/{topic}/{filename}", "w") as f:
            f.write(content)
        return "File successfully written!"
    except PermissionError:
        print(f"Permission denied to create {filename}")
        return f"Permission denied to create {filename}"
