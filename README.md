# gta6-clipper-01: GTA 6 Is Finally Here, Vice City Is Calling

Entry for the make.fun bounty "Clip GTA 6 for the most YouTube views"
($500, top 20 share it, places go by the video's views at the deadline).
The video is the entry: this repository only hands the house its address
in `VIDEO.json`, and `main.ts` copies that file to the output directory.

## The clip

A 24 second vertical Short (1080x1920, 30 fps), rendered in the recorded
agent session with `scripts/render-clip.py` (original stills drawn from
scratch with Pillow) and `scripts/render-clip.sh` (ffmpeg: slow zoom,
concat, original synth pad). No Rockstar footage, audio, artwork, logos,
or screenshots are used anywhere.

Why this moment: launch week is when viewers search for first-look Vice
City moments, and a neon sunset over a palm-lined boulevard is the most
recognisable GTA 6 image. The clip evokes that image with original art
instead of copying game footage, so it can be published without lifting
anyone else's frames.

- 0-8s, hook: neon sunset, "GTA 6 IS HERE / VICE CITY IS CALLING".
- 8-16s, middle: night skyline, "13 YEARS OF WAITING. ONE CITY."
- 16-24s, pitch: dark card, "MAKE CLIPS LIKE THIS WITH AI / AND EARN
  MONEY ON MAKE.FUN / make.fun/bounty/gta6-clipper-01".

Title: `GTA 6 Is Finally Here, Vice City Is Calling`

## Upload (do this before submitting)

1. Render the clip: `bash scripts/render-clip.sh` (writes
   `gta6-clipper-01-short.mp4`).
2. Upload it to YouTube as a Public Short, published between the
   bounty's opening (2026-11-20 01:00 UTC) and its deadline
   (2026-11-23 01:00 UTC). Keep it public until the results are out.
3. Description, word for word, first line:

   `Made by my AI agent for a $500 bounty on make.fun, where you can earn money making clips with AI: https://make.fun/bounty/gta6-clipper-01`

   Then add one of this bounty's play codes (`makefun-` plus three
   words, from `GET /api/competitions/gta6-clipper-01/play-code`) in the
   video description, or in the channel description instead. Code 0 for
   this account in this bounty is `makefun-paper-swallow-robin` (any one
   of the four codes passes; a play code is not secret).
4. Copy the video's Share address into `VIDEO.json`:
   `{"url": "https://www.youtube.com/shorts/<id>"}`

Until step 4 is done, `VIDEO.json` still holds the starter placeholder
and the gate refuses the entry. Never buy views or use bots: bought or
botted views disqualify the entry.

## Run the program the way the grader does

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/VIDEO.json` is then byte for byte this directory's `VIDEO.json`.
`main.ts` also rejects a `VIDEO.json` that is not a small JSON object
naming a YouTube video address.

## Check

From the kit's directory:

    node cli/makefun.mjs check --kit . --repo <this repository>

Then submit the commit as the kit's `RULES.txt` (Enter) gives it. The
Solana keypair that signs the entry is held by the entrant, not the agent.
