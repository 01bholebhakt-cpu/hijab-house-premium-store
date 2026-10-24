"""Single source of truth for the demo catalogue.
Used by gen_images.py (renders the illustrative images) and build_site.py (writes assets/js/products.js).
Prices are intentionally None = "Price on enquiry" until the owner supplies verified prices.
Fabric/material is intentionally omitted until the owner confirms it.
"""

# colour tuple: (name, hex[, print_hex])
PRODUCTS = [
    # ---------------- HIJABS ----------------
    dict(id="hj-01", name="Emerald Signature Hijab", cat="hijabs", kind="scarf", featured=True, new=True,
         colours=[("Emerald", "#0f5a46"), ("Midnight Navy", "#1d2a44"), ("Ivory", "#efe6d2")],
         desc="Our signature deep-emerald hijab, styled for everyday elegance and special occasions alike."),
    dict(id="hj-02", name="Blush Everyday Hijab", cat="hijabs", kind="scarf", featured=True, new=False,
         colours=[("Blush", "#eebfba"), ("Dusty Rose", "#c68790"), ("Mauve", "#9a7889")],
         desc="A soft, feminine everyday hijab in gentle blush and rose tones."),
    dict(id="hj-03", name="Sand & Mocha Hijab", cat="hijabs", kind="scarf", featured=False, new=False,
         colours=[("Sand", "#d6bf9b"), ("Mocha", "#7a5640"), ("Taupe", "#a39280")],
         desc="Warm neutral hijabs that pair easily with almost any outfit."),
    dict(id="hj-04", name="Midnight Black Hijab", cat="hijabs", kind="scarf", featured=True, new=False,
         colours=[("Black", "#1d1d20"), ("Charcoal", "#45474d")],
         desc="A wardrobe essential in classic black and charcoal."),
    dict(id="hj-05", name="Champagne Luxe Hijab", cat="hijabs", kind="scarf", featured=False, new=True,
         colours=[("Champagne", "#e4d0a2"), ("Antique Gold", "#c4a050"), ("Pearl", "#eee8e4")],
         desc="A luminous champagne-toned hijab for weddings, Eid and celebrations."),
    dict(id="hj-06", name="Garden Print Hijab", cat="hijabs", kind="scarf_print", featured=False, new=True,
         colours=[("Sage Floral", "#a9bba5", "#f1ead8"), ("Rose Floral", "#e9c4c0", "#b46b78"), ("Navy Floral", "#26324f", "#e4d0a2")],
         desc="A floral-printed hijab that adds a graceful pop of pattern."),
    dict(id="hj-07", name="Ivory Pearl Hijab", cat="hijabs", kind="scarf", featured=False, new=False,
         colours=[("Ivory", "#f1ead8"), ("Cream", "#f6efe0")],
         desc="Clean ivory and cream hijabs for a fresh, light look."),
    dict(id="hj-08", name="Dusty Blue Hijab", cat="hijabs", kind="scarf", featured=False, new=False,
         colours=[("Dusty Blue", "#8ea6bf"), ("Lilac", "#b7a6cc"), ("Powder Blue", "#cfdde8")],
         desc="Calm, cool-toned hijabs in dusty blue, lilac and powder blue."),
    # ---------------- CAPS ----------------
    dict(id="cp-01", name="Classic Inner Cap", cat="caps", kind="cap_classic", featured=True, new=False,
         colours=[("Black", "#1d1d20"), ("Ivory", "#efe6d2"), ("Nude", "#d9b99f"), ("Charcoal", "#45474d")],
         desc="An everyday inner cap to wear under your hijab."),
    dict(id="cp-02", name="Tube Inner Cap", cat="caps", kind="cap_tube", featured=False, new=False,
         colours=[("Black", "#1d1d20"), ("Sand", "#d6bf9b"), ("Rose", "#d99a9e")],
         desc="A tube-style inner cap designed to sit neatly under your hijab."),
    dict(id="cp-03", name="Bonnet Hijab Cap", cat="caps", kind="cap_bonnet", featured=False, new=True,
         colours=[("Emerald", "#0f5a46"), ("Navy", "#1d2a44"), ("Black", "#1d1d20")],
         desc="A bonnet-style cap with a decorative bow detail."),
    dict(id="cp-04", name="Lace-Edge Under Cap", cat="caps", kind="cap_lace", featured=False, new=False,
         colours=[("Ivory", "#efe6d2"), ("Blush", "#eebfba")],
         desc="An under cap finished with a delicate lace-style edge."),
    # ---------------- ACCESSORIES ----------------
    dict(id="ac-01", name="Magnetic Hijab Pin Set", cat="accessories", kind="magpin", featured=True, new=True,
         colours=[("Gold", "#d4af55"), ("Silver", "#c9ccd2"), ("Rose Gold", "#d69a86")],
         desc="Magnetic pins for securing your hijab without piercing the fabric."),
    dict(id="ac-02", name="Pearl Head Hijab Pins", cat="accessories", kind="pearlpin", featured=False, new=False,
         colours=[("Gold", "#d4af55"), ("Silver", "#c9ccd2")],
         desc="Classic hijab pins topped with pearl-style heads."),
    dict(id="ac-03", name="Golden Floral Brooch", cat="accessories", kind="brooch_floral", featured=True, new=False,
         colours=[("Gold", "#d4af55"), ("Rose Gold", "#d69a86")],
         desc="A flower-shaped brooch with a crystal centre to dress up any hijab."),
    dict(id="ac-04", name="Crystal Star Brooch", cat="accessories", kind="brooch_star", featured=False, new=True,
         colours=[("Silver", "#c9ccd2"), ("Gold", "#d4af55")],
         desc="A sparkling star-shaped brooch for occasion styling."),
    dict(id="ac-05", name="Crescent Scarf Clip", cat="accessories", kind="clip", featured=False, new=False,
         colours=[("Gold", "#d4af55"), ("Silver", "#c9ccd2")],
         desc="A crescent-shaped clip for gathering and holding scarf folds."),
    dict(id="ac-06", name="Assorted Hijab Pin Pack", cat="accessories", kind="pinpack", featured=False, new=False,
         colours=[("Mixed", "#d4af55")],
         desc="A value pack of assorted hijab pins in different head styles."),
]

CATEGORIES = [
    ("hijabs", "Hijabs", "hijabs.html"),
    ("caps", "Caps & Inner Caps", "caps.html"),
    ("accessories", "Pins & Accessories", "accessories.html"),
]


def slug(s):
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-").replace("--", "-")
