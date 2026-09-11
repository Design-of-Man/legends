#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LEGENDS RADIO 100.3 FM — static site generator (redesign concept).
Single source of truth: edit the content below, then `python3 build.py`.

Aesthetic: Art Deco / supper-club glamour for the Great American Songbook.
Everything is self-contained (self-hosted fonts, hand-built CSS/JS, no trackers
beyond nothing). SEO: unique title/desc/canonical, OG/Twitter, JSON-LD
(RadioStation + Person + ItemList + Breadcrumbs), sitemap, robots, manifest.

Facts are grounded in public sources (WLML-FM / legendsradio.com). Programming
blocks that aren't publicly confirmed are descriptive music blocks, not invented
hosted shows — see OWNER TO-DOS at the bottom of this file.
"""
import hashlib, json, os, re, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.legendsradio.com"   # canonical production home (see OWNER TO-DOS)
# Path the site is served from. As a subfolder deploy it MUST be "/legends-radio/" so
# relative assets resolve even when the URL has no trailing slash (Vercel trailingSlash:false
# strips it). For a root-domain deploy (legendsradio.com) set this to "/" and rebuild.
SITE_BASE_PATH = "/"
BUILT = datetime.date.today().isoformat()

# ---------------------------------------------------------------------------
# STATION
# ---------------------------------------------------------------------------
STATION = {
    "name": "Legends Radio 100.3 FM",
    "short": "Legends Radio",
    "call": "WLML-FM",
    "freq": "100.3",
    "slogan": "Where Legendary Music Lives",
    "flourish": "The One and Only…",
    "entertainment": "A Dick Robinson Entertainment Station",
    "heard": "Heard at 100.3 in Palm Beach County",
    "tagline": "The Great American Songbook — live & local from the Palm Beaches.",
    "market": "West Palm Beach / the Palm Beaches",
    "license_city": "Lake Park, FL",
    "founded": "2014",
    "founded_iso": "2014-02-22",
    "parent": "Robinson Entertainment, LLC",
    "phone": "561-469-6700",
    "phone_e164": "+15614696700",
    "request": "561-685-9565",
    "request_e164": "+15616859565",
    "email": "info@legendsradio.com",
    "sales_name": "Tim Reever",
    "sales_title": "Station Manager",
    "sales_phone": "561-469-6702",
    "sales_phone_e164": "+15614696702",
    "sales_email": "treever@legendsradio.com",
    "addr_street": "760 US Highway 1, Suite 102",
    "addr_city": "North Palm Beach",
    "addr_region": "FL",
    "addr_zip": "33408",
    "geo_lat": 26.8172,
    "geo_lng": -80.0561,
    "stream": "https://ice3.securenetsystems.net/WLML",
    "popout": "https://legendsradio.com/listen-live/",
    "instagram": "https://www.instagram.com/legendsradio100.3/",
    "facebook": "https://www.facebook.com/legendsradio",
    "twitter": "https://twitter.com/Legends_Radio",
    "soundcloud": "https://soundcloud.com/legendsradio",
    "tunein": "https://tunein.com/radio/Legends-Radio-1003-s218849/",
    "app_ios": "https://apps.apple.com/us/app/legends-radio-100-3-fm/id6575388465",
    "app_android": "https://play.google.com/store/apps/details?id=com.wlml1.player",
    "eventbrite": "https://www.eventbrite.com/o/8860760162",
    "venue": "Downtown Abacoa Amphitheater · 1267 Main St, Jupiter, FL 33458",
    "spgas": "Society for the Preservation of the Great American Songbook",
}
AREA_SERVED = ["West Palm Beach", "Palm Beach", "North Palm Beach", "Palm Beach Gardens",
               "Jupiter", "Lake Park", "Juno Beach", "Wellington", "Boca Raton", "Stuart"]

# Artists (Great American Songbook staples the station is documented to play).
ARTISTS = ["Frank Sinatra", "Ella Fitzgerald", "Tony Bennett", "Dean Martin", "Nat King Cole",
           "Michael Bublé", "Diana Krall", "Harry Connick Jr.", "Barbra Streisand", "Rod Stewart",
           "Vic Damone", "Jack Jones", "Bobby Darin", "Peggy Lee", "Sammy Davis Jr.",
           "Michael Feinstein", "Sarah Vaughan", "Nancy Wilson"]

# ---------------------------------------------------------------------------
# PATRONS — advertisers & partners
#
# Sourced 2026-09-11 from the station's own live site (legendsradio.com): the
# sitewide "Friends of Legends 100.3" footer, the live banner rotator
# (`?wpbrmethod=ad&id=…`), the sponsored-programming entries in the primary
# nav, and the named testimonial on /advertisers/. Only currently-running
# partners are listed; the rotator also holds a decade of expired 2019–2020
# creative, which is deliberately excluded (see README).
#
# Names and links only. **No advertiser logo artwork is reproduced** — that
# creative belongs to the advertisers, not to the station. Each patron is set
# as an engraved type plate instead, which is both cleaner and rights-safe.
#
# (group heading, group standfirst, [(name, url, kicker, line), …])
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# PROGRAMS — one page per show.
#
# Slots and hosts are the station's own (its weekday lineup graphic and the
# programme entries in its primary nav). Blurbs are descriptive, not invented
# credentials. `audio` and `video` carry only media that actually exists on the
# station's own properties; every other show gets a designed empty state rather
# than a fabricated episode list.
# ---------------------------------------------------------------------------
PROGRAMS = [
    # ---- Weekdays --------------------------------------------------------
    {"slug": "the-morning-lounge", "name": "The Morning Lounge", "kind": "Weekdays",
     "host": "Jill & Rich Switzer", "host_slug": "jill-rich-switzer",
     "slot": "Weekdays · 6–10 AM", "days": "Mon–Fri", "time": "6:00 – 10:00 AM",
     "blurb": "Wake up in the Palm Beaches with live music, warm conversation and the Songbook's "
              "brightest mornings — two working musicians at the top of the day.",
     "audio": [], "video": []},

    {"slug": "middays-with-mike-mcgann", "name": "Middays with Mike McGann", "kind": "Weekdays",
     "host": "Mike McGann", "host_slug": "mike-mcgann",
     "slot": "Weekdays · 10 AM – 2 PM", "days": "Mon–Fri", "time": "10:00 AM – 2:00 PM",
     "blurb": "The full music library, wide open — plus <em>Legends at Lunch</em> every weekday "
              "at noon, a midday set of the greatest recordings ever made.",
     "audio": [], "video": []},

    {"slug": "legends-afternoons", "name": "Legends Afternoons", "kind": "Weekdays",
     "host": "Steve Ketelaar", "host_slug": "steve-ketelaar",
     "slot": "Weekdays · 2–7 PM", "days": "Mon–Fri", "time": "2:00 – 7:00 PM",
     "blurb": "Timeless company from the middle of the afternoon through the golden-hour drive "
              "home across the Palm Beaches.",
     "audio": [], "video": []},

    {"slug": "evenings-with-alex-donner", "name": "Evenings with Alex Donner", "kind": "Weekdays",
     "host": "Alex Donner", "host_slug": "alex-donner",
     "slot": "Weekdays · 7–9 PM", "days": "Mon–Fri", "time": "7:00 – 9:00 PM",
     "blurb": "Supper-club standards for the front end of the night, hosted by the New York "
              "bandleader who has played more society rooms than most orchestras see in a decade.",
     "audio": [], "video": []},

    {"slug": "legends-after-dark", "name": "Legends After Dark", "kind": "Weekdays",
     "host": "Bob Merrill", "host_slug": "bob-merrill",
     "slot": "Weeknights · 9–11 PM", "days": "Mon–Fri", "time": "9:00 – 11:00 PM",
     "blurb": "The lights go down and the arrangements stretch out — late standards to carry the "
              "evening toward the small hours.",
     "audio": [], "video": []},

    {"slug": "american-standards-by-the-sea", "name": "American Standards by the Sea", "kind": "Weekdays",
     "host": "Dick Robinson", "host_slug": "dick-robinson",
     "slot": "Weeknights 11 PM · Sat 6–8 PM · Sun 10 AM", "days": "Nightly & weekends",
     "time": "Weeknights 11 PM – 1 AM · Sat 6–8 PM · Sun 10 AM – 12 PM",
     "blurb": "The station founder's internationally syndicated salute to Sinatra, Bennett, "
              "Streisand and the rest — produced in part aboard his yacht <em>Airwaves</em> and "
              "carried on 75+ stations nationwide.",
     "audio": [], "video": []},

    # ---- Weekends --------------------------------------------------------
    {"slug": "legends-of-jazz", "name": "Legends of Jazz", "kind": "Weekends",
     "host": "Gregory “Popeye” Alexander", "host_slug": "popeye-alexander",
     "slot": "Weekly · See schedule", "days": "Weekly", "time": "See schedule",
     "blurb": "The Songbook's cooler, smokier side — jazz vocals and instrumentals with a real "
              "player at the helm.",
     "audio": [], "video": []},

    {"slug": "sunday-legends-brunch", "name": "Sunday Legends Brunch", "kind": "Weekends",
     "host": "Bob Merrill", "host_slug": "bob-merrill",
     "slot": "Sundays", "days": "Sunday", "time": "See schedule",
     "blurb": "Sunday late morning with a long table, a longer playlist and the occasional "
              "remarkable guest.",
     "audio": [
        {"kind": "soundcloud", "title": "Sunday Legends Brunch — Ken Langone",
         "url": "https://soundcloud.com/legendsradio/sunday-brunch-ken-langone",
         "note": "The Home Depot co-founder in conversation."},
        {"kind": "soundcloud", "title": "Sunday Legends Brunch — Dick Robinson",
         "url": "https://soundcloud.com/legendsradio/sunday-legends-brunch-dick-robinson",
         "note": "The station's founder on the Songbook and the Palm Beaches."},
     ], "video": []},

    {"slug": "cindy-on-legends", "name": "Cindy on Legends", "kind": "Weekends",
     "host": "Cindy Hite", "host_slug": "cindy-hite",
     "slot": "Weekly · See schedule", "days": "Weekly", "time": "See schedule",
     "blurb": "Uplifting conversation and guests — a reminder that Legends is about companionship "
              "as much as it is about music.",
     "audio": [], "video": []},

    {"slug": "the-sounds-of-sinatra", "name": "The Sounds of Sinatra", "kind": "Weekends",
     "host": "Legends 100.3", "host_slug": None,
     "slot": "Weekly · See schedule", "days": "Weekly", "time": "See schedule",
     "blurb": "The Chairman of the Board, hour after hour — the Sinatra catalogue as only a "
              "Songbook station plays it.",
     "audio": [], "video": []},

    {"slug": "community-focus", "name": "Legends Community Focus", "kind": "Weekends",
     "host": "Mike McGann", "host_slug": "mike-mcgann",
     "slot": "Sundays · 6 AM", "days": "Sunday", "time": "6:00 AM",
     "blurb": "A half-hour public-affairs programme on the issues that reach Palm Beach County — "
              "health, preparedness and the causes the station champions. Non-profits can submit "
              "a public service announcement for the free on-air rotation.",
     "audio": [], "video": []},

    {"slug": "pain-2-power", "name": "Pain 2 Power", "kind": "Weekends",
     "host": "Mike McCannon & David Kashuba", "host_slug": None,
     "slot": "Saturdays · 8:30 AM", "days": "Saturday", "time": "8:30 AM",
     "blurb": "A weekly half-hour on health, healing and the mindset that turns pain into power — "
              "Legends' hometown wellness slot.",
     "audio": [], "video": []},

    # ---- From the archive -------------------------------------------------
    {"slug": "legends-international", "name": "Legends International", "kind": "Archive",
     "host": "Philippe Harari", "host_slug": None,
     "slot": "From the archive", "days": "Archive", "time": "Full shows, 2023",
     "blurb": "Full-length shows from the station's international hour, kept online in their "
              "entirety.",
     "audio": [
        {"kind": "mp3", "title": "Full Show — 20 May 2023", "date": "2023-05-20",
         "url": "https://legendsradio.com/wp-content/uploads/2024/05/Legends-May-20-2023-Full-Show.mp3"},
        {"kind": "mp3", "title": "Full Show — 26 August 2023", "date": "2023-08-26",
         "url": "https://legendsradio.com/wp-content/uploads/2024/05/Legends-Aug-26-2023-Full-Show.mp3"},
        {"kind": "mp3", "title": "Veterans Day Full Show — 11 November 2023", "date": "2023-11-11",
         "url": "https://legendsradio.com/wp-content/uploads/2024/05/Legends-Nov-11-2023-Veterans-Day-Full-Show.mp3"},
     ], "video": []},

    {"slug": "legends-of-the-palm-beaches", "name": "Legends of the Palm Beaches", "kind": "Archive",
     "host": "Legends 100.3", "host_slug": None,
     "slot": "From the archive", "days": "Archive", "time": "Interview series",
     "blurb": "Conversations with the people who made the Palm Beaches what they are.",
     "audio": [
        {"kind": "soundcloud", "title": "Ken Langone",
         "url": "https://soundcloud.com/legendsradio/sunday-brunch-ken-langone",
         "note": "Co-founder of The Home Depot."},
        {"kind": "soundcloud", "title": "Dick Robinson",
         "url": "https://soundcloud.com/legendsradio/sunday-legends-brunch-dick-robinson",
         "note": "Founder of Legends Radio."},
     ], "video": []},
]

# ---------------------------------------------------------------------------
# VIDEO — real embeds found on the station's own pages. Titles and channels are
# the ones YouTube itself returns via oEmbed; nothing here is invented.
# `sponsor` marks a clip that belongs to a sponsor's channel rather than the
# station's, so the page can say so plainly.
# ---------------------------------------------------------------------------
VIDEOS = [
    {"id": "WYvRJMJh69I", "title": "Deborah Silver and Freddy Cole — Orange Colored Sky",
     "sub": "Behind the scenes", "channel": "Deborah Silver Music", "group": "In the studio"},
    {"id": "gf5o4x4i6dI", "title": "Ballin’ the Jack — a duet with Ray Benson",
     "sub": "Deborah Silver", "channel": "Deborah Silver Music", "group": "In the studio"},
    {"id": "E5z7g_Tx1A0", "title": "Behind the scenes with Ray Benson and friends",
     "sub": "Recording <em>Glitter &amp; Grits</em>", "channel": "Deborah Silver Music", "group": "In the studio"},
    {"id": "wx-9Vd4hQkY", "title": "That Old Black Magic",
     "sub": "Lyric video", "channel": "Deborah Silver Music", "group": "In the studio"},
    {"id": "BfKB3uJb6sE", "title": "Crash Proof Retirement",
     "sub": "Sponsored programming", "channel": "Crash Proof Retirement", "group": "From our sponsors",
     "sponsor": True},
]

# Palm Beach venues the station keeps company with. Each links to that venue's
# own calendar — we never republish another organisation's listings.
VENUES = [
    ("The Society of the Four Arts", "https://www.fourarts.org/", "Palm Beach"),
    ("Kravis Center for the Performing Arts", "https://www.kravis.org/", "West Palm Beach"),
    ("Palm Beach Symphony", "https://www.palmbeachsymphony.org/", "West Palm Beach"),
    ("Maltz Jupiter Theatre", "https://www.jupitertheatre.org/", "Jupiter"),
    ("The Pops Orchestra of the Palm Beaches", "https://www.popsorchestrapalmbeaches.com/", "The Palm Beaches"),
    ("Palm Beach Dramaworks", "https://www.palmbeachdramaworks.org/", "West Palm Beach"),
    ("Sunrise Theatre", "https://www.sunrisetheatre.com/", "Fort Pierce"),
]

PROGRAM_BY_SLUG = {p["slug"]: p for p in PROGRAMS}

def program_file(slug):
    return "show-%s.html" % slug

# ---------------------------------------------------------------------------
# Live data endpoints (both send Access-Control-Allow-Origin, so the browser
# can read them directly — no backend, no proxy).
#   NOW_PLAYING  current item; goes blank during ad breaks and talk
#   PLAY_HISTORY last 30 songs, newest first, most carrying cover art
#   EVENTS_API   the station's own Events Calendar
# ---------------------------------------------------------------------------
NOW_PLAYING_URL = "https://streamdb5web.securenetsystems.net/player_status_update/WLML.xml"
PLAY_HISTORY_URL = "https://streamdb5web.securenetsystems.net/player_status_update/WLML_history.xml"
EVENTS_API = "https://legendsradio.com/wp-json/tribe/events/v1/events?per_page=50"

def load_events():
    """Build-time snapshot of the station's calendar.

    The page re-fetches EVENTS_API in the browser and reconciles, so this is the
    floor rather than the ceiling: it keeps the page correct with JS off, for
    crawlers, and when the API is unreachable.
    """
    path = os.path.join(ROOT, "assets", "data", "events.json")
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {"fetched": None, "events": []}


PATRONS = [
    ("Friends of Legends",
     "Presenting partners, carried in the house colours on every page of the station.",
     [("Schumacher Auto Group", "https://www.schumacherauto.com/", "Automotive",
       "schumacherauto.com"),
      ("The Lois Pope LIFE Foundation", "https://www.life-edu.org/", "Philanthropy",
       "life-edu.org"),
      ("Preserve Our Gas", "https://preserveourgas.org/your-legends-hour/", "Your Legends Hour",
       "Society for the Preservation of the Great American Songbook"),
      ("CSB Media Arts Center", "https://gocsb.com", "Broadcast Training",
       "Reinventing training in broadcast media"),
      ("Palm Beach Code School", "https://palmbeachcodeschool.com", "Digital Training",
       "Web development, social media marketing &amp; digital filmmaking")]),

    ("Legends Loves the Arts",
     "The stages, scores and seasons the station has kept company with for years.",
     [("The Society of the Four Arts", "https://www.fourarts.org/", "Palm Beach",
       "fourarts.org"),
      ("Palm Beach Symphony", "https://www.palmbeachsymphony.org/", "West Palm Beach",
       "palmbeachsymphony.org"),
      ("The Pops Orchestra of the Palm Beaches", "https://www.popsorchestrapalmbeaches.com/", "The Palm Beaches",
       "popsorchestrapalmbeaches.com"),
      ("Sunrise Theatre", "https://www.sunrisetheatre.com/", "Fort Pierce",
       "sunrisetheatre.com")]),

    ("Sponsored Programs",
     "Weekend hours built around a single brand — the deepest association the station sells.",
     [("Mittleman Eye", "https://mittlemaneye.com/", "Saturdays · 8:00 AM",
       "Through the Eyes of Dr. Mittleman"),
      ("First Rehabilitation", "https://www.firstrehabnpb.com/", "Saturdays · 8:30 AM",
       "Pain to Power with Dave Kashuba"),
      ("The Culture Circuit", "https://culturecircuit.art/", "Saturdays · 9:00 AM",
       "culturecircuit.art"),
      ("The GOLD LAW Firm", "https://goldlaw.com/", "Sundays · 8:00 AM",
       "The Gold Standard Radio Show"),
      ("Hippocrates Wellness", "https://hippocrateswellness.org/", "Sundays · 9:00 AM",
       "Health, Happiness and Healing")]),

    ("Around the Palm Beaches",
     "Neighbours on the air, on the banner rotation, and out on remote.",
     [("The Cosmetic Dentist", "https://www.thecosmeticdentist.com/", "Dentistry",
       "thecosmeticdentist.com"),
      ("Addington Place of Jupiter", "https://www.seniorlifestyle.com/property/florida/addington-place-of-jupiter/", "Jupiter",
       "Live broadcast host — The Morning Lounge"),
      ("Culinary Studio", "https://culinary-studio.com/culinary-clash/", "Dining",
       "Culinary Clash"),
      ("CBS12 News", "https://cbs12.com", "Media Partner",
       "cbs12.com")]),
]

# Audience figures exactly as published by the station on legendsradio.com/advertisers/.
# Quoted, never extrapolated — the footnote on the page says whose numbers these are.
AUDIENCE_PROFILE = [
    ("2&times;", "more likely to be affluent consumers born before 1960"),
    ("3&times;", "more likely to hold $1M+ in investments"),
    ("4&times;", "more likely to buy or sell property each year"),
    ("85%", "more likely to complete their mortgage within 12 months"),
]

# ---------------------------------------------------------------------------
# HOSTS  (confirmed on-air talent + roles; bios use documented facts only)
# ---------------------------------------------------------------------------
HOSTS = [
    {
        "slug": "jill-rich-switzer", "name": "Jill & Rich Switzer", "mono": "J&R",
        "role": "Weekday Mornings", "show": "The Morning Lounge", "slot": "Weekdays · 6–10 AM",
        "photo": "assets/hosts/jill-rich.jpg",
        "persons": ["Jill Switzer", "Rich Switzer"],
        "bio": "South Florida's first couple of the Songbook open every weekday. Jill is one of "
               "the region's most sought-after vocalists — a songwriter and published author — while "
               "Rich is a gifted pianist and composer. Together they also perform their acclaimed "
               "cabaret, <em>Supper Club with Jill &amp; Rich</em>.",
    },
    {
        "slug": "mike-mcgann", "name": "Mike McGann", "mono": "MM",
        "role": "Weekday Middays", "show": "Middays with Mike McGann", "slot": "Weekdays · 10 AM – 2 PM",
        "photo": "assets/hosts/mike-mcgann.jpg",
        "persons": ["Mike McGann"],
        "bio": "Mike carries the middays on Legends 100.3, keeping the Great American Songbook "
               "playing straight through the middle of the day.",
    },
    {
        "slug": "steve-ketelaar", "name": "Steve Ketelaar", "mono": "SK",
        "role": "Weekday Afternoons", "show": "Legends Afternoons with Steve Ketelaar",
        "slot": "Weekdays · 2–7 PM",
        "photo": "assets/hosts/steve-ketelaar.webp",
        "persons": ["Steve Ketelaar"],
        "bio": "Steve rides the afternoon drive on Legends 100.3, carrying the standards from "
               "mid-afternoon through the evening commute.",
    },
    {
        "slug": "alex-donner", "name": "Alex Donner", "mono": "AD",
        "role": "Weekday Evenings", "show": "Evenings with Alex Donner", "slot": "Weekdays · 7–9 PM",
        "photo": "assets/hosts/alex-donner.jpg",
        "persons": ["Alex Donner"],
        "bio": "Alex hosts the evening hours on Legends 100.3 — supper-club standards for the "
               "front end of the night.",
    },
    {
        "slug": "bob-merrill", "name": "Bob Merrill", "mono": "BM",
        "role": "Weeknights & Sundays", "show": "Legends After Dark", "slot": "Weeknights · 9–11 PM",
        "photo": "assets/hosts/bob-merrill.jpg",
        "persons": ["Bob Merrill"],
        "bio": "Bob hosts <em>Legends After Dark</em> on weeknights and returns for the "
               "<em>Sunday Legends Brunch</em>.",
    },
    {
        "slug": "dick-robinson", "name": "Dick Robinson", "mono": "DR",
        "role": "Founder · Late Nights", "show": "American Standards by the Sea",
        "slot": "Weeknights · 11 PM – 1 AM",
        "photo": "assets/hosts/american-standards.jpg",
        "persons": ["Dick Robinson"],
        "bio": "Founder of Legends Radio and of the Connecticut School of Broadcasting. His "
               "<em>American Standards by the Sea</em> is the station's flagship programme, "
               "syndicated well beyond the Palm Beaches.",
    },
    {
        "slug": "popeye-alexander", "name": 'Gregory "Popeye" Alexander', "mono": "PA",
        "role": "Legends of Jazz", "show": "Legends of Jazz", "slot": "Weekly",
        "photo": "assets/hosts/popeye-alexander.jpg",
        "persons": ["Gregory Alexander"],
        "bio": "Popeye hosts <em>Legends of Jazz</em>, the station's dedicated jazz programme.",
    },
    {
        "slug": "cindy-hite", "name": "Cindy Hite", "mono": "CH",
        "role": "Cindy on Legends", "show": "Cindy on Legends", "slot": "Weekly",
        "photo": "assets/hosts/cindy-hite.jpg",
        "persons": ["Cindy Hite"],
        "bio": "Cindy hosts <em>Cindy on Legends</em> on Legends 100.3.",
    },
    {
        "slug": "lauren-may", "name": "Lauren May", "mono": "LM",
        "role": "On Air", "show": "Legends 100.3", "slot": "Weekly",
        "photo": "assets/hosts/lauren-may.jpg",
        "persons": ["Lauren May"],
        "bio": "Lauren May is part of the on-air team at Legends 100.3.",
    },
]

# ---------------------------------------------------------------------------
# WEEKLY SCHEDULE  (Eastern). Keys: 0=Sun … 6=Sat. Fully covers every hour so
# "On Air Now" always resolves. Confirmed hosted shows carry a host; the rest
# are descriptive commercial-free music blocks (see OWNER TO-DOS).
# ---------------------------------------------------------------------------
_OVERNIGHT = {"show": "Nonstop Legends", "host": "Commercial-free standards, all night", "tag": "Overnight"}
_LATENIGHT = {"show": "Dick Robinson's American Standards by the Sea", "host": "Dick Robinson", "tag": "Standards", "slug": "dick-robinson"}
_WEEKDAY = [
    {"start": "00:00", "end": "01:00", **_LATENIGHT},
    {"start": "01:00", "end": "06:00", **_OVERNIGHT},
    {"start": "06:00", "end": "10:00", "show": "The Morning Lounge", "host": "Jill & Rich Switzer", "tag": "Live", "slug": "jill-rich-switzer"},
    {"start": "10:00", "end": "14:00", "show": "Middays with Mike McGann", "host": "Mike McGann", "tag": "Live", "slug": "mike-mcgann"},
    {"start": "14:00", "end": "19:00", "show": "Legends Afternoons with Steve Ketelaar", "host": "Steve Ketelaar", "tag": "Live", "slug": "steve-ketelaar"},
    {"start": "19:00", "end": "21:00", "show": "Evenings with Alex Donner", "host": "Alex Donner", "tag": "Live", "slug": "alex-donner"},
    {"start": "21:00", "end": "23:00", "show": "Legends After Dark", "host": "Bob Merrill", "tag": "Live", "slug": "bob-merrill"},
    {"start": "23:00", "end": "24:00", **_LATENIGHT},
]
SCHEDULE = {
    1: _WEEKDAY, 2: _WEEKDAY, 3: _WEEKDAY, 4: _WEEKDAY, 5: _WEEKDAY,
    6: [  # Saturday
        {"start": "00:00", "end": "08:00", **_OVERNIGHT},
        {"start": "08:00", "end": "08:30", "show": "Saturday Morning Swing", "host": "Big band & swing", "tag": "Music"},
        {"start": "08:30", "end": "09:00", "show": "Pain 2 Power", "host": "Mike McCannon & David Kashuba", "tag": "Talk"},
        {"start": "09:00", "end": "12:00", "show": "Saturday Morning Swing", "host": "Big band & swing", "tag": "Music"},
        {"start": "12:00", "end": "18:00", "show": "Legends Weekend", "host": "The best of the Songbook", "tag": "Music"},
        {"start": "18:00", "end": "20:00", "show": "American Standards by the Sea", "host": "Dick Robinson", "tag": "Signature", "slug": "dick-robinson"},
        {"start": "20:00", "end": "24:00", "show": "Saturday Night Standards", "host": "After-dark classics", "tag": "Music"},
    ],
    0: [  # Sunday
        {"start": "00:00", "end": "07:00", **_OVERNIGHT},
        {"start": "07:00", "end": "10:00", "show": "Sunday Legends Brunch", "host": "Bob Merrill", "tag": "Live", "slug": "bob-merrill"},
        {"start": "07:30", "end": "10:00", "show": "Sunday Morning Standards", "host": "An easy start to Sunday", "tag": "Music"},
        {"start": "10:00", "end": "12:00", "show": "American Standards by the Sea", "host": "Dick Robinson", "tag": "Signature", "slug": "dick-robinson"},
        {"start": "12:00", "end": "18:00", "show": "Sunday Serenade", "host": "Afternoon standards", "tag": "Music"},
        {"start": "18:00", "end": "20:00", "show": "Legends Evenings", "host": "Standards for the evening", "tag": "Music"},
        {"start": "20:00", "end": "22:00", "show": "Legends of Jazz", "host": "Gregory “Popeye” Alexander", "tag": "Jazz", "slug": "popeye-alexander"},
        {"start": "22:00", "end": "24:00", **_OVERNIGHT},
    ],
}
DAYS = [("0", "Sun"), ("1", "Mon"), ("2", "Tue"), ("3", "Wed"), ("4", "Thu"), ("5", "Fri"), ("6", "Sat")]

# Signature / specialty programs (for Shows page cards)

NAV = [("index.html", "Home"), ("listen.html", "Listen"), ("shows.html", "Shows"),
       ("hosts.html", "On-Air"), ("podcast.html", "On-Demand"), ("video.html", "Video"), ("events.html", "Events"),
       ("about.html", "About"), ("advertise.html", "Advertise"), ("contact.html", "Contact")]

# ---------------------------------------------------------------------------
# ASSET CACHE-BUSTING
# ---------------------------------------------------------------------------
def asset_v(relpath):
    p = os.path.join(ROOT, relpath)
    try:
        with open(p, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()[:10]
    except FileNotFoundError:
        return "0"

# ---------------------------------------------------------------------------
# ICONS (inline SVG, currentColor)
# ---------------------------------------------------------------------------
def _svg(body, vb="0 0 24 24"):
    return ('<svg viewBox="%s" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % (vb, body)
IC = {
    "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.14v13.72a1 1 0 0 0 1.54.84l10.29-6.86a1 1 0 0 0 0-1.68L9.54 4.3A1 1 0 0 0 8 5.14z"/></svg>',
    "pause": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>',
    "vol": _svg('<path d="M11 5 6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a9 9 0 0 1 0 14"/>'),
    "external": _svg('<path d="M15 3h6v6M21 3l-9 9M10 5H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/>'),
    "phone": _svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/>'),
    "mail": _svg('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'),
    "pin": _svg('<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    "clock": _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "mic": _svg('<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0M12 17v4"/>'),
    "radio": _svg('<path d="M4 10h16a1 1 0 0 1 1 1v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-8a1 1 0 0 1 1-1z"/><circle cx="8" cy="15" r="2.5"/><path d="M16 6 8 10M15 15h3M15 18h3"/>'),
    "cal": _svg('<rect x="3" y="4.5" width="18" height="17" rx="2"/><path d="M3 9h18M8 2.5v4M16 2.5v4"/>'),
    "arrow": _svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "chevron": _svg('<path d="m9 6 6 6-6 6"/>'),
    "headphones": _svg('<path d="M3 14v-2a9 9 0 0 1 18 0v2"/><path d="M21 15a2 2 0 0 1-2 2h-1v-5h1a2 2 0 0 1 2 2zM3 15a2 2 0 0 0 2 2h1v-5H5a2 2 0 0 0-2 2z"/>'),
    "speaker": _svg('<rect x="5" y="2" width="14" height="20" rx="2"/><circle cx="12" cy="14" r="4"/><path d="M12 6h.01"/>'),
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>',
    "note": _svg('<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'),
    "wave": _svg('<path d="M2 12h2M6 8v8M10 5v14M14 8v8M18 6v12M22 12h0"/>'),
    "heart": _svg('<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 1 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/>'),
    "megaphone": _svg('<path d="m3 11 15-6v14l-15-6zM3 11v4M18 7a4 4 0 0 1 0 10"/><path d="M7 15v4a2 2 0 0 0 2 2h1"/>'),
    "users": _svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>'),
    "ticket": _svg('<path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2 2 2 0 0 0 0 4 2 2 0 0 1-2 2H5a2 2 0 0 1-2-2 2 2 0 0 0 0-4z"/><path d="M13 6v12"/>'),
    "check": _svg('<path d="M20 6 9 17l-5-5"/>'),
    "insta": _svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.5"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor" stroke="none"/>'),
    "facebook": _svg('<path d="M15 3h-3a4 4 0 0 0-4 4v3H5v4h3v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'),
    "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.53 3H20l-5.9 6.74L21 21h-5.4l-4.23-5.53L6.5 21H4l6.3-7.2L3.3 3h5.53l3.82 5.05zM16.6 19.5h1.37L7.5 4.42H6.03z"/></svg>',
    "soundcloud": _svg('<path d="M4 15v-4M7 16V9M10 16V7M13 16V8a4 4 0 0 1 8 0.5 3 3 0 0 1-.5 6H13"/>'),
    "apple": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.4 12.9c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9s-1.8-.8-3-.8c-1.5 0-3 .9-3.8 2.3-1.6 2.8-.4 7 1.2 9.3.8 1.1 1.7 2.4 2.9 2.3 1.2-.1 1.6-.7 3-.7s1.8.7 3 .7 2-1.1 2.8-2.2c.9-1.3 1.2-2.5 1.3-2.6-.1 0-2.5-1-2.5-3.8zM14.2 6.2c.6-.8 1.1-1.9 1-3-1 0-2.1.6-2.8 1.4-.6.7-1.1 1.8-1 2.9 1.1.1 2.2-.5 2.8-1.3z"/></svg>',
    "googleplay": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3.6 2.3 13.4 12 3.6 21.7a1 1 0 0 1-.6-.9V3.2a1 1 0 0 1 .6-.9zM15 10.4l2.8-2.8 3.6 2a1.2 1.2 0 0 1 0 2.1l-3.6 2L15 13.6 16.4 12 15 10.4zM4.9 22.2 14 13.6l2 1.9-9.2 5.2a1.2 1.2 0 0 1-1.9-.5zM4.9 1.8a1.2 1.2 0 0 1 1.9-.5L16 6.5l-2 1.9z"/></svg>',
}

def deco_bar():
    return '<div class="hero-rays" aria-hidden="true"></div>'

# ---------------------------------------------------------------------------
# SHARED COMPONENTS
# ---------------------------------------------------------------------------
def brand():
    return (
        '<a class="brand" href="index.html" aria-label="Legends Radio 100.3 FM home">'
        '<img class="logo" src="assets/img/legends-emblem.svg" alt="" width="46" height="46" loading="eager">'
        '<span class="brand-txt">'
        '<span class="brand-word"><span class="brand-script">Legends</span><span class="brand-radio">radio</span></span>'
        '<small>100.3 FM · Palm Beach County</small></span>'
        '</a>'
    )

def header(active):
    items = ""
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        aria = ' aria-current="page"' if href == active else ""
        items += '<a href="%s"%s%s>%s</a>' % (href, cls, aria, label)
    return (
        '<a class="skip-link" href="#main">Skip to content</a>'
        '<div class="scroll-rail" id="scroll-rail" aria-hidden="true"></div>'
        '<header class="site-header"><div class="container"><nav class="nav" aria-label="Primary">'
        + brand() +
        '<div class="nav-links" id="nav-links">' + items +
        '<a class="btn btn-primary btn-sm mobile-only-cta" href="listen.html" style="margin-top:1.5rem">Listen Live</a>'
        '</div>'
        '<div class="nav-cta">'
        '<a class="btn btn-ghost btn-sm" href="tel:%s" aria-label="Call the studio">%s <span>Studio</span></a>'
        '<button class="btn btn-primary btn-sm" data-play data-play-label-text="Listen Live" aria-pressed="false">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>'
        '</div>'
        '<button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav-links">'
        '<span></span><span></span><span></span></button>'
        '</nav></div></header>'
    ) % (STATION["phone_e164"], IC["phone"])

def player():
    return (
        '<div class="player" role="region" aria-label="Live radio player">'
        '<button class="player-play" data-play aria-pressed="false" aria-label="Play or pause the live stream">'
        '<span class="ic-play">' + IC["play"] + '</span><span class="ic-pause">' + IC["pause"] + '</span>'
        '</button>'
        + art_slot(52, "player-art") +
        '<div class="player-meta">'
        '<span class="p-live"><span class="dot-live"></span> On Air Now</span>'
        '<span class="p-show">Nonstop Legends</span>'
        '<span class="p-host">The Great American Songbook</span>'
        '</div>'
        '<span class="eq player-eq" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>'
        '<span class="player-freq">100.3<span style="font-size:.62em;letter-spacing:.1em"> FM</span></span>'
        '<div class="player-vol">' + IC["vol"] +
        '<input type="range" min="0" max="100" value="85" aria-label="Volume"></div>'
        '<a class="player-pop" href="' + STATION["popout"] + '" target="_blank" rel="noopener" '
        'aria-label="Open pop-out player">' + IC["external"] + '</a>'
        '<audio id="legends-audio" preload="none"></audio>'
        '</div>'
    )

def social_links(cls="foot-social"):
    s = STATION
    return (
        '<div class="%s">'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Instagram">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Facebook">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="X (Twitter)">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="SoundCloud">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="TuneIn">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Apple App Store">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Google Play">%s</a>'
        '</div>'
    ) % (cls, s["instagram"], IC["insta"], s["facebook"], IC["facebook"], s["twitter"], IC["x"],
         s["soundcloud"], IC["soundcloud"], s["tunein"], IC["radio"],
         s["app_ios"], IC["apple"], s["app_android"], IC["googleplay"])

def footer():
    s = STATION
    nav_cols = ""
    listen_links = [("listen.html", "Listen Live"), ("shows.html", "Show Schedule"),
                    ("hosts.html", "On-Air Personalities"), ("podcast.html", "On-Demand & Podcasts"),
                    ("events.html", "Events")]
    station_links = [("about.html", "About the Station"), ("advertise.html", "Advertise With Us"),
                     ("contact.html", "Contact"), (s["eventbrite"], "Buy Event Tickets")]
    def col(title, links):
        li = "".join(
            '<li><a href="%s"%s>%s</a></li>' % (h, (' target="_blank" rel="noopener"' if h.startswith("http") else ""), t)
            for h, t in links)
        return '<div class="footer-col"><h4>%s</h4><ul>%s</ul></div>' % (title, li)
    maps = "https://www.google.com/maps/search/?api=1&query=" + \
           html.escape("%s, %s, %s %s" % (s["addr_street"], s["addr_city"], s["addr_region"], s["addr_zip"]))
    return (
        '<footer class="site-footer"><div class="container"><div class="footer-grid">'
        '<div class="footer-brand">' + brand() +
        '<p>' + s["short"] + ' 100.3 FM is a full-power, live &amp; local station in Florida\'s Palm Beaches, '
        'devoted to preserving and celebrating the Great American Songbook.</p>'
        '<p style="color:var(--gold);font-weight:600;font-size:.82rem;letter-spacing:.03em;margin-top:.9rem">'
        + s["entertainment"] + ' · ' + s["heard"] + '.</p>' + social_links() + '</div>'
        + col("Listen", listen_links) + col("Station", station_links) +
        '<div class="footer-col footer-contact"><h4>Studio</h4><ul>'
        '<li>' + IC["pin"] + '<a href="' + maps + '" target="_blank" rel="noopener">' + s["addr_street"] + '<br>' +
        s["addr_city"] + ', ' + s["addr_region"] + ' ' + s["addr_zip"] + '</a></li>'
        '<li>' + IC["phone"] + '<a href="tel:' + s["phone_e164"] + '">' + s["phone"] + ' · Studio</a></li>'
        '<li>' + IC["mic"] + '<a href="tel:' + s["request_e164"] + '">' + s["request"] + ' · Request Line</a></li>'
        '<li>' + IC["mail"] + '<a href="mailto:' + s["email"] + '">' + s["email"] + '</a></li>'
        '</ul></div>'
        '</div><div class="footer-bottom">'
        '<span>© <span id="year">' + BUILT[:4] + '</span> ' + s["parent"] + ' · ' + s["name"] + ' (' + s["call"] + '). '
        + s["entertainment"] + '. Licensed to ' + s["license_city"] + '.</span>'
        '<span><span class="footer-freq">100.3 FM</span> · ' + s["slogan"] + '</span>'
        '</div></div></footer>'
    )

# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------
def org_schema():
    s = STATION
    return {
        "@type": ["RadioStation", "LocalBusiness"],
        "@id": BASE + "/#station",
        "name": s["name"], "alternateName": s["call"],
        "url": BASE + "/", "slogan": s["slogan"],
        "description": "Legends Radio 100.3 FM (WLML-FM) is a live, local Great American Songbook "
                       "station serving West Palm Beach and the Palm Beaches.",
        "logo": BASE + "/assets/img/favicon.png",
        "image": BASE + "/assets/img/legends-og.png",
        "telephone": s["phone_e164"], "email": s["email"],
        "foundingDate": s["founded_iso"],
        "parentOrganization": {"@type": "Organization", "name": s["parent"]},
        "address": {"@type": "PostalAddress", "streetAddress": s["addr_street"],
                    "addressLocality": s["addr_city"], "addressRegion": s["addr_region"],
                    "postalCode": s["addr_zip"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": s["geo_lat"], "longitude": s["geo_lng"]},
        "broadcastFrequency": {"@type": "BroadcastFrequencySpecification",
                               "broadcastFrequencyValue": s["freq"], "broadcastSignalModulation": "FM"},
        "areaServed": [{"@type": "City", "name": c} for c in AREA_SERVED],
        "sameAs": [s["instagram"], s["soundcloud"], s["tunein"], s["app_ios"], s["app_android"]],
    }

def breadcrumb(title, filename):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": BASE + "/" + filename},
        ],
    }

def jsonld(*nodes):
    graph = [org_schema()]
    for n in nodes:
        if not n:
            continue
        graph.extend(n) if isinstance(n, list) else graph.append(n)
    doc = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">%s</script>' % json.dumps(doc, ensure_ascii=False)

# ---------------------------------------------------------------------------
# DOCUMENT SHELL
# ---------------------------------------------------------------------------
CSS_V = None
JS_V = None

def document(filename, title, desc, body, active, extra_schema=None, og_image="legends-og.png"):
    # One place to guarantee every page ships a snippet-length description.
    desc = clamp_desc(desc)
    canonical = BASE + "/" + ("" if filename == "index.html" else filename)
    og_url = BASE + "/assets/img/" + og_image
    sched_json = json.dumps({str(k): v for k, v in SCHEDULE.items()}, ensure_ascii=False)
    data_script = (
        "window.LEGENDS_SCHEDULE=" + sched_json + ";"
        "window.LEGENDS_STREAM=" + json.dumps(STATION["stream"]) + ";"
        "window.LEGENDS_POPOUT=" + json.dumps(STATION["popout"]) + ";"
        "window.LEGENDS_ARTWORK=" + json.dumps(BASE + "/assets/img/legends-artwork.png") + ";"
        "window.LEGENDS_NOWPLAYING=" + json.dumps(NOW_PLAYING_URL) + ";"
        "window.LEGENDS_HISTORY=" + json.dumps(PLAY_HISTORY_URL) + ";"
    )
    schema = jsonld(breadcrumb(title.split(" | ")[0], filename) if filename != "index.html" else None,
                    extra_schema)
    return (
        "<!doctype html><html lang=\"en\"><head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<base href=\"" + SITE_BASE_PATH + "\">"
        "<title>" + html.escape(title) + "</title>"
        "<meta name=\"description\" content=\"" + html.escape(desc) + "\">"
        "<link rel=\"canonical\" href=\"" + canonical + "\">"
        "<meta name=\"theme-color\" content=\"#0A0B16\">"
        # Open Graph / Twitter
        "<meta property=\"og:type\" content=\"website\">"
        "<meta property=\"og:site_name\" content=\"" + STATION["name"] + "\">"
        "<meta property=\"og:title\" content=\"" + html.escape(title) + "\">"
        "<meta property=\"og:description\" content=\"" + html.escape(desc) + "\">"
        "<meta property=\"og:url\" content=\"" + canonical + "\">"
        "<meta property=\"og:image\" content=\"" + og_url + "\">"
        "<meta property=\"og:image:width\" content=\"1200\"><meta property=\"og:image:height\" content=\"630\">"
        "<meta name=\"twitter:card\" content=\"summary_large_image\">"
        "<meta name=\"twitter:title\" content=\"" + html.escape(title) + "\">"
        "<meta name=\"twitter:description\" content=\"" + html.escape(desc) + "\">"
        "<meta name=\"twitter:image\" content=\"" + og_url + "\">"
        # icons + manifest
        "<link rel=\"icon\" href=\"assets/img/favicon.svg\" type=\"image/svg+xml\">"
        "<link rel=\"icon\" href=\"assets/img/favicon.png\" sizes=\"any\">"
        "<link rel=\"apple-touch-icon\" href=\"assets/img/apple-touch-icon.png\">"
        "<link rel=\"manifest\" href=\"site.webmanifest\">"
        # fonts preload (glamour serif + body sans)
        "<link rel=\"preload\" href=\"assets/fonts/playfair-display-latin-600-normal.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>"
        "<link rel=\"preload\" href=\"assets/fonts/inter-latin-500-normal.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>"
        "<link rel=\"stylesheet\" href=\"assets/css/legends.css?v=" + CSS_V + "\">"
        + schema +
        "</head><body>"
        + header(active) +
        "<main id=\"main\">" + body + "</main>"
        + footer()
        + player()
        + "<script>" + data_script + "</script>"
        + "<script src=\"assets/js/legends.js?v=" + JS_V + "\" defer></script>"
        "</body></html>"
    )

# ---------------------------------------------------------------------------
# SECTION HELPERS
# ---------------------------------------------------------------------------
def eyebrow(text, centered=False):
    return '<span class="eyebrow%s">%s</span>' % (" centered" if centered else "", html.escape(text))

def marquee():
    spans = "".join("<span>%s</span>" % html.escape(a) for a in ARTISTS)
    return ('<div class="marquee" aria-hidden="true"><div class="marquee-track">' + spans + '</div></div>'
            '<div class="sr-only">Legends Radio plays the Great American Songbook: '
            + html.escape(", ".join(ARTISTS)) + '.</div>')

def listen_options_grid():
    tiles = [
        ("headphones", "Online", "Stream free right here — one tap on the Listen Live player.",
         '<button class="btn btn-ghost btn-sm" data-play data-play-label-text="Play Stream"><span data-play-label>Play Stream</span></button>'),
        ("radio", "On Your Radio", "Tune to <strong>100.3 FM</strong> across the Palm Beaches.", ""),
        ("speaker", "Smart Speaker", "Say &ldquo;Alexa, play Legends Radio&rdquo; or ask Google.", ""),
        ("note", "Mobile App", "Take Legends anywhere on iOS &amp; Android.",
         '<a class="btn btn-ghost btn-sm" href="%s" target="_blank" rel="noopener">Get the App %s</a>' % (STATION["app_ios"], IC["external"])),
    ]
    cards = ""
    for i, (ic, h, p, cta) in enumerate(tiles):
        cards += ('<div class="card listen-tile reveal reveal-d%d"><div class="ic">%s</div>'
                  '<h3>%s</h3><p>%s</p>%s</div>') % (i % 4, IC[ic], h, p, ("<div class='mt-2'>%s</div>" % cta if cta else ""))
    return '<div class="listen-grid">' + cards + '</div>'

def cta_band(heading, sub, primary=None, secondary=None):
    p = ('<a class="btn btn-primary btn-lg" href="%s">%s</a>' % primary) if primary else ""
    s = ('<a class="btn btn-ghost btn-lg" href="%s">%s</a>' % secondary) if secondary else ""
    return (
        '<section class="section"><div class="container"><div class="cta-band reveal">'
        + eyebrow("Tune In", True) +
        '<h2>' + heading + '</h2><p class="lede mx-auto" style="margin-inline:auto">' + sub + '</p>'
        '<div class="hero-actions" style="justify-content:center;margin-top:1.8rem">'
        '<button class="btn btn-primary btn-lg" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>' + s +
        '</div></div></div></section>'
    )

def newsletter_block():
    return (
        '<section class="section-tight surface"><div class="container">'
        '<div class="split" style="align-items:center">'
        '<div class="reveal"><span class="eyebrow">Stay in the loop</span>'
        '<h2 style="margin:.6rem 0 .8rem">Never miss a note.</h2>'
        '<p class="lede">Concerts, supper clubs, giveaways, and new shows — straight to your inbox from the Palm Beaches.</p></div>'
        '<div class="reveal reveal-d1"><form class="subscribe" data-endpoint="https://formsubmit.co/ajax/'
        + STATION["email"] + '" data-success="You’re on the list — see you on 100.3!" aria-label="Newsletter signup">'
        '<input type="email" name="email" placeholder="you@example.com" required aria-label="Email address">'
        '<input type="hidden" name="_subject" value="New Legends newsletter signup">'
        '<button class="btn btn-primary" type="submit">Subscribe ' + IC["arrow"] + '</button>'
        '</form><p class="form-note" style="margin-top:.7rem">No spam — just the music. Unsubscribe anytime.</p>'
        '<div class="form-status" role="status"></div></div>'
        '</div></div></section>'
    )

def page_hero(eb, h1, sub, filename):
    crumbs = ('<nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a>'
              '<span>/</span><span style="color:var(--muted)">%s</span></nav>') % html.escape(h1)
    return ('<section class="page-hero">' + deco_bar() + '<div class="container">'
            + eyebrow(eb, True) + '<h1>' + h1 + '</h1>'
            '<div class="rule-deco" aria-hidden="true"><i></i></div>'
            '<p>' + sub + '</p>' + crumbs +
            '</div></section>')

def emblem_big():
    # Art Deco round emblem used inside deco frames
    return (
        '<div class="vinyl-wrap"><div class="vinyl" style="--s:min(340px,64vw)"></div>'
        '<div class="sheen"></div></div>'
    )

EQ7 = '<span class="eq" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>'

EVENTS = [
    {"title": "Live Concerts at Abacoa", "tag": "Free Concert Series", "icon": "ticket",
     "blurb": "Legends Radio &amp; Robinson Entertainment present a free tribute-concert series at the Downtown Abacoa Amphitheater in Jupiter — showtime 7:30 PM, all ages, with optional Preferred Reserved Seating."},
    {"title": "American Songbook Tributes", "tag": "On Stage", "icon": "note",
     "blurb": "From PHD (Petty · Hall &amp; Oates · Steely Dan) to a Chicago tribute and ’60s–’70s celebrations, the concert lineup rotates all season long across the Palm Beaches."},
    {"title": "Supper Club with Jill &amp; Rich", "tag": "Live Cabaret", "icon": "mic",
     "blurb": "An intimate evening of the Great American Songbook performed live by morning hosts Jill &amp; Rich Switzer — the classics the way they were meant to be heard."},
    {"title": "SPGAS Benefactors Gala", "tag": "Black Tie · Give Back", "icon": "heart",
     "blurb": "The Society for the Preservation of the Great American Songbook's signature gala — honoring legends like Marilyn Maye, from Club Colette to the Kravis Center."},
]

ON_DEMAND = [
    {"title": "American Standards by the Sea", "host": "Dick Robinson", "icon": "wave",
     "blurb": "Dick Robinson's syndicated Songbook program, produced in part aboard the yacht <em>Airwaves</em>. "
              "Catch it weeknights at 11 PM — or stream on demand.",
     "cta": "Listen on SoundCloud", "url": STATION["soundcloud"]},
    {"title": "The Legends Radio Archive", "host": "On SoundCloud", "icon": "headphones",
     "blurb": "Interviews, features, and moments from the studio — the station's growing on-demand library, "
              "free to stream anytime.",
     "cta": "Browse the archive", "url": STATION["soundcloud"]},
    {"title": "The Sounds of Sinatra", "host": "Legends 100.3", "icon": "mic",
     "blurb": "The Chairman of the Board, hour after hour — the Sinatra songbook as only Legends plays it.",
     "cta": "Visit the show", "url": "show-the-sounds-of-sinatra.html"},
    {"title": "Cindy on Legends", "host": "Cindy Hite", "icon": "heart",
     "blurb": "Cindy Hite's programme on Legends 100.3, available to stream between broadcasts.",
     "cta": "Follow on SoundCloud", "url": STATION["soundcloud"]},
]

def host_card(h, idx=0, full=False):
    persons = ""
    img = ('<img src="%s" alt="%s, %s on Legends Radio 100.3 FM" loading="lazy" decoding="async">'
           % (h["photo"], html.escape(h["name"]), html.escape(h["role"]))) if h.get("photo") else ""
    bio = ('<p class="host-bio">%s</p>' % h["bio"]) if full else ""
    return (
        '<article class="card host-card reveal reveal-d%d">'
        '<div class="host-medallion">%s<span class="mono">%s</span></div>'
        '<span class="host-role">%s</span>'
        '<h3>%s</h3>'
        '<div class="host-show">%s</div>'
        '<div class="host-slot">%s</div>%s'
        '</article>'
    ) % (idx % 4, img, h["mono"], html.escape(h["role"]), html.escape(h["name"]),
         html.escape(h["show"]), html.escape(h["slot"]), bio)

def show_card(sig, idx=0):
    """Card for one programme. Links through to that show's own page when it
    has one (every entry in PROGRAMS does)."""
    href = program_file(sig["slug"]) if sig.get("slug") else None
    inner = (
        '<span class="pill">%s</span>'
        '<h3 style="margin:.9rem 0 .3rem">%s</h3>'
        '<p style="color:var(--gold);font-weight:600;font-size:.92rem;margin-bottom:.6rem">%s</p>'
        '<p style="color:var(--muted);font-size:.95rem">%s</p>'
    ) % (html.escape(sig["slot"]), html.escape(sig["name"]),
         html.escape(sig["host"]), sig["blurb"])
    if not href:
        return '<article class="card reveal reveal-d%d">%s</article>' % (idx % 4, inner)
    return (
        '<article class="card show-card reveal reveal-d%d">'
        '<a class="show-card-link" href="%s">%s'
        '<span class="show-card-go">Show page %s</span></a>'
        '</article>'
    ) % (idx % 4, href, inner, IC["arrow"])

def event_card(ev, idx=0):
    return (
        '<article class="card reveal reveal-d%d" style="display:flex;flex-direction:column">'
        '<div style="width:56px;height:56px;display:grid;place-items:center;border-radius:15px;margin-bottom:1.2rem;'
        'background:linear-gradient(160deg,rgba(178,61,75,.28),rgba(138,44,56,.12));'
        'border:1px solid rgba(178,61,75,.42);color:var(--gold-bright)">%s</div>'
        '<span class="pill" style="align-self:flex-start">%s</span>'
        '<h3 style="margin:.8rem 0 .45rem">%s</h3>'
        '<p style="color:var(--muted);font-size:.95rem;flex:1">%s</p>'
        '<div class="mt-3"><a class="link-arrow" href="%s" target="_blank" rel="noopener">Dates &amp; tickets on Eventbrite %s</a></div>'
        '</article>'
    ) % (idx % 4, IC[ev["icon"]], ev["tag"], ev["title"], ev["blurb"], STATION["eventbrite"], IC["arrow"])

def np_card():
    return (
        '<div class="np-card">'
        '<div class="np-head"><span class="pill pill-live"><span class="dot-live"></span> On Air Now</span>' + EQ7 + '</div>'
        '<div class="np-body">'
        + art_slot(96) +
        '<div class="np-info">'
        '<div class="np-show" id="np-show">Nonstop Legends</div>'
        '<div class="np-host" id="np-host">The Great American Songbook</div>'
        '<div class="np-time" id="np-time"></div>'
        + track_line() +
        '</div></div>'
        '<div class="np-foot"><span class="np-next" id="np-next">Streaming live from the Palm Beaches</span>'
        '<button class="btn btn-primary btn-sm" data-play data-play-label-text="Listen"><span class="ic-play" style="display:inline-flex">'
        + IC["play"] + '</span> <span data-play-label>Listen</span></button></div>'
        '</div>'
    )

# ===========================================================================
# PAGES
# ===========================================================================
def home_page():
    hero = (
        '<section class="hero">'
        + deco_bar() +
        '<div class="hero-beam b1" aria-hidden="true"></div><div class="hero-beam b2" aria-hidden="true"></div>'
        '<div class="hero-vignette" aria-hidden="true"></div>'
        '<div class="container"><div class="hero-inner">'
        '<div class="hero-copy reveal">'
        '<p class="script-line" style="font-size:clamp(1.9rem,4vw,3rem);margin-bottom:.5rem;display:flex;align-items:center;gap:.5rem">'
        'The One and Only…<img class="deco-flag" src="assets/img/legends-flag.svg" alt="" width="46" height="29"></p>'
        '<div class="hero-badge"><span class="freq">100.3 FM</span><span class="sep"></span>'
        '<small>Live &amp; Local · Palm Beach County</small></div>'
        '<h1>Where <span class="accent foil">Legendary</span><br>Music Lives</h1>'
        '<p class="hero-sub">The Great American Songbook, on the air 24/7 from Florida\'s Palm Beaches — '
        'Sinatra to Bublé, Ella to Krall, all day and all night.</p>'
        '<div class="hero-actions">'
        '<button class="btn btn-primary btn-lg" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>'
        '<a class="btn btn-ghost btn-lg" href="shows.html">Explore the Lineup ' + IC["arrow"] + '</a>'
        '</div>'
        '<div class="hero-meta">'
        '<div><b>2014</b><span>On the Air Since</span></div>'
        '<div><b>75+</b><span>Stations Coast&nbsp;to&nbsp;Coast</span></div>'
        '<div><b>24/7</b><span>Worldwide Stream</span></div>'
        '</div></div>'
        '<div class="hero-visual reveal reveal-d2">' + np_card() + '</div>'
        '</div></div></section>'
    )
    stats = (
        '<section class="section-tight"><div class="container-wide"><div class="stats">'
        '<div class="stat"><div class="num">100.3</div><div class="lbl">FM · Live &amp; Local</div></div>'
        '<div class="stat"><div class="num" data-count="75" data-suffix="+"></div><div class="lbl">Syndicated Stations</div></div>'
        '<div class="stat"><div class="num">2014</div><div class="lbl">On the Air Since</div></div>'
        '<div class="stat"><div class="num">24/7</div><div class="lbl">Worldwide Stream</div></div>'
        '</div></div></section>'
    )
    intro = (
        '<section class="section surface"><div class="container"><div class="split">'
        '<div class="split-media reveal"><div class="deco-frame">' + emblem_big() + '</div></div>'
        '<div class="reveal reveal-d1">' + eyebrow("The Legends Sound") +
        '<h2 style="margin:.7rem 0 1rem">The greatest music ever made — '
        '<span class="serif-italic text-gold">all day, every day.</span></h2>'
        '<p class="lede">There was a time when a song was a story, an orchestra swelled behind a '
        'velvet voice, and the whole room leaned in. That music never went away — it just needed a home.</p>'
        '<p style="margin-top:1rem;color:var(--muted)">Legends 100.3 is a full-power, live and local FM station '
        'in the Palm Beaches, spinning Frank Sinatra, Ella Fitzgerald, Tony Bennett, Michael Bublé, Diana Krall '
        'and the entire Great American Songbook — hosted by real people who love it as much as you do.</p>'
        '<div class="mt-3"><a class="link-arrow" href="about.html">Our story ' + IC["arrow"] + '</a></div>'
        '</div></div></div></section>'
    )
    shows = (
        '<section class="section"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">On the Air</span>'
        '<h2>Signature shows, real hosts</h2>'
        '<p class="lede mx-auto">Live and local, morning to midnight — company for every hour of your day.</p></div>'
        '<div class="grid grid-3">'
        + show_card(PROGRAM_BY_SLUG["the-morning-lounge"], 0) + show_card(PROGRAM_BY_SLUG["middays-with-mike-mcgann"], 1) + show_card(PROGRAM_BY_SLUG["american-standards-by-the-sea"], 2) +
        '</div><div class="center mt-4"><a class="btn btn-ghost" href="shows.html">See the full weekly schedule ' + IC["arrow"] + '</a></div>'
        '</div></section>'
    )
    hosts = (
        '<section class="section surface-deep"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Your Hosts</span>'
        '<h2>The voices of the Palm Beaches</h2></div>'
        '<div class="grid grid-4">'
        + "".join(host_card(h, i) for i, h in enumerate(HOSTS[:4])) +
        '</div><div class="center mt-4"><a class="btn btn-ghost" href="hosts.html">Meet the whole on-air team ' + IC["arrow"] + '</a></div>'
        '</div></section>'
    )
    events = (
        '<section class="section"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Out on the Town</span>'
        '<h2>Legends, live and in the room</h2>'
        '<p class="lede mx-auto">The music leaves the studio all season long across Palm Beach County.</p></div>'
        '<div class="grid grid-3">'
        + "".join(event_card(e, i) for i, e in enumerate(EVENTS[:3])) +
        '</div><div class="center mt-4"><a class="btn btn-ghost" href="events.html">All events &amp; tickets ' + IC["arrow"] + '</a></div>'
        '</div></section>'
    )
    listen = (
        '<section class="section surface"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Four Ways to Listen</span>'
        '<h2>However you tune in, we’re there</h2></div>'
        + listen_options_grid() +
        '</div></section>'
    )
    body = hero + marquee() + stats + intro + shows + hosts + events + listen + patron_ribbon() + newsletter_block() + cta_band(
        "Pour a drink. Turn it up.",
        "The Great American Songbook is playing right now on 100.3 FM — and streaming worldwide.",
        secondary=("shows.html", "Browse Shows"))
    return document("index.html",
                    "Legends Radio 100.3 FM | Great American Songbook · Palm Beaches",
                    "Legends Radio 100.3 FM (WLML) streams the Great American Songbook live from the Palm Beaches — "
                    "Sinatra, Ella, Bublé, Krall and more, 24/7. Listen live online, on 100.3 FM, or on the app.",
                    body, "index.html",
                    extra_schema={"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/",
                                  "name": STATION["name"], "publisher": {"@id": BASE + "/#station"}})

def listen_page():
    hero = page_hero("Listen Live", "Tune the Palm Beaches in.",
                     "One tap and the Great American Songbook is playing — online, on your phone, on your radio, "
                     "or through your smart speaker.", "listen.html")
    big = (
        '<section class="section"><div class="container"><div class="cta-band reveal" style="text-align:center">'
        '<div class="np-head" style="justify-content:center;gap:1rem"><span class="pill pill-live"><span class="dot-live"></span> Streaming Live</span></div>'
        '<div style="display:flex;flex-direction:column;align-items:center;gap:1.4rem;margin-top:1.4rem">'
        '<div class="vinyl-wrap"><div class="vinyl" style="--s:min(240px,58vw)"></div><div class="sheen"></div></div>'
        '<div><div class="np-show" id="np-show" style="font-size:1.8rem">Nonstop Legends</div>'
        '<div class="np-host" id="np-host" style="font-size:1rem;margin-top:.3rem">The Great American Songbook</div>'
        '<div class="np-time" id="np-time" style="margin-top:.4rem"></div></div>'
        '<button class="btn btn-primary btn-lg" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>'
        '<p class="form-note">Or tune to <strong>100.3 FM</strong> across the Palm Beaches · Prefer a pop-out? '
        '<a href="' + STATION["popout"] + '" target="_blank" rel="noopener" style="color:var(--gold);text-decoration:underline">open the player</a></p>'
        '</div></div></div></section>'
    )
    ways = (
        '<section class="section surface"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Ways to Listen</span>'
        '<h2>Legends goes wherever you do</h2></div>' + listen_options_grid() +
        '<div class="grid grid-2 mt-4">'
        '<a class="btn btn-ghost btn-lg btn-block" href="' + STATION["app_ios"] + '" target="_blank" rel="noopener">'
        + IC["apple"] + ' Download for iPhone</a>'
        '<a class="btn btn-ghost btn-lg btn-block" href="' + STATION["app_android"] + '" target="_blank" rel="noopener">'
        + IC["googleplay"] + ' Get it on Google Play</a>'
        '</div></div></section>'
    )
    request = (
        '<section class="section"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("Request Line") +
        '<h2 style="margin:.7rem 0 1rem">Got a request or a dedication?</h2>'
        '<p class="lede">Ask for your favorite standard, send a shout-out, or dedicate a song to someone you love. '
        'Call the request line or drop us a note — our hosts read them on the air.</p>'
        '<div class="mt-3"><a class="btn btn-wine btn-lg" href="tel:' + STATION["request_e164"] + '">'
        + IC["phone"] + ' Call ' + STATION["request"] + '</a></div></div>'
        '<div class="reveal reveal-d1"><form class="form card" data-endpoint="https://formsubmit.co/ajax/'
        + STATION["email"] + '" data-success="Thanks — we’ve got your request. Keep it locked on 100.3!">'
        '<input type="hidden" name="_subject" value="Song request / dedication — legendsradio.com">'
        '<div class="field"><label for="rq-name">Your name</label><input id="rq-name" name="name" required placeholder="First &amp; last"></div>'
        '<div class="field"><label for="rq-song">Your request or dedication</label>'
        '<textarea id="rq-song" name="request" required placeholder="&ldquo;Fly Me to the Moon&rdquo; for my wife Rose on our anniversary…"></textarea></div>'
        '<div class="field"><label for="rq-email">Email <span style="text-transform:none;color:var(--muted-2)">(optional)</span></label>'
        '<input id="rq-email" type="email" name="email" placeholder="you@example.com"></div>'
        '<button class="btn btn-primary" type="submit">Send to the Studio ' + IC["arrow"] + '</button>'
        '<div class="form-status" role="status"></div></form></div>'
        '</div></div></section>'
    )
    body = hero + big + recently_played(12) + marquee() + ways + request
    return document("listen.html",
                    "Listen Live | Legends Radio 100.3 FM · Palm Beaches",
                    "Listen to Legends Radio 100.3 FM live online, on the iOS & Android app, on your radio at "
                    "100.3 FM, or via smart speaker. The Great American Songbook, streaming 24/7.",
                    body, "listen.html",
                    extra_schema={"@type": "BroadcastService", "name": STATION["name"],
                                  "broadcastDisplayName": "Legends 100.3", "provider": {"@id": BASE + "/#station"},
                                  "broadcastFrequency": {"@type": "BroadcastFrequencySpecification",
                                                         "broadcastFrequencyValue": "100.3", "broadcastSignalModulation": "FM"}})

def shows_page():
    hero = page_hero("Shows & Schedule", "The week on Legends 100.3.",
                     "Live hosts by day, standards by night, and specialty programs all weekend — here’s "
                     "everything on the air, with the current show highlighted in real time.", "shows.html")
    sig = (
        '<section class="section"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Signature Programs</span>'
        '<h2>Shows worth setting your day around</h2></div>'
        '<div class="grid grid-3">' + "".join(show_card(s, i) for i, s in enumerate(PROGRAMS)) + '</div>'
        '</div></section>'
    )
    # weekly grid
    tabs = '<div class="sched-tabs" role="tablist" aria-label="Choose a day">'
    for val, label in DAYS:
        tabs += '<button role="tab" data-day="%s" aria-selected="false">%s</button>' % (val, label)
    tabs += '</div>'
    panels = ""
    for val, label in DAYS:
        rows = ""
        day = SCHEDULE[int(val)]
        for i, slot in enumerate(day):
            live_tag = ('<span class="live-badge"><span class="dot-live"></span> Live Now</span>'
                        '<span class="s-tag">%s</span>') % html.escape(slot.get("tag", "Music"))
            rows += (
                '<div class="sched-row" data-day="%s" data-idx="%d" data-start="%s" data-end="%s">'
                '<div class="s-time">%s – %s</div>'
                '<div><div class="s-show">%s</div><div class="s-host">%s</div></div>'
                '<div class="s-meta-right" style="text-align:right">%s</div>'
                '<span class="s-progress"></span>'
                '</div>'
            ) % (val, i, slot["start"], slot["end"], fmt12(slot["start"]), fmt12(slot["end"]),
                 html.escape(slot["show"]), html.escape(slot["host"]), live_tag)
        panels += '<div data-sched-day="%s" class="sched-list" hidden>%s</div>' % (val, rows)
    grid = (
        '<section class="section surface"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Weekly Schedule</span>'
        '<h2>What’s on, right now</h2>'
        '<p class="lede mx-auto">All times Eastern. The live show is highlighted automatically.</p></div>'
        + tabs + panels +
        '<p class="form-note center mt-4">Programming is subject to change — for the very latest, visit '
        '<a href="https://legendsradio.com" target="_blank" rel="noopener" style="color:var(--gold)">legendsradio.com</a>.</p>'
        '</div></section>'
    )
    # ItemList schema for signature shows
    item_list = {"@type": "ItemList", "name": "Legends Radio Shows",
                 "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                      "item": {"@type": "RadioSeries", "name": s["name"]}}
                                     for i, s in enumerate(PROGRAMS)]}
    body = hero + sig + grid + cta_band("Hear it live",
                                        "Whatever’s on right now, it’s the best music ever made — playing on 100.3 FM.",
                                        secondary=("hosts.html", "Meet the Hosts"))
    return document("shows.html",
                    "Shows & Schedule | Legends Radio 100.3 FM",
                    "The full weekly schedule for Legends Radio 100.3 FM — The Morning Lounge, Middays, "
                    "Afternoons, American Standards by the Sea and more. All times Eastern, live show highlighted.",
                    body, "shows.html", extra_schema=item_list)

def hosts_page():
    hero = page_hero("On-Air Personalities", "The people behind the music.",
                     "Live and local means real voices you get to know — the hosts who make Legends 100.3 "
                     "feel like the best table in the room.", "hosts.html")
    grid = (
        '<section class="section"><div class="container"><div class="grid grid-3">'
        + "".join(host_card(h, i, full=True) for i, h in enumerate(HOSTS)) +
        '</div></div></section>'
    )
    # Person schema for each named individual
    persons = []
    for h in HOSTS:
        for name in h["persons"]:
            persons.append({"@type": "Person", "name": name, "jobTitle": "Radio Host",
                            "worksFor": {"@id": BASE + "/#station"}})
    body = hero + grid + newsletter_block() + cta_band(
        "Say hello on the air",
        "Call the request line, send a dedication, or just tell us what you want to hear next.",
        secondary=("contact.html", "Contact the Studio"))
    return document("hosts.html",
                    "On-Air Personalities | Legends Radio 100.3 FM",
                    "Meet the hosts of Legends Radio 100.3 FM — Jill & Rich Switzer, Mike McGann, "
                    "Steve Ketelaar, Alex Donner, Bob Merrill and Dick Robinson — live & local in the Palm Beaches.",
                    body, "hosts.html", extra_schema={"@type": "ItemList",
                                                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": p}
                                                                          for i, p in enumerate(persons)]})

def about_page():
    hero = page_hero("Our Story", "Keeping the Songbook alive.",
                     "Legends 100.3 was signed on the air in 2014 with a single mission: preserve and celebrate "
                     "the greatest music ever recorded — and give it a proud home in the Palm Beaches.", "about.html")
    story = (
        '<section class="section"><div class="container"><div class="split reverse">'
        '<div class="split-media reveal"><div class="deco-frame">' + emblem_big() + '</div></div>'
        '<div class="reveal reveal-d1">' + eyebrow("Since 2014") +
        '<h2 style="margin:.7rem 0 1rem">A station built to remember.</h2>'
        '<p class="lede">Legends Radio was founded by <strong>Dick Robinson</strong> — a broadcasting legend whose '
        'nearly 70-year career began in Massachusetts in 1958 and made him one of the biggest DJs in New England at '
        'WDRC in Hartford. In 1964 he founded the Connecticut School of Broadcasting.</p>'
        '<p style="margin-top:1rem;color:var(--muted)">In 2014, Robinson Entertainment won the 100.3 frequency and '
        'signed Legends on the air to bring “great music and great companionship back to the airwaves” — from the '
        'studios here in North Palm Beach, full-power across the Palm Beaches and streaming worldwide.</p>'
        '<p style="margin-top:1rem;color:var(--muted)"><strong>Locally owned, family-led.</strong> Dick runs the '
        'station with his children — James, Jill, and COO Missy Robinson. Not a national network, not a corporate '
        'boardroom: just a family that loves this music as much as the audience does. That’s the difference you can hear.</p>'
        '</div></div></div></section>'
    )
    quote = (
        '<section class="section surface"><div class="container"><div class="quote reveal">'
        '<div class="mark">&ldquo;</div>'
        '<blockquote>To celebrate timeless music, honor legendary artists, and serve Palm Beach County with '
        'integrity, class, and heart.</blockquote>'
        '<cite>— The Legends Radio Mission</cite></div></div></section>'
    )
    airwaves = (
        '<section class="section"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("The Flagship") +
        '<h2 style="margin:.7rem 0 1rem">American Standards <span class="serif-italic text-gold">by the Sea</span></h2>'
        '<p class="lede">Dick Robinson’s internationally-syndicated, two-hour salute to Sinatra, Bennett, Streisand '
        'and the legends — produced in part aboard his motor yacht <em>Airwaves</em>.</p>'
        '<p style="margin-top:1rem;color:var(--muted)">What began in the Palm Beaches now airs on <strong>75+ stations '
        'nationwide</strong>. Dick is also Founder &amp; Chairman of the <strong>' + STATION["spgas"] + '</strong> '
        '(SPGAS), the 501(c)(3) devoted to keeping this music alive for the next generation.</p>'
        '<div class="mt-3"><a class="link-arrow" href="shows.html">Hear it Sat 6–8 PM &amp; Sun 10 AM–12 PM ' + IC["arrow"] + '</a></div>'
        '</div>'
        '<div class="reveal reveal-d1"><div class="deco-frame" style="aspect-ratio:1/1">' + emblem_big() + '</div></div>'
        '</div></div></section>'
    )
    facts = (
        '<section class="section surface"><div class="container-wide"><div class="stats">'
        '<div class="stat"><div class="num">WLML</div><div class="lbl">FM · Lake Park, FL</div></div>'
        '<div class="stat"><div class="num">100.3</div><div class="lbl">Megahertz</div></div>'
        '<div class="stat"><div class="num" data-count="75" data-suffix="+"></div><div class="lbl">Syndicated Stations</div></div>'
        '<div class="stat"><div class="num">45+</div><div class="lbl">Our Loyal Audience</div></div>'
        '</div></div></section>'
    )
    partners = ["Palm Beach North Chamber of Commerce", "Abacoa", "Cultural Council for Palm Beach County", STATION["spgas"]]
    community = (
        '<section class="section" id="community"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Community &amp; Partners</span>'
        '<h2>Rooted in Palm Beach County</h2>'
        '<p class="lede mx-auto">Legends is a proud member and media partner of the organizations that make the '
        'Palm Beaches sing — on the air, on stage, and in the community.</p></div>'
        '<div style="display:flex;flex-wrap:wrap;gap:.9rem;justify-content:center;max-width:820px;margin-inline:auto">'
        + "".join('<span class="pill" style="font-size:.86rem;padding:.7em 1.2em">%s</span>' % p for p in partners) +
        '</div></div></section>'
    )
    music = (
        '<section class="section surface-deep"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">The Music</span>'
        '<h2>The Great American Songbook</h2>'
        '<p class="lede mx-auto">The timeless standards, swing, and vocal jazz that defined American music — '
        'performed by the artists who made them immortal.</p></div>'
        + marquee() +
        '</div></section>'
    )
    body = hero + story + quote + airwaves + facts + community + music + cta_band(
        "This is your station",
        "Live &amp; local in the Palm Beaches, streaming to the world. Come listen.",
        secondary=("hosts.html", "Meet the Team"))
    return document("about.html",
                    "About | Legends Radio 100.3 FM · Great American Songbook",
                    "Legends Radio 100.3 FM (WLML) was founded in 2014 by broadcaster Dick Robinson to preserve "
                    "the Great American Songbook — live & local from the Palm Beaches, streaming worldwide.",
                    body, "about.html")

def ev_month(iso):
    d = datetime.datetime.strptime(iso[:19], "%Y-%m-%d %H:%M:%S")
    return d.strftime("%B %Y")


def ev_render(e, idx=0):
    """One dated event. build.py renders the snapshot with this; legends.js
    renders live results with the same markup, so a refresh is seamless."""
    d = datetime.datetime.strptime(e["start"][:19], "%Y-%m-%d %H:%M:%S")
    time_txt = "All day" if e.get("all_day") else d.strftime("%-I:%M %p").lower().replace("am", "AM").replace("pm", "PM")
    cost = e.get("cost") or "Free"
    return (
        '<li class="ev reveal reveal-d%d" data-ev-start="%s">'
        '<time class="ev-date" datetime="%s">'
        '<span class="ev-mon">%s</span><span class="ev-day">%s</span><span class="ev-dow">%s</span>'
        '</time>'
        '<div class="ev-body">'
        '<h3 class="ev-title"><a href="%s" target="_blank" rel="noopener">%s</a></h3>'
        '<p class="ev-meta">%s<span class="ev-dot">·</span>%s</p>'
        '<p class="ev-where">%s</p>'
        '</div>'
        '<span class="ev-cost">%s</span>'
        '</li>'
    ) % (idx % 4, html.escape(e["start"], quote=True), d.strftime("%Y-%m-%dT%H:%M:%S"),
         d.strftime("%b"), d.strftime("%-d"), d.strftime("%a"),
         html.escape(e["url"], quote=True), html.escape(e["title"]),
         html.escape(time_txt), html.escape(e.get("venue") or "Venue TBA"),
         html.escape(e.get("address") or ""), html.escape(cost))


def events_page():
    data = load_events()
    evs = data.get("events", [])

    hero = page_hero("Events", "The music, out on the town.",
                     "All season long, Legends 100.3 brings the Great American Songbook off the dial "
                     "and into the Palm Beaches — free concerts, supper clubs and live broadcasts.",
                     "events.html")

    # --- the live board ----------------------------------------------------
    rows, seen_month = "", None
    for i, e in enumerate(evs):
        m = ev_month(e["start"])
        if m != seen_month:
            seen_month = m
            rows += '<li class="ev-month"><span>%s</span></li>' % html.escape(m)
        rows += ev_render(e, i)
    if not rows:
        rows = ('<li class="ev-empty" data-ev-empty>No dates on the calendar right now — '
                'new concerts are announced on the air first.</li>')

    board = (
        '<section class="section" id="calendar"><div class="container">'
        '<div class="ev-head">'
        '<div><span class="eyebrow">What&rsquo;s On</span>'
        '<h2 style="margin:.6rem 0 .4rem">The Legends calendar</h2></div>'
        '<p class="ev-status" data-ev-status data-ev-endpoint="%s">'
        '<span class="ev-dotlive" aria-hidden="true"></span>'
        '<span data-ev-status-text>Showing the schedule as of %s</span></p>'
        '</div>'
        '<div class="ev-countdown" data-ev-countdown hidden>'
        '<span class="cd-lbl">Next up</span>'
        '<strong class="cd-name" data-cd-name></strong>'
        '<span class="cd-clock" data-cd-clock aria-live="polite"></span>'
        '</div>'
        '<ol class="ev-list" data-ev-list>%s</ol>'
        '<p class="form-note center mt-3">Dates come straight from the station&rsquo;s own calendar and '
        'refresh while this page is open. Tickets and reserved seating on '
        '<a href="%s" target="_blank" rel="noopener" style="color:var(--gold)">Eventbrite</a>.</p>'
        '</div></section>'
    ) % (html.escape(EVENTS_API, quote=True),
         html.escape(data.get("fetched") or "the last build"), rows,
         STATION["eventbrite"])

    # --- what the station does, beyond the dated listings -------------------
    strands = (
        '<section class="section surface"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Season Long</span>'
        '<h2>How Legends shows up</h2></div>'
        '<div class="grid grid-4">' + "".join(event_card(e, i) for i, e in enumerate(EVENTS)) + '</div>'
        '</div></section>'
    )

    # --- the wider Palm Beach season ---------------------------------------
    venue_rows = "".join(
        '<li class="venue reveal reveal-d%d"><a href="%s" target="_blank" rel="noopener">'
        '<span class="venue-name">%s</span><span class="venue-city">%s</span>'
        '<span class="venue-go" aria-hidden="true">%s</span></a></li>'
        % (i % 4, html.escape(u, quote=True), html.escape(n), html.escape(c), IC["external"])
        for i, (n, u, c) in enumerate(VENUES))
    around = (
        '<section class="section"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Around the Palm Beaches</span>'
        '<h2>The rest of the season</h2>'
        '<p class="lede mx-auto" style="margin-inline:auto">The houses Legends keeps company with. '
        'Each keeps its own calendar — these go straight to theirs.</p></div>'
        '<ul class="venues">' + venue_rows + '</ul>'
        '</div></section>'
    )

    host_event = (
        '<section class="section surface"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("Host With Legends") +
        '<h2 style="margin:.7rem 0 1rem">Bringing Legends to your event</h2>'
        '<p class="lede">Planning a gala, grand opening or charity night? A live Legends broadcast or a '
        'Songbook performance sets a tone nothing else can — timeless, elegant, unmistakably Palm Beach.</p>'
        '<div class="mt-3"><a class="btn btn-ghost btn-lg" href="contact.html">Talk to us ' + IC["arrow"] + '</a></div></div>'
        '<div class="reveal reveal-d1"><div class="deco-frame" style="aspect-ratio:1/1">' + emblem_big() + '</div></div>'
        '</div></div></section>'
    )

    ld = [{"@type": "Event", "name": e["title"], "startDate": e["start"].replace(" ", "T"),
           "endDate": (e.get("end") or e["start"]).replace(" ", "T"),
           "eventStatus": "https://schema.org/EventScheduled",
           "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
           "url": e["url"],
           "location": {"@type": "Place", "name": e.get("venue") or "",
                        "address": e.get("address") or ""},
           "organizer": {"@type": "Organization", "name": STATION["parent"]}}
          for e in evs]

    body = hero + board + strands + around + host_event + newsletter_block()
    return document("events.html",
                    "Events | Legends Radio 100.3 FM · Palm Beaches",
                    "Upcoming Legends Radio 100.3 FM events across Palm Beach County — free tribute "
                    "concerts at Abacoa, supper clubs and live broadcasts. Updated from the station's "
                    "own calendar.",
                    body, "events.html",
                    extra_schema=(ld if len(ld) != 1 else ld[0]) if ld else None)


def podcast_page():
    hero = page_hero("On-Demand", "Miss a show? Not anymore.",
                     "Legends on your schedule — American Standards by the Sea, studio interviews, and specialty "
                     "shows, streaming free between broadcasts.", "podcast.html")
    cards = ""
    for i, p in enumerate(ON_DEMAND):
        cards += (
            '<article class="card reveal reveal-d%d" style="display:flex;flex-direction:column">'
            '<div class="ic" style="width:54px;height:54px;display:grid;place-items:center;border-radius:14px;'
            'border:1px solid var(--line);background:rgba(231,197,114,.06);color:var(--gold);margin-bottom:1.1rem">%s</div>'
            '<h3 style="font-size:1.25rem;margin-bottom:.25rem">%s</h3>'
            '<p style="color:var(--gold);font-weight:600;font-size:.9rem;margin-bottom:.7rem">%s</p>'
            '<p style="color:var(--muted);font-size:.95rem;flex:1">%s</p>'
            '<div class="mt-3"><a class="link-arrow" href="%s" target="_blank" rel="noopener">%s %s</a></div>'
            '</article>'
        ) % (i % 4, IC[p["icon"]], p["title"], p["host"], p["blurb"], p["url"], p["cta"], IC["external"])
    grid = ('<section class="section"><div class="container"><div class="grid grid-2">' + cards + '</div>'
            '<p class="form-note center mt-4">More on the way — the on-demand library grows every week. Follow '
            '<a href="' + STATION["soundcloud"] + '" target="_blank" rel="noopener" style="color:var(--gold)">SoundCloud</a> '
            'and <a href="' + STATION["instagram"] + '" target="_blank" rel="noopener" style="color:var(--gold)">Instagram</a> for the latest.</p>'
            '</div></section>')
    body = hero + grid + cta_band("Prefer it live?",
                                  "The Great American Songbook is playing right now on 100.3 FM.",
                                  secondary=("shows.html", "See the Schedule"))
    return document("podcast.html",
                    "On-Demand & Podcasts | Legends Radio 100.3 FM",
                    "Stream Legends Radio on demand — American Standards by the Sea, the Legends Radio archive, "
                    "The Sounds of Sinatra, and Cindy on Legends. Free between broadcasts.",
                    body, "podcast.html")

def patron_plate(name, url, kicker, line, idx):
    """One engraved type plate. Deliberately typographic — we do not reproduce
    advertiser logo artwork (see the PATRONS note)."""
    return (
        '<li class="patron-plate reveal reveal-d%d">'
        '<a href="%s" target="_blank" rel="noopener">'
        '<span class="plate-kicker">%s</span>'
        '<span class="plate-name">%s</span>'
        '<span class="plate-rule" aria-hidden="true"></span>'
        '<span class="plate-line">%s</span>'
        '<span class="plate-mark" aria-hidden="true">%s</span>'
        '</a></li>'
    ) % (idx % 4, html.escape(url, quote=True), kicker, html.escape(name), line, IC["external"])


def patrons_board():
    """The signature moment: the page steps out of the midnight supper club and
    into Palm Beach daylight — a scalloped awning over a shell-white trellis,
    with every advertiser set as a brass plate on the patrons' board."""
    groups = ""
    for gi, (heading, standfirst, rows) in enumerate(PATRONS):
        plates = "".join(patron_plate(n, u, k, l, i) for i, (n, u, k, l) in enumerate(rows))
        groups += (
            '<section class="patron-group" aria-labelledby="pg-%d">'
            '<div class="patron-group-head reveal">'
            '<h3 id="pg-%d">%s</h3><p>%s</p>'
            '<span class="patron-count">%02d</span>'
            '</div>'
            '<ul class="patron-board">%s</ul>'
            '</section>'
        ) % (gi, gi, html.escape(heading), standfirst, len(rows), plates)

    total = sum(len(r) for _, _, r in PATRONS)
    return (
        '<section class="patrons" id="patrons">'
        '<div class="awning" aria-hidden="true"><i></i></div>'
        '<div class="trellis" aria-hidden="true"></div>'
        '<div class="container">'
        '<div class="patrons-head reveal">'
        '<span class="eyebrow centered">In Legendary Company</span>'
        '<h2 class="patrons-title">The <em>Patrons</em><span>of 100.3</span></h2>'
        '<p class="patrons-lede">The houses, stages and storefronts that keep the Songbook on the air '
        'across the Palm Beaches. <strong>%d</strong> of them, and room on the board for yours.</p>'
        '</div>%s'
        '<p class="patrons-note">Listed by name only — advertiser artwork remains the property of each business. '
        'Current as of the station&rsquo;s September 2026 schedule and banner rotation.</p>'
        '</div></section>'
    ) % (total, groups)


