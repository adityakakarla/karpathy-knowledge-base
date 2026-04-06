from pathlib import Path


def read_index(topic):
    try:
        with open(f"./wikis/{topic}/index.md", "r") as f:
            index = f.read()
            return index
    except FileNotFoundError:
        print(f"Index file for {topic} not found")
        return "No index file found"
    except PermissionError:
        print(f"Permission denied for {topic} index")


def create_or_update_index(topic, new_index):
    try:
        with open(f"./wikis/{topic}/index.md", "w") as f:
            f.write(new_index)
    except PermissionError:
        print(f"Permission denied for {topic} index")


def get_topics():
    return [f.name for f in Path("./wikis").iterdir() if f.is_dir()]
