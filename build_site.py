"""Generates every HTML page, assets/js/products.js, sitemap.xml, robots.txt and favicon.
Usage:  python3 tools/build_site.py [https://your-live-site-url]
Re-run after editing catalog.py or any text below.  The generated .html files can also be edited by hand.
"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import PRODUCTS, CATEGORIES, slug

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = (sys.argv[1] if len(sys.argv) > 1 else "https://YOUR-SITE-URL").rstrip("/")
BRAND = "Katihar Hijab House"
TAGLINE = "Modest Fashion for Every You"
ADDRESS = "D.S. College Road, Nasirganj, Katihar, Bihar 854105"
WA_NUM = "918789241790"
WA_DISPLAY = "+91 87892 41790"
WA_LINK = f"https://wa.me/{WA_NUM}"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + "Katihar+Hijab+House+D.S.+College+Road+Nasirganj+Katihar+854105"
TBC = '<span class="tbc">To be confirmed by the store owner</span>'

FAMILY = {
    "Emerald": "Green", "Sage Floral": "Green", "Midnight Navy": "Blue", "Navy": "Blue", "Navy Floral": "Blue",
    "Dusty Blue": "Blue", "Powder Blue": "Blue", "Lilac": "Purple", "Blush": "Pink", "Dusty Rose": "Pink",
    "Mauve": "Pink", "Rose": "Pink", "Rose Floral": "Pink", "Ivory": "Neutral", "Cream": "Neutral", "Sand": "Neutral",
    "Taupe": "Neutral", "Pearl": "Neutral", "Champagne": "Neutral", "Nude": "Neutral", "Mocha": "Brown",
    "Black": "Black & Grey", "Charcoal": "Black & Grey", "Gold": "Gold", "Antique Gold": "Gold", "Mixed": "Gold",
    "Silver": "Silver", "Rose Gold": "Gold",
}
CATLABEL = {c[0]: c[1] for c in CATEGORIES}
CATLABEL["caps"] = "Caps & Inner Caps"

# ------------------------------------------------------------------ products.js
def build_products_js():
    out = []
    for i, p in enumerate(PRODUCTS):
        cols = []
        for c in p["colours"]:
            cols.append(dict(name=c[0], hex=c[1], family=FAMILY.get(c[0], "Neutral"),
                             image=f"assets/products/{p['id']}-{slug(c[0])}.jpg"))
        out.append(dict(id=p["id"], name=p["name"], cat=p["cat"], catLabel=CATLABEL[p["cat"]], desc=p["desc"],
                        featured=bool(p["featured"]), isNew=bool(p["new"]), order=i + 1, price=None, demo=True,
                        colours=cols, detailImage=f"assets/products/{p['id']}-detail.jpg"))
    js = ("/* CENTRAL PRODUCT CATALOGUE — generated from tools/catalog.py (you may also edit this file directly).\n"
          "   price: null  => shown as \"Price on enquiry\".  Set a number (e.g. 499) ONLY when the owner has verified the price.\n"
          "   demo: true   => shows a \"Demo\" tag. Set to false for the owner's real, verified inventory. */\n"
          "window.KHH_PRODUCTS = " + json.dumps(out, indent=2, ensure_ascii=False) + ";\n")
    open(os.path.join(ROOT, "assets/js/products.js"), "w", encoding="utf-8").write(js)


# ------------------------------------------------------------------ chrome
ICON = {
    "search": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "bag": '<svg viewBox="0 0 24 24"><path d="M5 8h14l-1 12H6L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "help": '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4.5-6 8-6s7 2 8 6"/></svg>',
    "menu": '<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "close": '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "truck": '<svg viewBox="0 0 24 24"><path d="M2 6h12v10H2zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
    "chat": '<svg viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12Z"/><path d="M9 10h6M9 14h4"/></svg>',
    "heart": '<svg viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>',
}
WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11 19.8L3 29l6.4-2A13 13 0 1 0 16 3Zm0 2.4a10.6 10.6 0 1 1-5.4 19.7l-.4-.2-3.8 1.2 1.2-3.7-.3-.4A10.6 10.6 0 0 1 16 5.4Zm-4 5.2c-.3 0-.7.1-1 .5-.4.4-1.3 1.3-1.3 3.1s1.3 3.6 1.5 3.9c.2.2 2.6 4.1 6.4 5.6 3.1 1.2 3.8 1 4.5.9.7-.1 2.2-.9 2.5-1.8.3-.9.3-1.6.2-1.8-.1-.2-.4-.3-.8-.5l-2.7-1.3c-.4-.1-.6-.1-.9.2l-1.2 1.5c-.2.3-.5.3-.9.1-.4-.2-1.6-.6-3.1-1.9-1.1-1-1.9-2.3-2.1-2.7-.2-.4 0-.6.2-.8l.6-.7c.2-.2.3-.4.4-.7.1-.3.1-.5 0-.7l-1.2-2.9c-.3-.7-.6-.7-.9-.7Z"/></svg>'

NAV = [("Home", "index.html"), ("Shop", "shop.html"), ("Hijabs", "hijabs.html"), ("Caps", "caps.html"),
       ("Accessories", "accessories.html"), ("New Arrivals", "new-arrivals.html")]


def header(active):
    nav = "".join(f'<a href="{h}"{" class=\"active\" aria-current=\"page\"" if h == active else ""}>{n}</a>' for n, h in NAV)
    mnav = "".join(f'<a href="{h}">{n}</a>' for n, h in NAV + [("About Us", "about.html"), ("Contact", "contact.html"), ("Shipping", "shipping.html"), ("Delivery", "delivery.html"), ("Returns", "returns.html"), ("FAQ", "faq.html")])
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="announce">Shipping all over India &nbsp;·&nbsp; Order easily on WhatsApp <a href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a></div>
<header class="site-header"><div class="container hdr">
<button class="icon-btn menu-btn" id="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav">{ICON["menu"]}</button>
<a class="brand" href="index.html" aria-label="{BRAND} — home"><span class="wordmark">Katihar Hijab House<small>MODEST FASHION</small></span></a>
<nav class="nav" aria-label="Main">{nav}</nav>
<div class="hdr-tools">
<form class="search" action="shop.html" method="get" role="search"><label class="sr-only" for="hs">Search products</label><input id="hs" name="q" type="search" placeholder="Search…"><button class="icon-btn" type="submit" aria-label="Search">{ICON["search"]}</button></form>
<a class="icon-btn" href="contact.html" aria-label="Help and contact" title="Help &amp; contact (no account needed)">{ICON["help"]}</a>
<a class="icon-btn" href="cart.html" aria-label="Shopping bag">{ICON["bag"]}<span class="badge" data-bag-count data-n="0">0</span></a>
</div></div></header>
<div class="scrim" id="scrim"></div>
<aside class="mobile-nav" id="mobile-nav" aria-label="Mobile menu" aria-hidden="true">
<div style="display:flex;justify-content:space-between;align-items:center"><strong style="font-family:var(--serif);font-size:1.3rem;color:var(--emerald-deep)">Menu</strong><button class="icon-btn" id="menu-close" aria-label="Close menu">{ICON["close"]}</button></div>
<form class="m-search search" action="shop.html" method="get" role="search"><label class="sr-only" for="ms">Search products</label><input id="ms" name="q" type="search" placeholder="Search products…"><button class="icon-btn" type="submit" aria-label="Search">{ICON["search"]}</button></form>
{mnav}</aside>'''


def footer():
    return f'''<footer class="site-footer"><div class="container">
<div class="foot-grid">
<div><div class="wordmark">Katihar Hijab House</div><p style="color:var(--gold-light);letter-spacing:.2em;font-size:.72rem;text-transform:uppercase;margin:.3rem 0 1rem">{TAGLINE}</p>
<p>{ADDRESS}</p><p>WhatsApp: <a style="display:inline" href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a></p><p>Shipping all over India.</p></div>
<div><h4>Shop</h4><a href="shop.html">All Products</a><a href="hijabs.html">Hijabs</a><a href="caps.html">Caps &amp; Inner Caps</a><a href="accessories.html">Pins &amp; Accessories</a><a href="new-arrivals.html">New Arrivals</a><a href="cart.html">Shopping Bag</a></div>
<div><h4>Help</h4><a href="shipping.html">Shipping Policy</a><a href="delivery.html">Delivery Information</a><a href="returns.html">Returns &amp; Exchanges</a><a href="faq.html">FAQs</a><a href="contact.html">Contact Us</a></div>
<div><h4>Company</h4><a href="about.html">About Us</a><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms &amp; Conditions</a><a href="{MAPS}" target="_blank" rel="noopener">Find Us on Maps</a></div>
</div>
<div class="foot-bottom"><span>© 2026 {BRAND}. All rights reserved.</span><span>Orders are confirmed by the store on WhatsApp. No online payment on this website.</span></div>
</div></footer>
<a class="wa-float" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Chat with {BRAND} on WhatsApp">{WA_SVG}</a>'''


def page(fname, title, desc, body, active="", data_page="", extra_attrs="", head_extra=""):
    full_title = f"{title} | {BRAND}" if title != BRAND else f"{BRAND} — {TAGLINE}"
    url = f"{SITE_URL}/{'' if fname == 'index.html' else fname}"
    html_ = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#0f5a46">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
{head_extra}</head>
<body data-page="{data_page}" {extra_attrs}>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/products.js"></script>
<script src="assets/js/app.js"></script>
</body>
</html>
'''
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(html_)


def page_head(h1, sub):
    return f'<section class="page-head"><div class="container"><h1>{h1}</h1><p>{sub}</p></div></section>'


def crumbs(*items):
    parts = ['<a href="index.html">Home</a>'] + [f'<a href="{h}">{n}</a>' if h else n for n, h in items]
    return f'<div class="container crumbs" aria-label="Breadcrumb">{"<span>/</span>".join(parts)}</div>'


# ------------------------------------------------------------------ pages
def build_home():
    body = f'''
<section class="hero" aria-label="Welcome">
<div class="container"><div class="hero-inner">
<span class="eyebrow">Katihar Hijab House</span>
<h1>Modest Fashion <em>for Every You</em></h1>
<p>From everyday hijabs to elegant occasion pieces, inner caps, pins and brooches — Katihar Hijab House brings modest fashion to Katihar and ships all over India. Choose your favourites and order easily on WhatsApp.</p>
<div class="actions"><a class="btn gold" href="shop.html">Shop Collection</a><a class="btn light" href="new-arrivals.html">Explore New Arrivals</a></div>
</div></div></section>

<section class="section"><div class="container">
<div class="section-head reveal"><span class="eyebrow">Shop by category</span><h2>Our Collections</h2><div class="orn"><i></i></div><p>Everything you need to complete your modest look, in one place.</p></div>
<div class="tiles">
<a class="tile reveal" href="hijabs.html"><img src="assets/cat-hijabs.jpg" alt="Hijabs in emerald, blush and ivory hanging on a gold rail" width="800" height="1000" loading="lazy"><div class="tile-body"><span>Explore</span><h3>Hijabs</h3></div></a>
<a class="tile reveal" href="caps.html"><img src="assets/cat-caps.jpg" alt="Inner caps and bonnet caps in assorted colours" width="800" height="1000" loading="lazy"><div class="tile-body"><span>Explore</span><h3>Caps &amp; Inner Caps</h3></div></a>
<a class="tile reveal" href="accessories.html"><img src="assets/cat-accessories.jpg" alt="Gold brooch, pearl pins and magnetic pins on emerald fabric" width="800" height="1000" loading="lazy"><div class="tile-body"><span>Explore</span><h3>Pins &amp; Accessories</h3></div></a>
</div></div></section>

<section class="section alt"><div class="container">
<div class="section-head reveal"><span class="eyebrow">Handpicked</span><h2>Featured Products</h2><div class="orn"><i></i></div>
<p class="notice" style="text-align:left">Demonstration range: product images are illustrative and prices are shown as “Price on enquiry” until the store owner supplies verified prices.</p></div>
<div class="grid" id="featured-grid"></div><noscript><p>Please enable JavaScript to browse products.</p></noscript>
<p style="text-align:center;margin-top:2rem"><a class="btn ghost" href="shop.html">View All Products</a></p></div></section>

<section class="section"><div class="container">
<div class="section-head reveal"><span class="eyebrow">Just in</span><h2>New Arrivals</h2><div class="orn"><i></i></div><p>The latest additions to the Katihar Hijab House collection.</p></div>
<div class="grid" id="new-grid"></div>
<p style="text-align:center;margin-top:2rem"><a class="btn" href="new-arrivals.html">See All New Arrivals</a></p></div></section>

<section class="section alt"><div class="container">
<div class="section-head reveal"><span class="eyebrow">Why shop with us</span><h2>Simple, Personal, Trusted</h2><div class="orn"><i></i></div></div>
<div class="benefits">
<div class="benefit reveal">{ICON["truck"]}<h3>Shipping All Over India</h3><p>We deliver across India. Shipping charges and timelines are confirmed by the store when you order.</p></div>
<div class="benefit reveal">{ICON["chat"]}<h3>Easy WhatsApp Ordering</h3><p>Fill your bag, add your address, and send your order to us on WhatsApp in one tap.</p></div>
<div class="benefit reveal">{ICON["heart"]}<h3>Helpful Support</h3><p>A real local store behind every order. Ask us about colours, availability and styling on WhatsApp.</p></div>
</div></div></section>

<section class="section"><div class="container split">
<div class="frame reveal"><img src="assets/story.jpg" alt="Emerald hijab hanging from a gold rail" width="1000" height="1200" loading="lazy"></div>
<div class="reveal"><span class="eyebrow">Our story</span><h2>A Local Store with Modest Fashion at Heart</h2>
<p>Katihar Hijab House is a modest-fashion store on D.S. College Road, Nasirganj, Katihar. We bring together hijabs, caps, pins and accessories so every woman can find a look that feels like her.</p>
<p>Visit us in Katihar or order from anywhere in India through WhatsApp — we’ll help you choose, confirm availability and arrange delivery.</p>
<a class="btn ghost" href="about.html">About Us</a></div>
</div></section>

<section class="cta-band"><div class="container reveal"><h2>Ready to order?</h2><p>Add your favourites to the bag, then send your order to us on WhatsApp. The store owner will confirm availability, final price and delivery details.</p>
<a class="btn gold" href="shop.html">Start Shopping</a> &nbsp; <a class="btn light" href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a></div></section>
'''
    page("index.html", BRAND, f"{BRAND} in Katihar, Bihar — hijabs, inner caps, pins and accessories. {TAGLINE}. Shipping all over India. Order on WhatsApp.", body, "index.html", "home")


def listing(fname, title, h1, sub, desc, active, cat="", new=False):
    attrs = (f'data-cat="{cat}" ' if cat else "") + ('data-new="1"' if new else "")
    body = page_head(h1, sub) + crumbs((h1, None)) + '<section class="container" style="padding-bottom:4rem"><div id="listing"></div><noscript><p>Please enable JavaScript to browse products.</p></noscript></section>'
    page(fname, title, desc, body, active, "listing", attrs)


def build_listings():
    listing("shop.html", "Shop All Products", "Shop All", "Browse hijabs, caps, pins and accessories.", f"Shop the full {BRAND} catalogue: hijabs, inner caps, hijab pins, magnetic pins and brooches. Search, filter and order on WhatsApp.", "shop.html")
    listing("hijabs.html", "Hijabs", "Hijabs", "Everyday and occasion hijabs in a range of colours.", f"Shop hijabs at {BRAND}: emerald, blush, neutral, black, champagne and printed hijabs. Shipping all over India.", "hijabs.html", cat="hijabs")
    listing("caps.html", "Caps & Inner Caps", "Caps & Inner Caps", "Inner caps and under caps to wear beneath your hijab.", f"Inner caps, tube caps, bonnet caps and lace-edge under caps from {BRAND}. Order on WhatsApp.", "caps.html", cat="caps")
    listing("accessories.html", "Pins & Accessories", "Pins & Accessories", "Hijab pins, magnetic pins, brooches and scarf clips.", f"Hijab pins, magnetic pins, brooches and clips from {BRAND}. Finishing touches for modest fashion.", "accessories.html", cat="accessories")
    listing("new-arrivals.html", "New Arrivals", "New Arrivals", "The latest additions to our collection.", f"New arrivals at {BRAND}: the latest hijabs, caps and accessories.", "new-arrivals.html", new=True)


def build_product():
    body = crumbs() .replace('<div class="container crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a></div>', '<div class="container crumbs" id="crumbs" aria-label="Breadcrumb"></div>')
    body += '<section class="container"><div class="pdp" id="pdp"><p>Loading product…</p></div><noscript><p>Please enable JavaScript to view this product.</p></noscript></section>'
    body += '<section class="section alt"><div class="container"><div class="section-head"><span class="eyebrow">You may also like</span><h2>Related Products</h2></div><div class="grid" id="related-grid"></div></div></section>'
    page("product.html", "Product Details", f"View product details, choose a colour and order on WhatsApp from {BRAND}.", body, "shop.html", "product")


def build_cart():
    body = page_head("Your Shopping Bag", "Review your items, then send your order on WhatsApp.") + crumbs(("Shopping Bag", None))
    body += '<section class="container"><div class="cart-layout" id="cart"><p>Loading your bag…</p></div></section>'
    page("cart.html", "Shopping Bag", f"Review your shopping bag at {BRAND}.", body, "", "cart")


STATES = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"]


def build_checkout():
    opts = '<option value="">Select state</option>' + "".join(f"<option>{s}</option>" for s in STATES)

    def f(id_, label, typ="text", ac="", extra="", full=False):
        return f'<div class="{"full" if full else ""}"><label for="{id_}">{label}</label><input class="field" id="{id_}" name="{id_}" type="{typ}" autocomplete="{ac}" {extra} required><div class="err" id="e-{id_}" role="alert"></div></div>'
    form = f'''<form id="co-form" class="panel" novalidate><h3>Delivery details</h3><div class="form">
{f("name", "Full name", ac="name", full=True)}
{f("phone", "Mobile / WhatsApp number", "tel", "tel", 'inputmode="tel" placeholder="10-digit number"', full=True)}
<div class="full"><label for="address">Full delivery address</label><textarea class="field" id="address" name="address" rows="3" autocomplete="street-address" required></textarea><div class="err" id="e-address" role="alert"></div></div>
{f("city", "City / Town", ac="address-level2")}
<div><label for="state">State</label><select class="field" id="state" name="state" autocomplete="address-level1" required>{opts}</select><div class="err" id="e-state" role="alert"></div></div>
{f("pin", "PIN code", "text", "postal-code", 'inputmode="numeric" maxlength="6"')}
<div class="full"><label for="notes">Notes (optional)</label><textarea class="field" id="notes" name="notes" rows="2" placeholder="Colour preference, delivery notes…"></textarea></div>
<div class="full"><button class="btn block" type="submit">Review My Order</button></div></div></form>
<div id="review" class="panel" hidden><h3>Review your order</h3><p>This is the message that will be sent to {BRAND} on WhatsApp. Check it, then tap the green button.</p>
<div class="msg-preview" id="msg"></div>
<p class="notice" style="margin-top:1rem"><strong>Please note:</strong> opening WhatsApp does not confirm your order. The store owner must confirm availability, final price, shipping charges and delivery details with you.</p>
<div style="display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1rem"><button class="btn ghost" id="edit" type="button">Edit Details</button><a class="btn wa" id="send" href="#" target="_blank" rel="noopener">Send Order on WhatsApp</a></div>
<p id="after" hidden class="notice" style="margin-top:1rem">WhatsApp should now be open with your order message. Press <strong>Send</strong> in WhatsApp to deliver it to us. Your order is <strong>not confirmed</strong> until the store replies and confirms. Your bag has been kept in case you need to resend. <a href="cart.html">Back to bag</a></p></div>'''
    body = page_head("WhatsApp Checkout", "Enter your delivery details, review, and send your order.") + crumbs(("Shopping Bag", "cart.html"), ("Checkout", None))
    body += f'<section class="container"><div class="cart-layout" id="checkout"><div>{form}</div><aside class="summary" aria-label="Your order"><h3>Your Order</h3><div id="co-items"></div><p style="font-size:.82rem;color:var(--muted);margin-top:.8rem">No online payment is taken on this website. Payment and delivery are arranged with the store on WhatsApp.</p></aside></div></section>'
    page("checkout.html", "Checkout", f"Enter your delivery details and send your order to {BRAND} on WhatsApp.", body, "", "checkout")


def build_about():
    body = page_head("About Katihar Hijab House", TAGLINE) + crumbs(("About", None)) + f'''
<section class="container"><div class="split" style="padding:1rem 0 3rem">
<div class="frame"><img src="assets/story.jpg" alt="Emerald hijab on a gold rail" width="1000" height="1200" loading="lazy"></div>
<div><span class="eyebrow">Who we are</span><h2>Modest fashion, close to home</h2>
<p>{BRAND} is a modest-fashion store on D.S. College Road, Nasirganj, Katihar, Bihar. We offer hijabs, caps and inner caps, pins, brooches and accessories — and we ship all over India.</p>
<p>This website lets you browse the collection, fill your bag and send your order to us on WhatsApp, so a real person can help you with colours, availability and delivery.</p>
<p>{TBC} Add the owner’s own story, founding year and values here (edit <code>about.html</code>).</p>
<h3>Visit the store</h3><p>{ADDRESS}<br><a href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps</a></p>
<p><a class="btn wa" href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a></p></div></div></section>'''
    page("about.html", "About Us", f"About {BRAND}, a modest-fashion store on D.S. College Road, Nasirganj, Katihar, Bihar. Shipping all over India.", body, "")


def build_contact():
    body = page_head("Contact Us", "We’re happy to help — reach us on WhatsApp or visit the store.") + crumbs(("Contact", None)) + f'''
<section class="container"><div class="contact-grid">
<div><h2>Get in touch</h2>
<div class="contact-card">{ICON["phone"]}<div><b>WhatsApp (ordering &amp; support)</b><a href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a></div></div>
<div class="contact-card">{ICON["pin"]}<div><b>Store address</b>{ADDRESS}<br><a href="{MAPS}" target="_blank" rel="noopener">View on Google Maps</a></div></div>
<div class="contact-card">{ICON["truck"]}<div><b>Shipping</b>All over India</div></div>
<div class="contact-card">{ICON["chat"]}<div><b>Store hours</b>{TBC}</div></div></div>
<form id="ct-form" class="panel" novalidate><h3>Send an enquiry on WhatsApp</h3><div class="form">
<div class="full"><label for="ct-name">Your name</label><input class="field" id="ct-name" autocomplete="name" required><div class="err" id="e-ct-name" role="alert"></div></div>
<div class="full"><label for="ct-phone">Phone (optional)</label><input class="field" id="ct-phone" type="tel" autocomplete="tel"></div>
<div class="full"><label for="ct-msg">Your message</label><textarea class="field" id="ct-msg" rows="5" required placeholder="Ask about a product, colour, price or delivery…"></textarea><div class="err" id="e-ct-msg" role="alert"></div></div>
<div class="full"><button class="btn wa block" type="submit">Send on WhatsApp</button></div></div>
<p style="font-size:.82rem;color:var(--muted);margin:.8rem 0 0">This opens WhatsApp with your message ready to send.</p></form>
</div></section>'''
    page("contact.html", "Contact Us", f"Contact {BRAND}: WhatsApp {WA_DISPLAY}, {ADDRESS}. Send an enquiry on WhatsApp.", body, "", "contact")


def prose(fname, title, h1, sub, inner, desc):
    body = page_head(h1, sub) + crumbs((h1, None)) + f'<section class="container"><div class="prose">{inner}</div></section>'
    page(fname, title, desc, body, "")


def build_policies():
    note = '<p class="notice"><strong>Editable policy.</strong> Anything marked <span class="tbc">To be confirmed by the store owner</span> has not yet been supplied by the store. Edit this page (or <code>tools/build_site.py</code> and re-run it) to add the final wording.</p>'
    prose("shipping.html", "Shipping Policy", "Shipping Policy", "How we ship your order.", note + f'''
<h2>Where we ship</h2><p>{BRAND} ships all over India.</p>
<h2>How orders work</h2><p>Orders are placed through WhatsApp. After you send your order, the store owner replies to confirm availability, final price, shipping charges and delivery details.</p>
<h2>Shipping charges</h2><p>{TBC}</p>
<h2>Courier / dispatch details</h2><p>{TBC}</p>
<h2>Dispatch time</h2><p>{TBC}</p>
<p>Questions? <a href="{WA_LINK}" target="_blank" rel="noopener">Message us on WhatsApp</a>.</p>''', f"Shipping policy of {BRAND}: we ship all over India. Orders are confirmed on WhatsApp.")
    prose("delivery.html", "Delivery Information", "Delivery Information", "What to expect after you order.", note + f'''
<h2>Delivery coverage</h2><p>We deliver all over India.</p>
<h2>Estimated delivery time</h2><p>{TBC}</p>
<p>Delivery time depends on your location and the courier used. The store will share an estimate when it confirms your order on WhatsApp.</p>
<h2>Before delivery</h2><ul><li>Make sure your name, phone number, full address and PIN code are correct.</li><li>Keep your phone reachable on WhatsApp so the store can confirm details.</li></ul>
<h2>Delivery issues</h2><p>If anything looks wrong with your parcel, message us on <a href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp</a> as soon as possible. {TBC}</p>''', f"Delivery information for {BRAND} orders across India.")
    prose("returns.html", "Returns & Exchanges", "Returns & Exchanges", "Our return and exchange policy.", note + f'''
<h2>Returns</h2><p>{TBC}</p>
<h2>Exchanges</h2><p>{TBC}</p>
<h2>Cancellations</h2><p>{TBC}</p>
<h2>Damaged or incorrect items</h2><p>{TBC}</p>
<p>Until the final policy is added, please contact the store on <a href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp</a> before ordering if you have questions.</p>''', f"Return and exchange policy of {BRAND}.")
    prose("privacy.html", "Privacy Policy", "Privacy Policy", "How we handle your information.", note + f'''
<h2>What this website stores</h2><p>Your shopping bag is saved only in your own browser (local storage) so it stays when you refresh or move between pages. It is not sent to any server.</p>
<h2>What we collect when you order</h2><p>When you checkout, the details you enter (name, phone number, delivery address, city, state, PIN code and notes) are placed into a WhatsApp message that <em>you</em> choose to send to {BRAND}. This website does not store those details on a server.</p>
<h2>How the store uses your details</h2><p>The store uses the details you send on WhatsApp only to confirm and deliver your order and to reply to your enquiries. {TBC}</p>
<h2>Third parties</h2><p>WhatsApp is operated by a third party under its own terms and privacy policy. This site loads fonts from Google Fonts.</p>
<h2>Your choices</h2><p>You can clear your bag at any time, or clear this site’s data from your browser settings. To ask about your information held by the store, contact us on <a href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp</a>.</p>
<h2>Contact</h2><p>{BRAND}, {ADDRESS}.</p>''', f"Privacy policy of {BRAND}.")
    prose("terms.html", "Terms & Conditions", "Terms & Conditions", "Please read before ordering.", note + f'''
<h2>About these terms</h2><p>By using this website and placing an order enquiry you agree to these terms. {TBC}</p>
<h2>Orders</h2><p>Orders are placed by sending a message on WhatsApp. An order is <strong>not confirmed</strong> until the store owner confirms availability, final price, shipping charges and delivery details.</p>
<h2>Products and images</h2><p>Product images on this website are for illustration. Actual colour, fabric and finish may vary. Items shown as “Demo” are demonstration products until the store marks them as available inventory.</p>
<h2>Prices</h2><p>Prices shown as “Price on enquiry” are confirmed by the store on WhatsApp. Final prices and shipping charges are confirmed by the store.</p>
<h2>Payment</h2><p>No online payment is taken on this website. Payment methods: {TBC}</p>
<h2>Returns, shipping and cancellations</h2><p>See our <a href="returns.html">Returns &amp; Exchanges</a>, <a href="shipping.html">Shipping</a> and <a href="delivery.html">Delivery</a> pages.</p>
<h2>Governing law</h2><p>{TBC}</p>''', f"Terms and conditions for shopping at {BRAND}.")

    faqs = [
        ("How do I place an order?", "Add items to your bag, go to checkout, enter your delivery details and tap “Send Order on WhatsApp”. Your order message opens in WhatsApp for you to send to us."),
        ("Is my order confirmed once WhatsApp opens?", "No. The store owner must confirm availability, final price, shipping charges and delivery details with you on WhatsApp."),
        ("Do you ship all over India?", "Yes, we ship all over India."),
        ("Can I pay online on this website?", "No. There is no online payment on this website. Payment is arranged with the store on WhatsApp. Accepted payment methods: To be confirmed by the store owner."),
        ("Why do some products say “Price on enquiry”?", "The store owner has not supplied a verified price for that item yet. Send an enquiry on WhatsApp and we will reply with the price."),
        ("Are the product images real photographs?", "Images in this demonstration catalogue are illustrative. The store can send real photos of any item on WhatsApp on request."),
        ("What are the shipping charges and delivery time?", "To be confirmed by the store owner. See our Shipping and Delivery pages."),
        ("Can I return or exchange an item?", "To be confirmed by the store owner. See our Returns & Exchanges page."),
        ("Where is the store?", f"{ADDRESS}."),
    ]
    items = "".join(f'<details><summary>{html.escape(q)}</summary><div class="ans">{a.replace("To be confirmed by the store owner", TBC)}</div></details>' for q, a in faqs)
    body = page_head("Frequently Asked Questions", "Quick answers about ordering and delivery.") + crumbs(("FAQs", None)) + f'<section class="container"><div class="prose faq">{items}<p style="margin-top:2rem">Still have a question? <a href="contact.html">Contact us</a> or message us on <a href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp</a>.</p></div></section>'
    page("faq.html", "FAQs", f"Frequently asked questions about ordering from {BRAND}: WhatsApp orders, shipping across India, prices and more.", body, "")


def build_misc():
    fav = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><!-- PLACEHOLDER favicon: replace with the official Katihar Hijab House logo --><circle cx="32" cy="32" r="30" fill="#0f5a46" stroke="#b8934a" stroke-width="3"/><text x="32" y="43" text-anchor="middle" font-family="Georgia,serif" font-size="32" font-weight="700" fill="#d9bd7e">K</text></svg>'''
    open(os.path.join(ROOT, "assets/favicon.svg"), "w").write(fav)
    pages = ["", "shop.html", "hijabs.html", "caps.html", "accessories.html", "new-arrivals.html", "cart.html", "checkout.html", "about.html", "contact.html", "shipping.html", "delivery.html", "returns.html", "faq.html", "privacy.html", "terms.html"]
    urls = [f"{SITE_URL}/{p}" for p in pages] + [f"{SITE_URL}/product.html?id={p['id']}" for p in PRODUCTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{html.escape(u)}</loc></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /cart.html\nDisallow: /checkout.html\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")


if __name__ == "__main__":
    build_products_js()
    build_home(); build_listings(); build_product(); build_cart(); build_checkout()
    build_about(); build_contact(); build_policies(); build_misc()
    print("built; site url:", SITE_URL)