def patron_ribbon():
    """Compact homepage nod to the roster — a brass ribbon, not a logo wall."""
    names = [n for _, _, rows in PATRONS for (n, _u, _k, _l) in rows]
    spans = "".join('<span>%s</span><i aria-hidden="true"></i>' % html.escape(n) for n in names)
    return (
        '<section class="section-tight ribbon-sec"><div class="container">'
        '<div class="ribbon-head reveal"><span class="eyebrow centered">In Legendary Company</span>'
        '<p>Proudly supported by the Palm Beaches&rsquo; finest.</p></div></div>'
        '<div class="ribbon" aria-hidden="true"><div class="ribbon-track">' + spans + spans + '</div></div>'
        '<div class="sr-only">Legends Radio advertisers and partners: ' + html.escape(", ".join(names)) + '.</div>'
        '<div class="container"><p class="ribbon-cta reveal">'
        '<a href="advertise.html">See the patrons&rsquo; board ' + IC["arrow"] + '</a></p></div>'
        '</section>'
    )


# ---------------------------------------------------------------------------
# NOW PLAYING — album art
#
# Art comes from SecureNetSystems, the station's own streaming vendor, on the
# same CDN that feeds the station's official player. Roughly 40% of tracks
# carry no cover, so the spinning vinyl is the designed fallback rather than a
# broken image.
# ---------------------------------------------------------------------------
def clamp_desc(text, n=155):
    """Search engines cut descriptions around 155 chars — trim on a word
    boundary so nothing ends mid-word."""
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return cut + "\u2026"


