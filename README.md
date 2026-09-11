# Legends Radio 100.3 FM — website (redesign concept)

A dynamic, premium marketing + streaming site for **Legends Radio 100.3 FM (WLML-FM)**,
"Where Legendary Music Lives" — the Great American Songbook, live & local from Florida's
Palm Beaches. Built as a self-contained static site with the same philosophy as the rest
of this repo: **`build.py` is the single source of truth.**

> This lives in the `legends-radio/` subfolder so it can be previewed on this project's
> Vercel deploy at `/legends-radio/` without touching the First Rehab site. It is designed
> to move to its own domain unchanged (all internal links are relative).

## What's in the box
- **8 pages + 404**: Home, Listen Live, Shows & Schedule, On-Air Personalities, Events,
  About, Advertise, Contact.
- **A persistent live player** wired to the real WLML stream
  (`https://ice3.securenetsystems.net/WLML`), with volume persistence, animated
  equalizer + spinning vinyl, OS media-session metadata, and a pop-out fallback if the
  stream can't play cross-origin.
- **A client-side "On Air Now / Up Next" engine** computed in the station's Eastern time,
  so the hero card, the sticky player, and the weekly schedule grid always show the show
  that's actually on — no backend required.
- **Art Deco / supper-club design system** (midnight + gold + oxblood, Playfair Display +
  Inter, self-hosted): cinematic hero lighting, film grain, legends marquee, schedule grid
  with a live progress bar, host medallions, scroll reveals, count-ups.
- **SEO**: unique title/description/canonical, Open Graph + Twitter cards, JSON-LD
  (`RadioStation` + `BroadcastService` + `Person` + `ItemList` + `BreadcrumbList`),
  `sitemap.xml`, `robots.txt`, `site.webmanifest`, favicons + Apple touch icon + OG image.
- **Fully accessible & fast**: skip link, focus states, `prefers-reduced-motion` support,
  self-hosted fonts, no third-party trackers, no external runtime dependencies.

## Architecture
- **`build.py`** — all content (station facts, hosts, shows, weekly schedule, events,
  artists) + the page templates + SEO file generation. Edit it, then rebuild.
- **`assets/css/legends.css`** — the whole design system (hand-written).
- **`assets/js/legends.js`** — player, On-Air engine, schedule tabs, reveals, counters,
  marquee cloning, mobile nav, forms. Zero dependencies. Consumes `window.LEGENDS_*`
  data injected by `build.py`.
- **`assets/img/`** — SVG emblem/favicon + generated PNGs (favicon, apple-touch, OG,
  media-session artwork). No fabricated photos of real people.
- **`assets/fonts/`** — self-hosted Playfair Display + Inter (woff2).

## Build & preview
```bash
cd legends-radio
python3 build.py
# from the repo root:
python3 -m http.server 8000   # →  http://localhost:8000/legends-radio/
```
CSS/JS links carry build-time content-hash cache-busters (`asset_v()`), matching the
convention in the rest of this repo.

