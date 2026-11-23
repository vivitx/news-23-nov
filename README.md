# Monday 23 November 2026 in one picture

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/vivitx/news-23-nov/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/vivitx/news-23-nov/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A single 1024×1024 image summing up Monday 23 November 2026's world news,
in the style of a dense newspaper front page — all flat vector-style graphics,
no AI photos.

## The three leads

1. **COP31 collapses without a deal (Antalya)** — the longest summit ever ends
   in failure; 194 delegations, no fossil-fuel mention, first collapse since
   Copenhagen 2009.
2. **Tankers ablaze in the Strait of Hormuz** — IRGC says two supertankers hit
   naval mines; 22 shipping attacks in November.
3. **Kyiv mourns as rescue ends in Dymer** — 11 killed, 14 missing; a 79-year-old
   woman and Davyd, 7, pulled alive.

Plus ten medium stories (Democrats take the House with 258 seats, the AI rout,
Vanuatu M6.5, Nepal–Modi, FIFA 2035, Liverpool 4–0 United, NATO on Poland,
Geneva killer-robot rules…), a flat world map, 32 briefs, a UTC timeline, and a
DATE CHECK box listing the previous-day stories deliberately left out.

## How it works

`main.py` (Python 3.13, stdlib only, no network) validates `entry.png`
(a real PNG, 1024×1024, under 1 MiB) and copies it to `MAKEFUN_OUTPUT_DIR`
(or `/output`). The image was drawn in-session by `draw.py` (PIL) and is
committed as `entry.png`, so both runs write the same bytes — deterministic.

## Entry

- Image: `entry.png`, 1024×1024, 245,142 bytes, md5 `5b1da2a4c0579279dd86ef189fa367a4`
  (verified: two runs of `main.py` produce byte-identical output)
- Build script: `draw.py`
- Content paper trail: `content-2026-11-23.md` (in the work directory)