def art_slot(size, cls=""):
    return (
        '<div class="art %s" data-art>'
        '<img class="art-img" data-art-img alt="" width="%d" height="%d" hidden>'
        '<div class="vinyl-wrap art-fallback" data-art-fallback>'
        '<div class="vinyl" style="--s:%dpx"></div><div class="sheen"></div></div>'
        '</div>'
    ) % (cls, size, size, size)


def track_line():
    """Live track strip — hidden until the feed actually returns a song, so it
    never renders an empty row during ad breaks or talk."""
    return (
        '<div class="track" data-track hidden>'
        '<span class="track-note" aria-hidden="true">' + IC["note"] + '</span>'
        '<span class="track-txt"><b data-track-title></b><span data-track-artist></span></span>'
        '</div>'
    )


def recently_played(limit=12):
    """Station-wide play history, rendered client-side from the vendor feed."""
    return (
        '<section class="section surface" id="recently-played">'
        '<div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Just Played</span>'
        '<h2>The last hour on 100.3</h2>'
        '<p class="lede mx-auto" style="margin-inline:auto">Straight off the transmitter — '
        'what the Palm Beaches have been listening to, updated as it airs.</p></div>'
        '<ol class="played" data-played data-played-limit="%d" aria-live="polite" aria-label="Recently played songs">'
        '<li class="played-empty" data-played-empty>Loading the playlist&hellip;</li>'
        '</ol>'
        '<noscript><p class="form-note center mt-2">The live playlist needs JavaScript. '
        'You can always hear what&rsquo;s on at <strong>100.3 FM</strong>.</p></noscript>'
        '</div></section>'
    ) % limit


