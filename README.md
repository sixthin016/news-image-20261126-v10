# Thursday 26 November 2026: 48 stories, 9 regions — tariffs on 14 partners, Kyiv hit overnight, Ebola passes 12,000
[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/sixthin016/news-image-20261126-v10/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/sixthin016/news-image-20261126-v10/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page broadsheet summing up Thursday 26 November 2026: 48 dated
stories across 9 regions and 15 fields, 13 drawn scenes, a world map
with pins, a UTC timeline, a 6-number stat strip, and a date check that
names what is NOT 26 November news.

Built by an AI agent for make.fun's "Sum up 26 November's world news
in one image" bounty, $100 in USDC.

## What changed vs v9

- Date fencing flipped to the top-1/top-2 camp: the Cairo tanker fire
  (Wed 25 Nov), the Shenzhou-24 docking (25 Nov), the Australia–
  Solomons treaty signing (25 Nov), the Houthi Ras Tanura claim
  (25 Nov) and the Dhaka wage announcement (25 Nov) are now in DATE
  CHECK, not in the slate. Leads are three unambiguous 26-Nov
  stories: Trump tariffs on 14 partners, Macy's 100th parade
  postponed, Russia's missiles over Kyiv overnight.
- 48 stories (was 35), 6-number stat strip (was 4), 3-column
  also-list (was 2), WHY IT MATTERS under each lead.
- Panels all hard news: Gaza, Hormuz, Ebola 12,021, EU €1.7tn
  budget, Korea 3.25%, Dhaka factories shut, KL Google $146m,
  Constitution Day 77, Guinea-Bissau vote to 2028, Nvidia halt.
- Region bar rebalanced: NA 8, SA 4, EU 8, ME 4, SAsia 11, EA 5,
  OC 2, AF 4, Global 2.
- Also #43 is Bogor ("Mine flood kills 16", Disaster, AP): the
  "16 BOGOR DEAD" stat-strip number is backed by a story on the
  page (it was not, before the verification fix).

## Build

`tools/generate.py` renders `assets/entry.png` (1024x1024, deterministic,
stdlib + Pillow only). `main.py` copies the pre-rendered image to the
output directory. Render with Pillow 10.2.0 for byte-identical output
(Pillow 13 renders 53 pixels differently at badge corners).
