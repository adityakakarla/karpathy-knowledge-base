import os

import click
from dotenv import load_dotenv

from llm import query_agent


@click.group()
def cli():
    pass


@cli.command()
@click.argument("topic")
def create(topic: str):
    try:
        os.mkdir(f"./wikis/{topic}")
        with open(f"./wikis/{topic}/index.md", "w") as f:
            f.write("\n")
    except FileExistsError:
        print(f"ERROR: Topic {topic} already exists")


@cli.command()
@click.argument("content")
def add(content: str):
    query_agent(
        f"Add content about {content}. Use the tools at your disposal. You must use the print output tool if you want to provide updates to the user."
    )


@cli.command()
@click.argument("question")
def ask(question: str):
    query_agent(question)


if __name__ == "__main__":
    load_dotenv()
    cli()