# ---------------------------------------------------------------------------
# AUDIO — the episode archive
# ---------------------------------------------------------------------------
def episode_list(prog):
    eps = prog.get("audio") or []
    if not eps:
        return (
            '<div class="empty reveal">'
            '<div class="empty-ic" aria-hidden="true">' + IC["headphones"] + '</div>'
            '<h3>The archive is open.</h3>'
            '<p>Episodes of <em>%s</em> will appear here as the station posts them. '
            'In the meantime it airs %s &mdash; and the stream never stops.</p>'
            '<div class="empty-actions">'
            '<button class="btn btn-primary btn-sm" data-play data-play-label-text="Listen Live">'
            '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
            '<span data-play-label>Listen Live</span></button>'
            '<a class="btn btn-ghost btn-sm" href="%s" target="_blank" rel="noopener">'
            'The station archive %s</a></div>'
            '</div>'
        ) % (html.escape(prog["name"]), html.escape(prog["slot"]).lower(),
             STATION["soundcloud"], IC["external"])

    rows = ""
    for i, ep in enumerate(eps):
        if ep["kind"] == "mp3":
            rows += (
                '<li class="episode reveal reveal-d%d" data-episode data-src="%s">'
                '<button class="ep-play" data-ep-play aria-label="Play %s">'
                '<span class="ic-play">%s</span><span class="ic-pause">%s</span></button>'
                '<div class="ep-main">'
                '<h3 class="ep-title">%s</h3>'
                '<div class="ep-scrub"><div class="ep-rail" data-ep-rail role="presentation">'
                '<div class="ep-fill" data-ep-fill></div></div>'
                '<span class="ep-time"><span data-ep-now>0:00</span> / <span data-ep-dur>&mdash;&mdash;</span></span>'
                '</div></div>'
                '<a class="ep-dl" href="%s" download aria-label="Download %s">%s</a>'
                '</li>'
            ) % (i % 4, html.escape(ep["url"], quote=True),
                 html.escape(ep["title"], quote=True), IC["play"], IC["pause"],
                 html.escape(ep["title"]), html.escape(ep["url"], quote=True),
                 html.escape(ep["title"], quote=True), IC["arrow"])
        else:  # soundcloud — click-to-load facade, no third-party JS until asked
            rows += (
                '<li class="episode episode-sc reveal reveal-d%d">'
                '<button class="ep-play" data-sc-load '
                'data-sc-url="https://w.soundcloud.com/player/?url=%s&amp;color=%%23E7C572&amp;'
                'hide_related=true&amp;show_comments=false&amp;show_user=true&amp;visual=false" '
                'aria-label="Load and play %s from SoundCloud">'
                '<span class="ic-play">%s</span></button>'
                '<div class="ep-main"><h3 class="ep-title">%s</h3>'
                '<p class="ep-note">%s<span class="ep-src">SoundCloud</span></p></div>'
                '<a class="ep-dl" href="%s" target="_blank" rel="noopener" '
                'aria-label="Open %s on SoundCloud">%s</a>'
                '</li>'
            ) % (i % 4, html.escape(ep["url"], quote=True), html.escape(ep["title"], quote=True),
                 IC["play"], html.escape(ep["title"]),
                 html.escape(ep.get("note", "")), html.escape(ep["url"], quote=True),
                 html.escape(ep["title"], quote=True), IC["external"])
    return '<ol class="episodes">' + rows + '</ol>'