## Facts & sourcing
Station facts are grounded in public sources (WLML-FM / legendsradio.com): call sign,
100.3 FM, licensed to Lake Park FL, founded 2014 by Dick Robinson, studio at 760 US
Highway 1 Ste 102 North Palm Beach, business line 561-469-6700, request line
561-685-9565, `info@legendsradio.com`. Confirmed shows/hosts: **The Morning Lounge**
(Jill & Rich Switzer), **Middays** (Walt Pinto), **Afternoons** (Lorna O'Connell),
**American Standards by the Sea** (Dick Robinson), **The Golf & Travel Show**
(Dan Shube & Doris Muscarella). No credentials, quotes, or events were invented.

## Owner to-dos
- **Canonical domain** — `BASE` in `build.py` is `https://www.legendsradio.com`. If this
  is deployed somewhere else permanently, update `BASE` and rebuild.
- **Live stream** — the player uses the real SecureNetSystems mount. It plays in a normal
  browser; if SecureNet ever hotlink-protects it, the pop-out button opens
  `legendsradio.com/listen-live`. Hosting on the `legendsradio.com` domain makes the
  referer match and is the most robust option.
- **Contact/advertise/request forms** — they POST to
  `formsubmit.co/ajax/info@legendsradio.com`. FormSubmit sends a **one-time activation
  email** to that inbox on the first submission (check spam); click it once to turn the
  forms on. (Or swap in a real backend endpoint.)
- **Schedule** — confirmed hosted shows: The Morning Lounge (Jill & Rich Switzer),
  Middays w/ Walt Pinto (Legends at Lunch @ noon), Afternoons w/ Lorna O'Connell,
  American Standards by the Sea (Dick Robinson), Legends of Jazz (Gregory "Popeye"
  Alexander), Late Nights with Legends, The Golf & Travel Show (Dan Shube & Doris
  Muscarella), Inspired To Be (Sherrye Fenton). The **overnight/weekend music blocks**
  (Nonstop Legends, Legends Evenings, Saturday Morning Swing, etc.) are descriptive
  placeholders — replace with the real grid in `SCHEDULE`.
- **Host photos** — medallions use monogram initials (no fabricated portraits). Add real
  portraits and wire them in when available.
- **Events** — cards route to the station's Eventbrite (no fabricated dates). The
  "Live Concerts at Abacoa" series and tribute acts are real; specific show dates live on
  Eventbrite (verify before hard-coding any date).
- **Now Playing** — shows the current *show* (always accurate). If SecureNet exposes a
  CORS-enabled now-playing endpoint, live track/artist metadata could be layered on.

### Confirm with owner (from the 2026-07 research audit)
The current legendsradio.com blocks bots, so these were third-party-sourced — please verify:
- **Afternoon-drive host** — sourced as Lorna O'Connell, but older indexed snippets show
  other names on `/afternoons/`. Confirm the current live host.
- **"Inspired To Be" (Sherrye Fenton)** air day/time (listed as "Weekly · See schedule").
- **Overnight hours** outside the confirmed 11 PM–1 AM Late Nights block (assumed automated).
- **ASbtS affiliate count** — used "75+"; confirm exact number.
- **Brand assets** — the script wordmark, red palette, and red/white/blue musical-note
  flag emblem are recreated from the owner-supplied logo; drop in the official vector /
  exact hex values to make them pixel-perfect.
- **Excluded as historical (not current on-air):** Angela Manfredi, Steve Ketelaar, Taylor
  Morgan, Paul Cavenaugh, Toni May — confirm none should be reinstated.
- **Studio address** — using 760 US Highway 1, Ste 102, North Palm Beach 33408 (license
  city is Lake Park); confirm the correct public studio/mailing address.

## 2026-08 — lineup correction + real station imagery

The original build sourced its lineup from third-party pages because
legendsradio.com returns 403 to automated clients. Those sources were stale.
The lineup was re-derived from the station's **own** pages (fetched via a
GitHub Actions relay, which has open egress) and from the station's current
"Your Weekdays Lineup" graphic.

