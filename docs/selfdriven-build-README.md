# selfdriven.build

**Be Constructive. Let's Build!** The workshop companion to [selfdriven.you](https://selfdriven.you): real projects to make, each with the idea behind it, the how-to, and a first small step.

The site is the Jekyll source in `docs/`, deployed to GitHub Pages by `docs/_workflows/jekyll-gh-pages.yml`. Pages use the selfdriven.you dark 4Cs system (Bricolage Grotesque, DM Sans, JetBrains Mono), led by Constructive mint `#00e5a0`, with the mint logo in every header.

## Projects

| # | Project | URL | Source |
|---|---------|-----|--------|
| 01 | Cyberdeck · the idea | `/cyberdeck-the-idea` | `docs/pages/cyberdeck-the-idea.html` |
| 01 | Field Deck build guide | `/cyberdeck-build-guide` | `docs/pages/cyberdeck-build-guide.html` |
| 01 | Pocket Deck build guide | `/cyberdeck-pocket-build-guide` | `docs/pages/cyberdeck-pocket-build-guide.html` |
| 02 | Build Your World | `/build-your-world` | `docs/pages/build-your-world.html` |
| 03 | Verify the Network | `/verify-the-network` | `docs/pages/verify-the-network.html` |
| 04 | Open Silicon | `/open-silicon` | `docs/pages/open-silicon.html` |

Project pages are self-contained HTML with `layout: null` and a `permalink` in their front matter.

Open Silicon is the build companion to [selfdriven.computer/open-silicon](https://www.selfdriven.computer/open-silicon): Layer 00 under the six-layer model. Three build paths (First Tile and Verilog Tile on Tiny Tapeout, Own Die on a wafer.space GF180MCU slot), a six-step flow, a verify track (OpenTitan, Tiny Tapeout chip maps, Caliptra) and start-now ticks stored under `sdb-open-silicon-v1`. Its podcast episode plays from `#listen`. Prices on the page and the home card were checked on 15 November 2026 (Tiny Tapeout individual €185 / full €385; wafer.space Run 3 quarter slot US$2,000 early bird / US$3,000 standard, announced but not open); re-check them when shuttles change.

## Podcast episodes

Pages with an episode carry a `#listen` audio card (play/pause, seek bar, time, download link) and its metadata:

- `<audio preload="metadata">` with `<source type="audio/mp4">` for `.m4a` files
- `og:audio`, `og:audio:secure_url` and `og:audio:type` in the head
- JSON-LD `PodcastEpisode` in the `selfdriven.you podcast` series, with an `AudioObject` (`encodingFormat: audio/mp4`)
- Media Session title, artist and artwork, set when playback starts

The home card for a project with an episode gets a `Podcast` tag and a `Listen` button to `#listen`.

## Layout

```
docs/
  index.html          Home: project index, the four project cards, how a build runs, why build, start now
  404.html            Not-found page
  pages/              Project pages (front matter sets the permalink)
  assets/img/         selfdriven-build-logo-round-mint.png (header + favicon) and the selfdriven.you logos
  assets/audio/       Cyberdeck podcast episode, ESP32 episode, Build_Your_Own_Microchip_in_a_Browser.m4a (Open Silicon)
  assets/pdf/         Cyberdeck Field Manual, Blueprint Manual
  assets/skills/      cyberdeck-field-deck.skill, cyberdeck-pocket-deck.skill
  sitemap.xml  robots.txt  CNAME  _config.yml  _layouts/  _well-known/  _workflows/
```

## Header

Every page header and the home footer use the mint logo followed by the word `build`, linking to `/`:

```html
<a href="/" class="brand" aria-label="selfdriven.build home"><img src="/assets/img/selfdriven-build-logo-round-mint.png" alt="" width="30" height="30"><span><em>build</em></span></a>
```

`build` is Constructive mint (`#00e5a0`). Project pages carry a small `<style id="sdb-brand">` block for the logo size and glow.

## Adding a project

1. Add `docs/pages/<slug>.html` with front matter `layout: null`, `title`, `permalink: /<slug>`, using the header above and a `selfdriven.build · all projects` link in the footer.
2. On `docs/index.html`, add a row to the `.pindex` strip and a `<article class="project">` card in `#projects` (alternate `project flip` for art-left). Number it, and move the dashed "next bench space" slot to the next number. The strip is four columns on desktop; a fifth project needs the grid rethought.
3. Add the URL to `docs/sitemap.xml`.

## Moving pages off selfdriven.you

The cyberdeck pages and Verify the Network still exist on selfdriven.you at the same paths. Once selfdriven.build is live, replace each one in `selfdriven-you/docs/pages/` with a redirect that keeps its permalink:

```html
---
layout: null
permalink: /cyberdeck-build-guide
---
<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<link rel="canonical" href="https://selfdriven.build/cyberdeck-build-guide">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url=https://selfdriven.build/cyberdeck-build-guide">
<script>location.replace('https://selfdriven.build/cyberdeck-build-guide' + location.hash)</script>
</head><body><a href="https://selfdriven.build/cyberdeck-build-guide">This page moved to selfdriven.build</a></body></html>
```

Then point the "Build a cyberdeck" link in the selfdriven.you footer at `https://selfdriven.build/cyberdeck-the-idea`.

CC BY 4.0, selfdriven Foundation.