# ---------------------------------------------------------------------------
# VIDEO — click-to-load facades. No YouTube iframe (and no YouTube cookie)
# until the visitor actually asks for the clip.
# ---------------------------------------------------------------------------
def video_card(v, idx=0):
    return (
        '<article class="vid reveal reveal-d%d">'
        '<button class="vid-thumb" data-video="%s" aria-label="Play %s">'
        '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">'
        '<span class="vid-play" aria-hidden="true">%s</span>'
        '</button>'
        '<div class="vid-meta"><h3>%s</h3><p>%s</p>'
        '<span class="vid-chan">%s</span></div>'
        '</article>'
    ) % (idx % 4, v["id"], html.escape(v["title"], quote=True), v["id"], IC["play"],
         html.escape(v["title"]), v.get("sub", ""), html.escape(v["channel"]))


def video_page():
    hero = page_hero("Video", "Legends, on screen.",
                     "Sessions, behind-the-scenes and the occasional lyric video — the Songbook "
                     "with the picture turned on.", "video.html")
    body = hero
    for group in ("In the studio", "From our sponsors"):
        items = [v for v in VIDEOS if v["group"] == group]
        if not items:
            continue
        note = ""
        if group == "From our sponsors":
            note = ('<p class="lede mx-auto" style="margin-inline:auto">Programming paid for by its '
                    'sponsor, published on the sponsor&rsquo;s own channel.</p>')
        body += (
            '<section class="section"><div class="container">'
            '<div class="section-head center"><span class="eyebrow centered">%s</span>'
            '<h2>%s</h2>%s</div>'
            '<div class="vid-grid">%s</div>'
            '</div></section>'
        ) % (html.escape(group), html.escape(group), note,
             "".join(video_card(v, i) for i, v in enumerate(items)))

    body += (
        '<section class="section-tight"><div class="container">'
        '<p class="form-note center">Clips load from YouTube only once you press play, '
        'so nothing is requested from Google until you ask for it.</p>'
        '</div></section>'
    )
    body += cta_band("Rather just listen?",
                     "The stream runs 24 hours a day from the Palm Beaches.",
                     secondary=("shows.html", "See the Schedule"))
    return document("video.html", "Video | Legends Radio 100.3 FM",
                    "Sessions, behind-the-scenes footage and music video from Legends Radio 100.3 FM, "
                    "the Great American Songbook station in Florida's Palm Beaches.",
                    body, "video.html")


