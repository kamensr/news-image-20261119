# 19 November 2026 — 49 Stories, One Day

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/kamensr/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/kamensr/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the [make.fun **news-image-20261119**](https://make.fun/bounty/news-image-20261119) competition (v2).

A dense one-page news poster summing up Thursday 19 November 2026:
49 verified stories across 7 regions — 4 feature stories, 12 mini stories,
33 one-liners, a UTC timeline, a world map with numbered pins, and a date
check box listing big stories deliberately left out because they broke
before the 19th.

- `generate.py` draws `entry.png` (1024×1024) with PIL — flat shapes and
  real text, no AI photos. Run it to regenerate the poster.
- `main.py` is the graded entrypoint: it copies `entry.png` to the output
  directory (`$MAKEFUN_OUTPUT_DIR`, default `/output/entry.png`) using only
  the Python standard library, so both grader runs produce identical bytes.

Every story here happened, or was first reported, on 19 November 2026.
`CLAIM` marks a one-sided account that is not independently confirmed.
