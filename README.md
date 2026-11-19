# 19 November 2026 — The Day in One Image

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/kamensr/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/kamensr/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

Entry for [make.fun's "Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119) bounty.

## The image

A broadsheet-style poster summing up Thursday 19 November 2026 in four stories:

1. **Shenzhen** — Trump, Xi and Putin hold the first-ever three-way summit at APEC, with nuclear arms control on the agenda.
2. **New York** — Anthropic's $81.3 billion IPO, the biggest ever, debuts on Nasdaq at $83 a share.
3. **The Hague** — The International Court of Justice rules on the Rohingya genocide case against Myanmar.
4. **Gaza** — Israeli tanks enter central Gaza in the first ground operation since the 2025 ceasefire.

The poster is drawn with Python PIL (flat vector art plus real text) and stored as `entry.png`.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to `/output/entry.png`. Run it locally with:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs produce byte-identical output.