# ---------------------------------------------------------------------------
# ONE PAGE PER SHOW
# ---------------------------------------------------------------------------
def program_page(prog):
    host_obj = next((h for h in HOSTS if h["slug"] == prog.get("host_slug")), None)

    crumbs = ('<nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a>'
              '<span>/</span><a href="shows.html">Shows</a>'
              '<span>/</span><span style="color:var(--muted)">%s</span></nav>') % html.escape(prog["name"])

    hero = (
        '<section class="page-hero show-hero" data-show="%s">' % html.escape(prog["name"], quote=True)
        + deco_bar() + '<div class="container">'
        '<span class="eyebrow centered">%s</span>'
        '<h1>%s</h1>'
        '<div class="rule-deco" aria-hidden="true"><i></i></div>'
        '<p class="show-slot">%s<span class="show-dot">·</span>%s</p>'
        '<p>%s</p>'
        '<div class="show-live" data-show-live hidden>'
        '<span class="pill pill-live"><span class="dot-live"></span> On air right now</span>'
        '<button class="btn btn-primary btn-sm" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button></div>'
        + crumbs + '</div></section>'
    ) % (html.escape(prog["kind"]), html.escape(prog["name"]),
         html.escape(prog["days"]), html.escape(prog["time"]), prog["blurb"])

    # --- host ------------------------------------------------------------
    host_block = ""
    if host_obj:
        photo = ('<img src="%s" alt="%s" width="360" height="360" loading="lazy" decoding="async">'
                 % (host_obj["photo"], html.escape(host_obj["name"], quote=True))) if host_obj.get("photo") else \
                ('<span class="mono">%s</span>' % html.escape(host_obj["mono"]))
        host_block = (
            '<section class="section surface"><div class="container"><div class="split">'
            '<div class="reveal show-portrait">%s</div>'
            '<div class="reveal reveal-d1">%s'
            '<h2 style="margin:.7rem 0 1rem">%s</h2>'
            '<p class="lede">%s</p>'
            '<div class="mt-3"><a class="btn btn-ghost btn-sm" href="hosts.html">'
            'All on-air personalities %s</a></div>'
            '</div></div></div></section>'
        ) % (photo, eyebrow("Your Host"), html.escape(host_obj["name"]),
             host_obj["bio"], IC["arrow"])

    # --- audio -------------------------------------------------------------
    audio = (
        '<section class="section" id="listen"><div class="container">'
        '<div class="section-head"><span class="eyebrow">On Demand</span>'
        '<h2>Listen to %s</h2></div>%s'
        '</div></section>'
    ) % (html.escape(prog["name"]), episode_list(prog))

    # --- video (only when the show actually has clips) ----------------------
    vids = [v for v in VIDEOS if v["id"] in (prog.get("video") or [])]
    video = ""
    if vids:
        video = (
            '<section class="section surface"><div class="container">'
            '<div class="section-head"><span class="eyebrow">Watch</span><h2>On screen</h2></div>'
            '<div class="vid-grid">%s</div></div></section>'
        ) % "".join(video_card(v, i) for i, v in enumerate(vids))

    # --- more shows --------------------------------------------------------
    siblings = [p for p in PROGRAMS if p["slug"] != prog["slug"] and p["kind"] == prog["kind"]][:3]
    if len(siblings) < 3:
        siblings += [p for p in PROGRAMS if p["slug"] != prog["slug"] and p not in siblings][:3 - len(siblings)]
    more = (
        '<section class="section"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Keep Listening</span>'
        '<h2>More on 100.3</h2></div>'
        '<div class="grid grid-3">%s</div>'
        '<div class="center mt-4"><a class="btn btn-ghost" href="shows.html">'
        'The full weekly schedule %s</a></div>'
        '</div></section>'
    ) % ("".join(show_card(p, i) for i, p in enumerate(siblings)), IC["arrow"])

    schema = {"@type": "RadioSeries", "name": prog["name"],
              "description": re.sub(r"<[^>]+>", "", prog["blurb"]),
              "url": BASE + "/" + program_file(prog["slug"]),
              "productionCompany": {"@type": "Organization", "name": STATION["parent"]},
              "publication": {"@type": "BroadcastEvent", "isLiveBroadcast": True,
                              "publishedOn": {"@type": "RadioChannel", "name": STATION["name"]}}}
    if host_obj:
        schema["actor"] = [{"@type": "Person", "name": n} for n in host_obj.get("persons", [host_obj["name"]])]

    body = hero + audio + host_block + video + more
    lead = "%s on Legends Radio 100.3 FM, %s. " % (prog["name"], prog["slot"])
    return document(program_file(prog["slug"]),
                    "%s with %s | Legends Radio 100.3 FM" % (prog["name"], prog["host"])
                    if prog.get("host_slug") else "%s | Legends Radio 100.3 FM" % prog["name"],
                    clamp_desc(lead + re.sub(r"<[^>]+>", "", prog["blurb"])),
                    body, "shows.html", extra_schema=schema)


