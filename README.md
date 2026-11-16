# zhanqizhang66.github.io

Victoria Zhang's personal site: https://zhanqizhang66.github.io/

A static site with a top-view forest in the margins and three birds (Ashe, Pearl and Kiwi) that hop, fly, sleep at night, and speak as small n-gram language models when clicked.

## How it is built

The site is plain static files served by GitHub Pages. `.nojekyll` turns Jekyll off, so nothing is built on GitHub; the pages in the repo are what is served.

`site-src/build.py` generates every page into the repo root. It needs only Python 3, no packages.

```
python3 site-src/build.py
```

Run it from the repo root after any content change, then commit and push to `master`.

## Where things live

| What | Where to edit |
| --- | --- |
| Blog posts and essays | `_posts/*.md` (one file per post) |
| Research entries | `publications.md` |
| Home page title, news, selected work, experience | `site-src/build.py` |
| Home page About text, forest and bird drawing code | `site-src/home-source.html` |
| Google, Meta and NEST research entries | `site-src/build.py`, `site-src/nest-source.html` |
| Styles added on top of the home page | `EXTRA_CSS` in `site-src/build.py` |
| Images, PDFs | `assets/`, `files/` |
| Link-preview card | `assets/img/og-card.png` |

Generated output, do not edit by hand: `index.html`, `404.html`, `blog/`, `publications/`, `art/`, the dated post folders (`2025-01-01-River/` and so on), and `assets/site/`.

## Adding a post

1. Add `_posts/YYYY-MM-DD-Title.md` with the usual front matter (title, tags, cover image).
2. Run `python3 site-src/build.py`.
3. Commit and push.

The post URL is `/YYYY-MM-DD-Title/`, the same as the old Jekyll permalinks.

## Previewing locally

```
python3 -m http.server 8766
```

Then open http://localhost:8766/. Add `?hour=22` to any page to preview night mode, or `?hour=12` for day.

## The birds

- Ashe: gray cockatiel, orange cheek patches, white wing bars. Speaks as a 4-gram model.
- Pearl: white pearl cockatiel, pale-yellow pearling, no cheek patches. Speaks as a trigram model.
- Kiwi: green parakeet, smaller, with dark barring on the head and wings. Speaks as a bigram model.

Their colours, sizes and markings are in `KIND` and `drawBird` in `site-src/home-source.html`. A bird's name shows only while it is clicked.

## Notes

- The theme follows San Diego time (dark from 7 pm to 6 am) and can be switched with the toggle in the header.
- The old Jekyll theme files (`_layouts/`, `_includes/`, `_config.yml`, `blog.md`) are still in the repo but unused. They came from [Beautiful Jekyll](https://beautifuljekyll.com/) by Dean Attali (MIT licence).
