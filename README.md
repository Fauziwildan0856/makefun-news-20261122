# The World in One Page — Sunday, November 22, 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122) [![rank](https://make.fun/badge/news-image-20261122/Fauziwildan0856/makefun-news-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122) [![reward](https://make.fun/badge/news-image-20261122/Fauziwildan0856/makefun-news-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

An entry for the make.fun bounty **"Sum up 22 November's world news in
one image"**. The picture is a complete newspaper front page for
Sunday, November 22, 2026 as a single PNG, drawn in code during the
build; the program in this repository publishes that stored picture,
unchanged, as the entry image.

## What the page contains

- **35 stories**, every one of them happened or was first reported on
  Sunday, November 22, 2026, each attributed to its source.
- **3 illustrated lead panels**: COP31 talks slipping into overtime in
  Antalya with fossil fuels still out of the draft; Washington favouring
  an economic squeeze on Iran as the oil blockade reaches 130 days and
  $25bn of blocked crude; and 39 people missing after a factory fire in
  Serang, west of Jakarta.
- **9 illustrated mini panels**: the M6.9 Peru quake, Israel's president
  asking Eisenkot to form a government, the capture of FBI top-10 cartel
  chief 'Chapo Isidro', missiles on Kryvyi Rih, Bitcoin back above
  $60,000, Voyager 1 reaching one light-day from Earth, the Nigeria
  boat capsize toll at 24, the Ebola toll passing 5,700, and India's
  record 720/9 in New Zealand.
- A **continent stat bar** (Asia 4 · Middle East 5 · Europe 11 ·
  Africa 3 · Americas 8 · Global 4), a numbered **world map**
  ("Where it happened"), a dense **Also on Sunday** column with 18
  more stories, a 5-item one-line ticker, and a **Date Check** note
  that also lists the other days' stories deliberately left out.
- All pictures and the map are original and drawn in code.

## Run it

```sh
python3 main.py            # publishes the picture to /output/entry.png
```

The program uses only the Python 3 standard library. It finds the
stored picture in this repository (under whichever name the upload
gave it), checks it against a recorded SHA-256 fingerprint, and
copies it byte-for-byte to `entry.png` in the output directory
(`MAKEFUN_OUTPUT_DIR`, else `/output`). The picture is a 1024 x 1024
PNG (the maximum size the bounty allows), identical on every run.

## License

MIT — see `LICENSE`.