def advertise_page():
    s = STATION
    hero = page_hero("Advertise", "Palm Beach County’s gateway to the top ten percent.",
                     "Legends 100.3 is the only commercial station in the market curated for Palm Beach&rsquo;s "
                     "highest earners — delivered by the most trusted voices on the air, to listeners with the "
                     "means and the appetite to buy.", "advertise.html")

    # --- The pitch, in the station's own published terms -------------------
    figures = "".join(
        '<li class="fig reveal reveal-d%d"><span class="fig-num">%s</span><span class="fig-lbl">%s</span></li>'
        % (i % 4, n, l) for i, (n, l) in enumerate(AUDIENCE_PROFILE))
    pitch = (
        '<section class="section surface"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("The Audience") +
        '<h2 style="margin:.7rem 0 1rem">The top 10% of households,<br>listening on purpose.</h2>'
        '<p class="lede">Legends reaches Palm Beach County households with expendable income of '
        '$250,000 or more — an audience that drives nearly half of all U.S. consumer spending, and '
        'stays with a station for hours rather than minutes.</p>'
        '<p class="lede" style="margin-top:1rem">Seventy-five percent of Americans say they trust radio '
        'hosts more than television personalities. On 100.3 those hosts are Palm Beach figures in their '
        'own right — entertainers, philanthropists and community leaders whose endorsement carries '
        'weight a banner never will.</p>'
        '</div>'
        '<div class="reveal reveal-d1"><ul class="figures">' + figures + '</ul>'
        '<p class="figures-note">Audience figures as published by Legends Radio 100.3.</p></div>'
        '</div></div></section>'
    )

    # --- Why advertisers choose Legends -----------------------------------
    why = [
        ("users", "Target affluence", "The only commercial station in the market curated for Palm Beach&rsquo;s top earners — no waste, no spill into audiences you are not trying to reach."),
        ("radio", "One buy, four platforms", "100.3 FM, the worldwide stream, the iOS and Android apps, and the station&rsquo;s social channels — bought once, delivered everywhere."),
        ("mic", "Trusted local voices", "Live reads and host endorsements from the personalities your customers invite into the car, the kitchen and the office every day."),
        ("megaphone", "Syndicated reach", "<em>American Standards by the Sea</em> carries the station — and its sponsors — to 75+ affiliates nationwide."),
        ("ticket", "On air, online, in person", "Supper clubs, live remotes and concerts at Abacoa put your brand in front of the audience with a drink in their hand."),
        ("check", "Turnkey creative", "A local partner who writes it, produces it and plans the flight — built on the holy trinity of reach, frequency and creativity."),
    ]
    cards = "".join(
        '<article class="card reveal reveal-d%d"><div class="ic" style="width:52px;height:52px;display:grid;place-items:center;'
        'border-radius:14px;border:1px solid var(--line);background:rgba(231,197,114,.06);color:var(--gold);margin-bottom:1rem">%s</div>'
        '<h3 style="font-size:1.2rem;margin-bottom:.4rem">%s</h3><p style="color:var(--muted);font-size:.95rem">%s</p></article>'
        % (i % 4, IC[ic], t, p) for i, (ic, t, p) in enumerate(why))
    grid = ('<section class="section"><div class="container">'
            '<div class="section-head center"><span class="eyebrow centered">Why Legends</span>'
            '<h2>Legendary company for your brand</h2></div>'
            '<div class="grid grid-3">' + cards + '</div></div></section>')

    # --- Testimonial (published on legendsradio.com/advertisers/) ----------
    quote = (
        '<section class="section-tight"><div class="container"><figure class="testimonial reveal">'
        '<blockquote><p>On air, online and in person&hellip; on-target results. Legends is very helpful and '
        'conscientious in relaying the proper messaging to give us an audible voice to many and bring us '
        'successful results.</p></blockquote>'
        '<figcaption><span class="t-name">Jennifer Jones</span>'
        '<span class="t-role">Director of Communication · Palm Beach Symphony</span></figcaption>'
        '</figure></div></section>'
    )

    # --- Sales contact + enquiry form -------------------------------------
    form = (
        '<section class="section surface"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("Let’s Talk") +
        '<h2 style="margin:.7rem 0 1rem">There is room on the board.</h2>'
        '<p class="lede">Tell us a little about your business and what you are hoping to move. We will come '
        'back with a plan — on air, streaming, digital and events.</p>'
        '<div class="sales-card mt-3">'
        '<span class="sales-eb">Station Manager</span>'
        '<span class="sales-name">' + s["sales_name"] + '</span>'
        '<ul class="stack-sm">'
        '<li>' + IC["phone"] + ' <a href="tel:' + s["sales_phone_e164"] + '">' + s["sales_phone"] + '</a></li>'
        '<li>' + IC["mail"] + ' <a href="mailto:' + s["sales_email"] + '">' + s["sales_email"] + '</a></li>'
        '<li>' + IC["pin"] + ' ' + s["addr_street"] + ', ' + s["addr_city"] + ', ' + s["addr_region"] + ' ' + s["addr_zip"] + '</li>'
        '</ul></div></div>'
        '<div class="reveal reveal-d1"><form class="form card" data-endpoint="https://formsubmit.co/ajax/'
        + s["email"] + '" data-success="Thank you — a Legends representative will reach out shortly.">'
        '<input type="hidden" name="_subject" value="New advertising inquiry — legendsradio.com">'
        '<div class="row"><div class="field"><label for="ad-name">Name</label><input id="ad-name" name="name" required></div>'
        '<div class="field"><label for="ad-co">Company</label><input id="ad-co" name="company" required></div></div>'
        '<div class="row"><div class="field"><label for="ad-email">Email</label><input id="ad-email" type="email" name="email" required></div>'
        '<div class="field"><label for="ad-phone">Phone</label><input id="ad-phone" type="tel" name="phone"></div></div>'
        '<div class="field"><label for="ad-msg">What are you hoping to promote?</label>'
        '<textarea id="ad-msg" name="message" required placeholder="Tell us about your business, timing, and goals…"></textarea></div>'
        '<button class="btn btn-primary" type="submit">Request a Media Kit ' + IC["arrow"] + '</button>'
        '<div class="form-status" role="status"></div></form></div>'
        '</div></div></section>'
    )

    body = hero + why_stats() + pitch + patrons_board() + quote + grid + form
    return document("advertise.html",
                    "Advertise on Legends Radio 100.3 FM | Palm Beach Radio Advertising",
                    "Advertise on Legends Radio 100.3 FM and reach the top 10% of Palm Beach County households "
                    "— FM, streaming, mobile, syndication and events. See the patrons’ board and request a media kit.",
                    body, "advertise.html")

