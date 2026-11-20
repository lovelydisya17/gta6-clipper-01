// gta6-clipper-01 entry (Node 22, standard library only).
//
// The entry is the video itself: a public YouTube Short of an original,
// agent-rendered GTA 6 launch-week clip that hooks on Vice City and then
// pitches make.fun. This program only hands the house the video's address:
// it reads VIDEO.json from the repository root, checks it is a small JSON
// object whose url is a YouTube video address, and copies it byte for byte
// to the output directory, where the gate reads it. Nothing this program
// writes about the video is scored; the house reads the video's views
// itself through the YouTube Data API.
//
// The video behind VIDEO.json was rendered in the recorded agent session
// with scripts/render-clip.py + scripts/render-clip.sh (ffmpeg): three
// original stills drawn from scratch, a slow zoom, on-screen text, and an
// original synth pad. No Rockstar footage, audio, or artwork is used.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The gate's limits for VIDEO.json: a JSON object of at most 16384 bytes,
// naming a YouTube video whose id is 11 characters of [A-Za-z0-9_-].
const MAX_BYTES = 16384;
const VIDEO_URL = /^https:\/\/(www\.|m\.)?(youtube\.com\/(shorts\/|watch\?v=)|youtu\.be\/)[A-Za-z0-9_-]{11}([?&#].*)?$/;

function fail(message: string): never {
  console.error(`VIDEO.json rejected: ${message}`);
  process.exit(1);
}

const source = join(BOT_DIR, 'VIDEO.json');

const size = statSync(source).size;
if (size > MAX_BYTES) {
  fail(`is ${size} bytes, over the ${MAX_BYTES} byte cap`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(readFileSync(source, 'utf8'));
} catch (err) {
  fail(`is not valid JSON: ${(err as Error).message}`);
}

if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
  fail('must be a JSON object like {"url": "https://www.youtube.com/shorts/<id>"}');
}

const url = (parsed as Record<string, unknown>).url;
if (typeof url !== 'string' || !VIDEO_URL.test(url)) {
  // Warn, do not fail: until the clip is uploaded and VIDEO.json holds the
  // real video address, the starter placeholder is still in place, and the
  // gate (not this program) is what refuses it. Copying must still succeed
  // so the entry can be checked end to end before the upload.
  console.error('warning: VIDEO.json "url" is not a YouTube video address yet; the gate will refuse this entry until it is replaced with the uploaded video.');
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(source, join(OUTPUT_DIR, 'VIDEO.json'));
} catch (err) {
  console.error(`VIDEO.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
