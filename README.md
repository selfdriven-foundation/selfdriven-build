# selfdriven.build

**Be Constructive. Let's Build!** The workshop companion to [selfdriven.you](https://selfdriven.you): real projects to make, each with the idea behind it, a full build guide, and an installable `.skill` package.

Every page is a single self-contained HTML file in the selfdriven.you dark 4Cs system (Bricolage Grotesque, DM Sans, JetBrains Mono), led by Constructive mint `#00e5a0`.

## Layout

```
index.html                 Home: projects, how a build runs, why build, start now
cyberdeck/index.html       Project 01, the idea (was selfdriven.you/cyberdeck-the-idea)
cyberdeck/field-deck/      Field Deck guide   ← copied in by tools/migrate-cyberdeck.mjs
cyberdeck/pocket-deck/     Pocket Deck guide  ← copied in by tools/migrate-cyberdeck.mjs
assets/                    audio, pdf, skills, img ← copied in by the script
404.html  CNAME  .nojekyll  robots.txt  sitemap.xml
tools/migrate-cyberdeck.mjs
```

## Moving the cyberdeck over from selfdriven.you

The two build guides and their downloads still live in the selfdriven.you repo. One script moves them:

```bash
node tools/migrate-cyberdeck.mjs --you ../selfdriven.you            # dry run, prints every change
node tools/migrate-cyberdeck.mjs --you ../selfdriven.you --apply    # writes it
```

| Old (selfdriven.you)            | New (selfdriven.build)    |
|---------------------------------|---------------------------|
| `/cyberdeck-the-idea`           | `/cyberdeck/`             |
| `/cyberdeck-build-guide`        | `/cyberdeck/field-deck/`  |
| `/cyberdeck-pocket-build-guide` | `/cyberdeck/pocket-deck/` |

It copies the guides (links rewritten, nav wordmark switched to `.build`, canonical and og:url updated), copies every `/assets/` file the selfdriven.build pages reference, replaces the three old pages with redirect stubs that keep the `#anchor`, repoints the "Build a cyberdeck" footer link and any other links on selfdriven.you, and drops the old URLs from its `sitemap.xml`. Asset originals stay on selfdriven.you so existing download links keep working. Re-running is safe.

Then commit both repos. Optional: add a companion link to the selfdriven.you footer next to "Build a cyberdeck":

```html
<a href="https://selfdriven.build">Be Constructive → selfdriven.build</a>
```

## Going live on GitHub Pages

1. Settings → Pages → deploy from the default branch, root folder. Custom domain `selfdriven.build` (the `CNAME` file is included), then Enforce HTTPS.
2. DNS: apex `A` records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` as a `CNAME` to `<owner>.github.io`.

## Adding a project

1. Copy `cyberdeck/index.html` to `<project>/index.html`. Sections: hero → listen (optional) → four modes → no-workbench moves → builds (`#builders`) → closing.
2. On `index.html`, duplicate the `<article class="project">` block in `#projects`, set its serial (`PROJECT 02`), and keep the dashed "next bench space" slot last.
3. Build guides run Plan it (Curious) → Build it (Constructive) → Tend it (Caring) → Live with it (Chill) and ship a `.skill` package in `assets/skills/`.
4. Add the new URLs to `sitemap.xml`.

CC BY 4.0, selfdriven Foundation.