def why_stats():
    return (
        '<section class="section-tight"><div class="container-wide"><div class="stats">'
        '<div class="stat"><div class="num">45+</div><div class="lbl">Core Audience</div></div>'
        '<div class="stat"><div class="num">4</div><div class="lbl">Platforms · FM · Stream · App · Events</div></div>'
        '<div class="stat"><div class="num" data-count="75" data-suffix="+"></div><div class="lbl">Syndicated Stations</div></div>'
        '<div class="stat"><div class="num">24/7</div><div class="lbl">Always On</div></div>'
        '</div></div></section>'
    )

def contact_page():
    s = STATION
    hero = page_hero("Contact", "Say hello.",
                     "Requests, dedications, advertising, events, or just to tell us what you love — we’d love to "
                     "hear from you.", "contact.html")
    maps_q = html.escape("%s, %s, %s %s" % (s["addr_street"], s["addr_city"], s["addr_region"], s["addr_zip"]))
    maps_link = "https://www.google.com/maps/search/?api=1&query=" + maps_q
    info = (
        '<section class="section"><div class="container"><div class="grid grid-2" style="gap:2.4rem;align-items:start">'
        '<div class="reveal">'
        '<div class="card"><h3 style="margin-bottom:1.2rem">Studio &amp; Offices</h3>'
        '<ul class="footer-contact" style="font-size:1rem">'
        '<li>' + IC["pin"] + '<a href="' + maps_link + '" target="_blank" rel="noopener">' + s["addr_street"] + '<br>' +
        s["addr_city"] + ', ' + s["addr_region"] + ' ' + s["addr_zip"] + '</a></li>'
        '<li>' + IC["phone"] + '<div><a href="tel:' + s["phone_e164"] + '">' + s["phone"] + '</a><br>'
        '<span style="color:var(--muted-2);font-size:.85rem">Studio &amp; Sales</span></div></li>'
        '<li>' + IC["mic"] + '<div><a href="tel:' + s["request_e164"] + '">' + s["request"] + '</a><br>'
        '<span style="color:var(--muted-2);font-size:.85rem">On-Air Request Line</span></div></li>'
        '<li>' + IC["mail"] + '<a href="mailto:' + s["email"] + '">' + s["email"] + '</a></li>'
        '</ul>' + social_links("foot-social") + '</div>'
        '<div class="mt-3 deco-frame" style="aspect-ratio:16/10;padding:2.2rem;text-align:center;'
        'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.1rem">'
        '<div style="width:66px;height:66px;display:grid;place-items:center;border-radius:50%;'
        'border:1px solid var(--line);background:rgba(231,197,114,.06);color:var(--gold);position:relative;z-index:1">'
        '<span style="width:30px">' + IC["pin"] + '</span></div>'
        '<div style="position:relative;z-index:1"><div style="font-family:var(--serif);font-size:1.5rem;color:#fff">North Palm Beach, Florida</div>'
        '<div style="color:var(--muted);font-size:.92rem;margin-top:.3rem">' + s["addr_street"] + ' · ' + s["addr_zip"] + '</div></div>'
        '<a class="btn btn-primary btn-sm" href="' + maps_link + '" target="_blank" rel="noopener" style="position:relative;z-index:1">'
        + IC["pin"] + ' Get Directions</a></div></div>'
        '<div class="reveal reveal-d1"><form class="form card" data-endpoint="https://formsubmit.co/ajax/'
        + s["email"] + '" data-success="Thank you — we’ll be in touch soon. Keep it locked on 100.3!">'
        '<input type="hidden" name="_subject" value="New message from legendsradio.com">'
        '<div class="row"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required></div>'
        '<div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required></div></div>'
        '<div class="row"><div class="field"><label for="c-phone">Phone</label><input id="c-phone" type="tel" name="phone"></div>'
        '<div class="field"><label for="c-topic">Reason</label><select id="c-topic" name="topic">'
        '<option>General</option><option>Song Request / Dedication</option><option>Advertising</option>'
        '<option>Events</option><option>Careers</option></select></div></div>'
        '<div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea></div>'
        '<button class="btn btn-primary" type="submit">Send Message ' + IC["arrow"] + '</button>'
        '<div class="form-status" role="status"></div></form></div>'
        '</div></div></section>'
    )
    body = hero + info
    return document("contact.html",
                    "Contact | Legends Radio 100.3 FM · Palm Beaches",
                    "Contact Legends Radio 100.3 FM in North Palm Beach — studio " + s["phone"] + ", request line "
                    + s["request"] + ", or " + s["email"] + ". Requests, advertising, events and more.",
                    body, "contact.html")

def not_found_page():
    body = (
        '<section class="page-hero" style="min-height:70vh;display:flex;align-items:center">'
        + deco_bar() + '<div class="container">'
        + eyebrow("404", True) +
        '<h1 style="font-size:clamp(3rem,9vw,6rem)">Off the dial</h1>'
        '<p>We couldn’t tune in that page — but the music’s still playing.</p>'
        '<div class="hero-actions" style="justify-content:center;margin-top:2rem">'
        '<button class="btn btn-primary btn-lg" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>'
        '<a class="btn btn-ghost btn-lg" href="index.html">Back Home ' + IC["arrow"] + '</a>'
        '</div></div></section>'
    )
    return document("404.html", "Page Not Found | Legends Radio 100.3 FM",
                    "That page is off the dial — head back home and keep listening to Legends Radio 100.3 FM.",
                    body, "")

# ---------------------------------------------------------------------------
def fmt12(hhmm):
    h, m = int(hhmm[:2]), int(hhmm[3:5])
    if h == 24:
        h = 0
    ap = "PM" if h >= 12 else "AM"
    h12 = h % 12 or 12
    return ("%d:%02d %s" % (h12, m, ap)) if m else ("%d %s" % (h12, ap))

# ===========================================================================
# SEO FILES
# ===========================================================================
PAGES = (["index.html", "listen.html", "shows.html", "hosts.html", "podcast.html",
          "video.html", "events.html", "about.html", "advertise.html", "contact.html"]
         + [program_file(p["slug"]) for p in PROGRAMS])

def build_sitemap():
    urls = ""
    for p in PAGES:
        loc = BASE + "/" + ("" if p == "index.html" else p)
        pri = "1.0" if p == "index.html" else ("0.9" if p in ("listen.html", "shows.html") else "0.7")
        urls += ("<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq>"
                 "<priority>%s</priority></url>") % (loc, BUILT, pri)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>'

def build_robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE

def build_manifest():
    return json.dumps({
        "name": STATION["name"], "short_name": "Legends 100.3",
        "description": "The Great American Songbook, live from the Palm Beaches.",
        "start_url": "index.html", "display": "standalone",
        "background_color": "#0A0B16", "theme_color": "#0A0B16",
        "icons": [
            {"src": "assets/img/favicon.png", "sizes": "512x512", "type": "image/png"},
            {"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    }, indent=2)

# ===========================================================================
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return len(content)

def main():
    global CSS_V, JS_V
    CSS_V = asset_v("assets/css/legends.css")
    JS_V = asset_v("assets/js/legends.js")
    pages = {
        "index.html": home_page(), "listen.html": listen_page(), "shows.html": shows_page(),
        "hosts.html": hosts_page(), "podcast.html": podcast_page(), "events.html": events_page(),
        "about.html": about_page(), "advertise.html": advertise_page(), "contact.html": contact_page(),
        "video.html": video_page(), "404.html": not_found_page(),
    }
    for prog in PROGRAMS:
        pages[program_file(prog["slug"])] = program_page(prog)
    total = 0
    for path, content in pages.items():
        total += write(path, content)
    write("sitemap.xml", build_sitemap())
    write("robots.txt", build_robots())
    write("site.webmanifest", build_manifest())
    print("Built %d pages + sitemap/robots/manifest (%d KB) · css v=%s js v=%s"
          % (len(pages), total // 1024, CSS_V, JS_V))
    print("Preview:  python3 -m http.server 8000  →  http://localhost:8000/legends-radio/")

if __name__ == "__main__":
    main()
