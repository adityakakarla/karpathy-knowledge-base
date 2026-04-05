import os

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("topic")
def create(topic):
    try:
        os.mkdir(f"./wikis/{topic}")
        with open(f"./wikis/{topic}/index.md", "w") as f:
            f.write("\n")
    except FileExistsError:
        print(f"ERROR: Topic {topic} already exists")


@cli.command()
@click.argument("content")
def add(content):
    print(f"New content {content} added")


@cli.command()
@click.argument("question")
def ask(question):
    print(f"Question {question} asked.")


if __name__ == "__main__":
    cli()
