// Generate golden parity fixtures by running the JS `biblia-ruf` package over a fixed
// set of inputs and writing the results to tests/golden/. The Python parity tests then
// assert byte-for-byte equality against these files.
//
// Point BIBLIA_JS_DIST at the built ESM entry of a local biblia-ruf checkout, e.g.:
//   BIBLIA_JS_DIST=../biblia-ruf/dist/index.mjs node scripts/gen_golden.mjs
// Defaults to ../biblia-ruf/dist/index.mjs relative to this repo root.

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "..");
const distPath = resolve(
  root,
  process.env.BIBLIA_JS_DIST ?? "../biblia-ruf/dist/index.mjs",
);
const goldenDir = resolve(root, "tests", "golden");
mkdirSync(goldenDir, { recursive: true });

const lib = await import(pathToFileURL(distPath).href);

const PASSAGES = [
  "Jn 3:16",
  "Zsolt 139:23-24",
  "Zsolt 100",
  "Zsolt 139:3,23-24",
  "Róm 8:28",
  "1Móz 1:1-3",
  "Mt 5:3-12",
];

const SEARCHES = [
  { query: "szeretet", options: { limit: 10 } },
  { query: "Isten", options: { testament: "old", limit: 5 } },
  { query: "Isten", options: { testament: "new", limit: 5 } },
  { query: "kegyelem", options: { book: "Róm", limit: 20 } },
  { query: "SZERETET", options: { caseSensitive: true, limit: 5 } },
];

// A spread of dates across months/years to exercise the hash.
const DATES = [
  [2024, 1, 1],
  [2024, 2, 29],
  [2024, 7, 1],
  [2024, 12, 31],
  [2025, 6, 15],
  [2026, 1, 1],
  [2000, 10, 5],
  [1999, 3, 20],
];

const snakeSearch = (r) => ({
  book: r.book,
  book_name: r.bookName,
  chapter: r.chapter,
  verse: r.verse,
  text: r.text,
  reference: r.reference,
});

const passages = {};
for (const ref of PASSAGES) {
  passages[ref] = await lib.getBiblePassage(ref);
}

const searches = SEARCHES.map(({ query, options }) => ({
  query,
  options,
  results: lib.searchBible(query, options).map(snakeSearch),
}));

const daily = DATES.map(([y, m, d]) => ({
  date: [y, m, d],
  result: lib.getDailyVerse(new Date(y, m - 1, d)),
}));

const write = (name, data) =>
  writeFileSync(resolve(goldenDir, name), JSON.stringify(data, null, 2) + "\n");

write("passages.json", passages);
write("searches.json", searches);
write("daily.json", daily);

console.log(
  `Wrote golden fixtures: ${PASSAGES.length} passages, ${SEARCHES.length} searches, ${DATES.length} daily verses.`,
);