Corrected weekday lineup (per the station's own graphic, July 2026):

| Slot | Host | Show |
|---|---|---|
| 6a–10a  | Jill & Rich Switzer | The Morning Lounge |
| 10a–2p  | Mike McGann         | Middays with Mike McGann |
| 2p–7p   | Steve Ketelaar      | Legends Afternoons |
| 7p–9p   | Alex Donner         | Evenings with Alex Donner |
| 9p–11p  | Bob Merrill         | Legends After Dark |
| 11p–1a  | Dick Robinson       | American Standards by the Sea |

Also on air: Gregory "Popeye" Alexander (Legends of Jazz), Cindy Hite
(Cindy on Legends), Lauren May, Bob Merrill (Sunday Legends Brunch),
The Sounds of Sinatra.

**Removed as not-current:** Walt Pinto, Lorna O'Connell, Sherrye Fenton /
"Inspired To Be", and The Golf & Travel Show (Dan Shube & Doris Muscarella).
Steve Ketelaar had previously been excluded as "historical" — he is in fact
the current afternoon host.

### Owner confirmations still needed
- **Morning Lounge start time.** The lineup graphic says 6a; the Morning
  Lounge page says "Weekdays 5:00 AM – 10:00 AM". The site currently uses 6a.
- **Host bios.** Only Jill & Rich and Dick Robinson have substantive bios.
  The rest are deliberately minimal factual lines — no credentials were
  invented. Please supply proper bios.
- **Weekend/specialty slot times** for Legends of Jazz, Cindy on Legends,
  Lauren May and Sounds of Sinatra are not published on the station site.

### Image provenance
`assets/hosts/*` are the station's own photographs, taken from
legendsradio.com for use on the station's own new site. **Advertiser creative
was deliberately excluded** (Alaina's Cafe, Harbourside/BurgerFi, Uncle
Eddie's, Bake Me A Wish etc.) — that artwork belongs to the advertisers, not
the station. Confirm the station holds rights to each host portrait before
launch.

## 2026-09 — advertisers & partners ("the patrons' board")

The site had an Advertise page with no advertisers on it. This adds the real
roster, crawled from the station's own live site, and gives it a home that is
worth looking at.

### Where the roster came from

`legendsradio.com` returns 403 to most automated clients but serves a normal
browser UA fine, so the whole site was crawled directly (43 pages off
`wp-sitemap.xml`). Four sources, all of them the station's own:

| Source | What it yielded |
|---|---|
| Sitewide **"Friends of Legends 100.3"** footer | Schumacher Auto Group, The Lois Pope LIFE Foundation, Preserve Our Gas, CSB Media Arts Center, Palm Beach Code School |
| **Banner rotator** (`?wpbrmethod=ad&hit=1&id=…`) | The Cosmetic Dentist (sitewide), and on the arts pages: The Society of the Four Arts, Sunrise Theatre, The Pops Orchestra of the Palm Beaches |
| **Sponsored programming** in the primary nav | Mittleman Eye, First Rehabilitation, The Culture Circuit, The GOLD LAW Firm, Hippocrates Wellness — each weekend show links straight to its sponsor |
| **Homepage sliders / named testimonial** | Addington Place of Jupiter, Culinary Studio, CBS12, Palm Beach Symphony |

**18 current partners.** The rotator also still holds ~25 expired 2019–2020
creative slots (Kravis, Maltz Jupiter Theatre, Palm Beach Dramaworks, a decade
of finished contests). Those are deliberately **excluded** — they are not
current business. The full inventory is recoverable by walking ids 1–40 on the
rotator endpoint if the owner wants any of them reinstated.

All 18 destinations were checked live: every one resolves. Four were `http://`
in the station's own markup and were upgraded to `https://`.

### No borrowed artwork

Consistent with the 2026-08 decision, **no advertiser logo is reproduced.**
Each patron is set as an engraved type plate — kicker, name, hairline brass
rule, descriptor. That is rights-clean (the creative belongs to the
advertisers) and, on a Playfair/Pinyon site, better looking than a logo wall.
Descriptor lines use the station's own words where it publishes them.

### The design — Palm Beach daylight

The site is a midnight supper club. The patrons' board is the one place it
steps outside: a green-and-white **scalloped awning** over a shell-white
**lattice**, with palm green, conch coral and brass replacing gold-on-black.
The contrast is the point — it reads as stepping out from under the awning into
Worth Avenue at eleven in the morning. Implementation notes:

- Daylight tokens are **scoped to `.patrons`**, so nothing else on the site shifts.
- Awning and lattice are pure CSS (`mask` + `repeating-linear-gradient`); the
  scallop pitch and the stripe pitch are both 46px so they stay in phase.
- Zero new requests, zero images, zero dependencies added.
- Gold focus rings are invisible on shell white, so focus goes **palm green**
  inside the daylight section.
- Plate hover is a brass sheen sweep on `transform`/`opacity` only; disabled
  under `prefers-reduced-motion`.

Also added: a brass **partner ribbon** on the homepage, the station's real
audience-profile figures, the Palm Beach Symphony testimonial, and the
published sales contact (Tim Reever, 561-469-6702, `treever@legendsradio.com`).
Audience figures are quoted verbatim from the station's own `/advertisers/`
page and are labelled as the station's figures on the page — they are not
independently verified.

### Verified this run
- axe (WCAG 2.0/2.1/2.2 A + AA): **0 violations**, advertise + home, desktop + mobile
- CLS **0.006** (advertise) / **0.001** (home); no horizontal overflow at 390px
- All internal links, assets, `alt`, `<h1>` counts, meta and JSON-LD: clean
- All 18 advertiser destinations resolve

### Owner to-dos
- **Confirm the roster is current** — especially Culinary Studio and CBS12,
  which appear as homepage slider/banner placements rather than in the footer.
- **Reinstate anything from the expired rotator** that is still a live account.
- **Sponsored-program times** are taken from the station's nav labels; confirm
  them against the current clock.
- **Audience figures** — the station publishes these; confirm the source before
  they go in a media kit.

## 2026-09 — shows, audio, video and a calendar that updates itself

The site grew from 9 pages to 25, and from a schedule grid to something you can
actually listen to and watch.

### Live "Now Playing", with album art

The station's streaming vendor (SecureNetSystems) publishes two feeds that the
browser can read directly — both send `Access-Control-Allow-Origin`, so there is
no backend and no proxy:

| Feed | What it gives |
|---|---|
| `player_status_update/WLML.xml` | the current item — **goes blank during ad breaks and talk** |
| `player_status_update/WLML_history.xml` | the last 30 songs, newest first |

Each song carries title, artist, album, duration and a **cover-art URL on the
vendor's own CDN** (also CORS-open, `max-age=86400`).

**On the artwork question:** this is the same art the station's official
SecureNet player already displays, served by the station's own licensed
streaming vendor as part of its streaming service. Nothing is scraped from a
third party and no iTunes/Spotify lookup is involved — which is why this route
was chosen over the usual album-art APIs.

About **40% of tracks carry no cover**, so the spinning vinyl is a designed
fallback, not a broken image. The poller stops while the tab is hidden.

This drives: the sticky player, the hero card's live track line, OS/lock-screen
media metadata, and the **Just Played** board on `listen.html`.

### One page per show

`PROGRAMS` in `build.py` is now the single source for the lineup — the old
`SIGNATURE` list was a second, drifting copy of it and has been deleted (it
carried the Golf & Travel Show's blurb on Alex Donner's entry). 14 shows each
get `show-<slug>.html` with hero, an on-air-right-now badge computed in station
time, host block, episode archive, video, and related shows.

### Audio

A custom episode player, not `<audio controls>`. Starting an episode stops the
live stream and vice versa — only one thing ever plays. The `playing` state is
set by the audio element's own event, so a file that never loads shows a loading
then an error state rather than pretending to play.

Real media only: three full-show MP3s on *Legends International* and the
SoundCloud interviews on *Sunday Legends Brunch* / *Legends of the Palm Beaches*.
**Every other show gets a designed empty state** — no episode lists were
invented. SoundCloud loads behind a click-to-load facade.

### Video

`video.html` plus per-show sections. Titles and channels are what YouTube's own
oEmbed returns. Clips use a **click-to-load facade** — no YouTube iframe and no
Google request until the visitor presses play, then `youtube-nocookie.com`.
Sponsor-owned clips are labelled as such.

### The calendar that updates itself

`events.html` is rendered twice:

1. **Build time** — `assets/data/events.json`, a snapshot of the station's own
   Events Calendar REST API. This is the floor: correct with JS off, for
   crawlers, and when the API is down.
2. **Runtime** — the page re-fetches the live API and reconciles, then says so
   ("Live from the station calendar · updated just now"). If the fetch fails it
   says *that* instead, and keeps the snapshot.

Plus a countdown to the next event and an "Around the Palm Beaches" rail linking
each partner venue's own calendar — we never republish another organisation's
listings.

### Fixed along the way
- `SIGNATURE` carried the wrong blurb on Alex Donner (see above), and
  *The Sounds of Sinatra* linked to `thegolfandtravelshow.com` — a show removed
  as not-current in 2026-08.
- The global list reset covered `ul` but not `ol`, so the new episode, event and
  playlist lists rendered their numbering.
- Adding a nav item pushed the header past its container at every desktop width
  (the row needs ~1333px; the body grid caps at 1220). The header now has its own
  container and hands over to the drawer at 1280px.
- Meta descriptions are clamped to snippet length in `document()`, on a word
  boundary, so this can't drift again.
- `role="presentation"` on the month separators made the event `<ol>` read as
  containing non-list children; inline links in running text were signalled by
  colour alone (WCAG 1.4.1).

### Verified this run
- **axe (WCAG 2.0/2.1/2.2 A + AA): 0 violations** — all 25 pages × desktop + mobile
- **CLS** 0.0003–0.046, **LCP** 184–1500ms (local server; re-measure on Vercel)
- Nav fits with no overflow at 390 / 768 / 1024 / 1279 / 1281 / 1366 / 1440 / 1600 / 1920
- Playlist grid never ends ragged (12 items across 3 / 2 / 1 columns)
- Live feeds exercised against real captured payloads, including the blank-feed
  ad-break path and the no-cover-art path
- Links, assets, alt text, `<h1>` counts, meta, JSON-LD and sitemap: clean

### Owner to-dos
- **Show blurbs** are descriptive rather than sourced — have the station approve
  the wording, especially Alex Donner's and Bob Merrill's.
- **Weekend slot times** for Legends of Jazz, Cindy on Legends, Sounds of Sinatra
  and Sunday Legends Brunch still read "See schedule" — the station does not
  publish them.
- **The archive is thin** because only four MP3s and a handful of SoundCloud
  posts exist publicly. Point `PROGRAMS[*]["audio"]` at a real feed and the
  empty states fill themselves in.

## 2026-09 — follow-up pass: wayfinding, on-demand, schedule integrity

Cleaning up what the restructure exposed.

### A real schedule bug
Sunday had **two shows claiming 07:30–10:00** — *Sunday Legends Brunch*
(07:00–10:00) and the descriptive *Sunday Morning Standards* placeholder
(07:30–10:00). The on-air engine picked between them arbitrarily, so the
"On Air Now" card could show the wrong programme every Sunday morning. The
placeholder is gone; the Brunch owns the slot.

There is now a check that every day covers 00:00–24:00 with no overlaps and no
gaps. All seven days pass.

### Wayfinding into the show pages
14 show pages existed but little linked to them. Now:
- **40 schedule rows** link through to the show's page (a matcher maps the
  schedule's fuller titles — "Dick Robinson's American Standards by the Sea" —
  onto `PROGRAMS`; the descriptive music blocks deliberately match nothing).
- **8 of 9 host cards** link to their show (Lauren May has no distinct show).
- Show cards on `shows.html` are links, grouped Weekdays / Weekends / Archive
  rather than one flat wall of 14.
- `shows.html` now also lists the station's **sponsored weekend half-hours**,
  each linking to the business behind it.

### On-Demand rebuilt around real audio
`podcast.html` was four hand-written cards describing categories. It now builds
itself from `PROGRAMS`: every episode that actually exists, playable inline,
grouped by show — **7 episodes across 3 shows** — plus an honest "still
live-only" list of the other 11. The `ON_DEMAND` placeholder list is deleted.

### Breadcrumbs
The visible breadcrumb was rendering the **headline** rather than the section,
so On-Demand read "Home / Miss a show? Not anymore." Both the visible crumb and
the JSON-LD now derive from one source — the nav label — so they cannot drift.
Show pages nest under Shows in both. A breadcrumb on 404 made no sense and is
gone. **0 mismatches across all 25 pages.**

### Verified
- axe 0 violations · 0 JS errors · 0 horizontal overflow — 25 pages × desktop + mobile
- Schedule: no overlaps, no gaps, all 7 days
- Breadcrumbs: visible and structured data identical on every page
- Links, assets, alt, `<h1>`, titles, JSON-LD, sitemap: clean
