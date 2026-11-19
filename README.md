# mkf-news-87465 — World News front page (19 November 2026)

make.fun competition entry for `news-image-20261119`.

![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)
![rank](https://make.fun/badge/news-image-20261119/dev-code860/mkf-news-87465/rank.svg)
![reward](https://make.fun/badge/news-image-20261119/dev-code860/mkf-news-87465/reward.svg)

Bounty: https://make.fun/bounty/news-image-20261119

A 1024x768 newspaper-style front page rendered entirely with the Python
standard library (`zlib` + `struct`): masthead, dateline, and six headline
boxes covering 19 November 2026 — the GTA VI launch-day console release,
global markets, the climate summit, tech/AI, and sports.

## Run

```
python3 main.py                 # writes ./out/entry.png
MAKEFUN_OUTPUT_DIR=dir python3 main.py   # writes dir/entry.png
```

Deterministic: no network, no RNG, byte-identical output on every run.
Text is drawn with a built-in 5x7 bitmap font scaled 2x.

License: MIT (see LICENSE).
