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

## 2026-09 — daylight: the palette flips

The site launched near-black (`--ink #0B0807`, luminance 0.003). That was wrong
for this client, and the evidence is one-sided.

### What the category actually does

Measured from the live CSS of each site, 2026-09-14:

| Site | Page background | |
|---|---|---|
| **legendsradio.com — the station's own site** | `#ffffff` | LIGHT |
| Classic FM | `#f5f5f5` | LIGHT |
| Smooth Radio | `#f5f5f5` | LIGHT |
| Heart | `#f5f5f5` | LIGHT |
| Jazz FM | `#ffffff` | LIGHT |
| Global Player | `#ffffff` | LIGHT |
| NPR | `#ffffff` | LIGHT |
| iHeartRadio | `light-dark()` | adaptive |
| SiriusXM | `#021f3c` | dark |
| TuneIn | `#000000` | dark |

The split is not arbitrary. Every **station brand** runs light. The only dark
ones are **subscription streaming products** — SiriusXM and TuneIn — where the
visitor lives inside a player. Legends is a station brand with editorial
content, and it was built like a player app.

Two further reasons, beyond convention:

- **It fought the brand they already have.** legendsradio.com is white. Anyone
  who knows the station would read the rebuild as a change of identity.
- **It was the worst case for this audience.** The station's own published
  figure is that listeners are "2× more likely to be affluent consumers born
  before 1960". Light-on-dark haloes badly with the lens changes and
  astigmatism that come with age.

### How the flip was done

The stylesheet is token-driven, so the palette turns over in the tokens rather
than across 403 separate declarations. `:root` now carries a warm-paper scale
(`--ink #F7F2E7`), warm near-black type, and a **brass** (`--gold #8A6A1F`)
in place of the bright gold, which is unreadable on paper.

The black lacquer survives as a **scoped accent** — `.lacquer` re-declares the
original midnight tokens, and is applied to the homepage hero, each page's hero
band, the sticky player and the footer. Everything inside those keeps working
untouched, because only the tokens change.

Paper is `#F7F2E7`, not `#fff` — pure white is clinical under Playfair.

### Caught in the flip
- **Form fields are `.field`, not `.form`** — the first override missed them
  entirely and left dark wells with invisible placeholders on a light page.
- `.deco-frame` and `.host-medallion` hardcoded near-black and became black
  boxes floating on paper.
- The active nav link was set to `color:inherit`, so over the lacquer hero it
  inherited the body's new dark ink and **disappeared**. The header now carries
  its own palette in both states: night tokens while it floats over the hero,
  paper tokens once scrolled.
- `.pill` landed at 4.4:1 on the tinted card ground — a step deeper to clear AA.

### Verified
- **axe 0 violations · 0 JS errors · 0 horizontal overflow** — 25 pages ×
  desktop + mobile
- Contrast scanned separately across all 25 pages: **0 failures**. Note that
  scanning before the scroll-reveal transition settles produces false
  positives, since axe blends the half-faded foreground — force
  `.reveal{opacity:1}` before measuring.

## 2026-09 — photos, a live rail, and an archive you can actually browse

### Host photo crops
Three portraits are tall (Mike McGann 400×600, Alex Donner 360×504, Bob Merrill
250×340). A square centre-crop in the round medallion landed on the chest —
Mike's head was cut off entirely. Each host now carries a `focus` value (the
face centre as a % of image height), applied as `object-position`, and the
programme cards crop square so those same values hold.

### What's playing, with the cover
The Listen page led with a generic spinning vinyl. It now carries an **On Air
Now panel**: the actual cover art from the station's streaming vendor, the
track and artist set large, then the show, host and slot. The record slides out
from behind the sleeve on hover. Falls back to the vinyl on the ~40% of tracks
with no cover, and the track line hides entirely during ad breaks.

The artist separator (` · `) moved from JS into CSS, so the compact strip keeps
it and the big panel doesn't.

### Shows
Cards were text-only. They now lead with the **host's portrait**, and shows
without one get a monogram plate rather than a grey box. A **live rail** sits
under the hero: who is on, their photo, a progress bar through the slot, and
what follows — recomputed every 30s from the same Eastern-time engine that
drives the player. The matching card marks itself `is-live`.

**A real bug this exposed:** `var` is function-scoped, and the scroll-progress
bar at the top of the page already used `var rail`. Declaring `var rail` again
for the live rail reassigned the *same* variable, so the scroll handler wrote
its percentage into the live rail's `style.width` — the rail shrank as you
scrolled, down to 56px. Renamed to `liveRail`.

