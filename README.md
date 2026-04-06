# karpathy-knowledge-base

A personal knowledge base CLI inspired by Karpathy's approach to note-taking. You create topics, add content to them, and ask questions — Grok does the heavy lifting.

## what it does

- **create** a topic to start a new wiki section
- **add** content that gets summarized and stored via Grok
- **ask** questions against your knowledge base

## how it works

Topics live as folders under `wikis/`, each with an `index.md` that tracks what you've added. When you run `add`, it calls Grok with tool use to print a summary. Simple, local, yours.
