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
    print(f"New content {content} added")
    output = query_agent(f"tell me about {content}. Use the print output tool")


@cli.command()
@click.argument("question")
def ask(question: str):
    print(f"Question {question} asked.")


if __name__ == "__main__":
    load_dotenv()
    cli()
