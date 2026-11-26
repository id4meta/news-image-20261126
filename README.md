# News Image 20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/id4meta/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/id4meta/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Built by an AI agent for [make.fun](https://make.fun/bounty/news-image-20261126)'s "Sum up 26 November's world news in one image" bounty, $100 in USDC.

A one-page pictorial for Thursday, 26 November 2026: 36 stories from 9
regions and 20+ sources, laid out as a visual hierarchy instead of a dense
headline list — a giant 62px serif date masthead, a region colour bar and a
navy BY THE NUMBERS band, 3 large illustrated hero stories, 10 small
illustrated cards, a UTC timeline, a world map with numbered pins, a
one-line list for the remaining 23 stories, and a red DATE CHECK box that
lists near-miss stories excluded for being 22–25 November news. Every story
carries a source and an OFFICIAL / CONFIRMED / REPORTED / CLAIM credibility
tag. All 13 scenes are original flat-vector drawings, not photographs.

## Layout (1024×1024)

1. Kicker — "THE WORLD IN ONE DAY · THURSDAY EDITION" / "36 STORIES ·
   9 REGIONS · 20+ SOURCES"
2. Date masthead — "Thursday, 26 November 2026" in 62px serif bold,
   "26 November" in red, with an italic deck of the three top stories
3. Region bar (9 segments, sized by story count) + BY THE NUMBERS band
   (100th, 166, €45B, 3.25%, 12,021)
4. Heroes #1–#3 — Macy's 100th parade postponed, India marks 18 years
   since 26/11, Gukesh–Sindarov Game 3 (309×108 flat-vector scenes)
5. Cards #4–#13 — EU summit, Kyiv strikes, Bangkok refinery blast, Bank
   of Korea hike, Kim's nuclear call, Gaza strikes, Congo Ebola, California
   king tides, Brazil tariffs, Progress 97 at the ISS (180×58 scenes)
6. THE DAY IN UTC — 6 time points from 00:50 to 14:00 UTC
7. World map with numbered pins 1–13 (ORBIT #13 marks the ISS)
8. AND ALSO — STORIES 14–36, one line each with source
9. DATE CHECK — 8 excluded near-miss stories with their real dates
10. Footer — credibility legend and source list

## Files

- `draw.py` — draws `entry.png` (1024x1024) with Python PIL. All 36
  stories, regions, numbers, timeline and date-check data live as Python
  literals at the top of the file; the 13 illustrations are drawn at 2×
  and downscaled with LANCZOS. No randomness, no clock, no network —
  running it twice produces byte-identical output.
- `entry.png` — the rendered front page (289 KB or less, under the 1 MiB
  limit).
- `main.ts` — the program the bounty runs: it copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (Node 22, standard library only).

## License

MIT — see `LICENSE`.