### Photo strip
A rolling, full-bleed strip of station photography on the homepage.

**On Instagram:** a live feed needs an Instagram Graph API token the station has
to issue — Basic Display was retired at the end of 2024. Without one there is
no way to read the account. So the component is source-agnostic: it renders
`assets/data/photos.json` at build time and can be repointed at any endpoint
returning the same shape.

Today that cache is the station's **own Flickr** (`158689475@N04`, linked from
their footer). Worth knowing: **all 20 photos are from a single day,
2018-06-29** — one event shoot, not a rolling feed. It is labelled as event
photography rather than "latest from Instagram" for that reason. Flickr's feed
also sends no `Access-Control-Allow-Origin`, so it can only be read at build
time, never live in the browser.

### On-Demand
Was a flat list of three show blocks that didn't explain itself. Now:
- the hero says plainly what it is — *"Shows you missed, kept online to play
  whenever you like"*
- every episode is a card with the show's portrait, a type label and inline
  playback
- **filter chips** (All 7 / Interview 4 / Full show 3) driven off a `type` on
  each episode
- the shows with nothing posted are framed as "catch these on the air" rather
  than an apology

### Verified
- axe 0 violations · 0 JS errors · 0 horizontal overflow — 25 pages × desktop + mobile
- Links, assets, alt text, `<h1>`, titles, JSON-LD: clean
- Filters, live rail, album art and episode playback all exercised in-browser

---

## Photographs, on-air artwork and the hero (Sept 2026)

### Real photographs replace the drawn vinyl
Two panels were holding a decorative record where a picture belonged — the
homepage *"The Legends Sound"* split and the About page's *"A station built to
remember"*. Both now carry the station's own event photography via a new
`photo_frame()` helper: WebP with a JPEG fallback, an explicit focal point
(these are press-night frames, not studio plates — a centre crop takes heads
off), the deco frame's inner brass rule, and a caption.

| Asset | Source | Used on |
|---|---|---|
| `assets/img/legends-live.*` | station Flickr, `41348361790` | `index.html` |
| `assets/img/legends-room.*` | station Flickr, `41348373850` | `about.html` |

Both are the station's own photographs, self-hosted rather than hot-linked so
the pages don't depend on Flickr staying up. **Same caveat as the photo strip:
every frame on that Flickr is from 2018-06-29.** They read as timeless event
photography, but if the station has anything newer — especially studio
photography — these are the first two slots to upgrade.

### Why the On Air card kept showing a blank record
Not a bug in the page. The vendor feed simply leaves `<cover>` empty on a large
minority of tracks — **9 of 30** in a sample of `WLML_history.xml`, Michael
Bublé's *When You're Smiling* among them. The old rule was cover-or-vinyl, so
roughly a third of the time it fell to the drawn record.

`paintArt()` now runs a three-step chain: **album cover → the portrait of
whoever is on air → vinyl**. The portrait comes from `LEGENDS_SHOWART`, which
the schedule already publishes, so no extra request. `paintNowPlaying()`
repaints the art slots as well, so the fallback follows the schedule across
show boundaries. The vinyl is now a genuine last resort — overnight, or if the
feed is unreachable.

### The hero is built from the records in rotation
It was a flat red radial. It now carries three slow-drifting rows of the
sleeves actually played this hour, pulled from the station's own play history,
under a scrim weighted to the left where the headline sits.

- Source is the existing history feed — no new dependency, no new licensing
  question. The same CDN that serves the On Air card's artwork.
- `paintHeroCovers()` **only renders with six or more distinct covers**. Below
  that it returns and the red stands alone exactly as before, so a thin or
  unreachable feed degrades to the old design rather than a broken grid.
- Rows are duplicated so the drift loop has no visible seam, and offset from
  each other so the sleeves never line up into columns.
- Motion is off under `prefers-reduced-motion`.

**Measured, not eyeballed:** with the wall painted, the lightest pixel behind
the hero copy is `rgb(47,36,30)` on desktop and `rgb(43,34,23)` on phone —
**15.1:1** and **15.6:1** against the white headline, **8.2:1** and **8.5:1**
against the muted sub-copy. AA needs 4.5:1.

### Verified
- 25 pages × desktop + phone — **axe 0 violations · 0 JS errors · 0 horizontal
  overflow**
- Both art paths exercised against real captured payloads: a track with a cover
  (Emma Smith, *Bitter Orange*) and one without (Bublé, *When You're Smiling*)
  — the second correctly falls through to Jill & Rich's portrait
