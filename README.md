# Katihar Hijab House — Online Store

A complete, multi-page, static online store (plain HTML, CSS and JavaScript — no build step, no database).
Customers browse, fill a shopping bag and **send their order to WhatsApp (+91 87892 41790)**. There is no online payment.

> **Important — what is demonstration content and what is real**
> * The 18 products, their descriptions and **all product images are demonstration content**. The images are
>   illustrative renders created for this project (not photographs of real stock). Every card is tagged **Demo**.
> * **No prices have been invented.** Every product shows **“Price on enquiry”** until you add a verified price.
> * Fabric / material, stock counts, ratings, discounts and reviews are intentionally **not shown** (none were supplied).
> * Shipping charges, delivery times, return/exchange/cancellation terms, store hours and payment methods are marked
>   **“To be confirmed by the store owner”**.
> * The **official logo was not supplied**, so the header uses a text wordmark and `assets/favicon.svg` is a plain placeholder.

---

## 1. Run it on your computer

Just open `index.html` in a browser, or run a tiny local server (recommended):

```bash
cd katihar-hijab-house
python3 -m http.server 8000      # then open http://localhost:8000
```

## 2. Replace the demo content with your real shop

### Product photos
1. Put your own photos in `assets/products/` (JPG, ideally 800 × 1000 px, under ~150 KB each).
2. Open `assets/js/products.js`. For each product, point `"image"` (one per colour) and `"detailImage"` to your file names.
3. Keep file names without spaces. Change `"demo": true` to `"demo": false` for real, verified stock (removes the “Demo” tag
   and the demonstration notice on the product page).

### Prices
In `assets/js/products.js` change `"price": null` to the verified number, e.g. `"price": 499`.
The bag and checkout then show totals automatically. If **any** item in a bag is still `null`, the site shows
“Price on enquiry” and does **not** calculate a total.
(Price sorting appears automatically once at least one price is set.)

### Add / remove / rename products
Edit `assets/js/products.js` directly, **or** edit `tools/catalog.py` and run
`python3 tools/build_site.py` (regenerates `products.js` and all pages). Product pages are generated from the product `id`
(`product.html?id=hj-01`), so no new HTML file is needed per product.

### Logo
Add your official logo as `assets/logo.png`, then in `assets/js/app.js` set `logo: 'assets/logo.png'`.
Replace `assets/favicon.svg` with a favicon made from your logo.

### Policies, FAQ, About, hours
Edit `shipping.html`, `delivery.html`, `returns.html`, `faq.html`, `privacy.html`, `terms.html`, `about.html`, `contact.html`.
Search for **“To be confirmed by the store owner”** and replace each with your real wording.
(If you re-run `tools/build_site.py`, edit the text inside that file instead, because the script rewrites the HTML pages.)

### WhatsApp number
Set `whatsapp` in `assets/js/app.js` (`CONFIG`) and `WA_NUM` / `WA_DISPLAY` in `tools/build_site.py`, then re-run the build.

## 3. Set your live website address (SEO)

After you know your final URL, run:

```bash
python3 tools/build_site.py https://your-site-name.vercel.app
```

This updates canonical links, social-sharing tags, `sitemap.xml` and `robots.txt`.

## 4. Deploy

### Option A — Vercel (easiest)
1. Create a free GitHub account and a new **public or private repository**; upload everything in this folder
   (drag-and-drop on github.com → *Add file → Upload files*).
2. Go to **vercel.com** → *Add New → Project* → import your repository.
3. Framework preset: **Other**. Build command: *(leave empty)*. Output directory: *(leave empty / `.`)*. Click **Deploy**.
4. Your store goes live at `https://<project>.vercel.app`. Add a custom domain under *Project → Settings → Domains*.

### Option B — GitHub Pages
1. Upload the files to a GitHub repository (as above).
2. *Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `(root)` → Save*.
3. After a minute the site is live at `https://<username>.github.io/<repository>/`.
   All links and image paths are relative, so it works from a sub-folder.

## 5. How ordering works
1. Customer adds products (with chosen colour and quantity) to the bag — saved in the browser (`localStorage`).
2. At **Checkout** they enter name, mobile number, full address, city, state and PIN (validated), review the exact message,
   then tap **Send Order on WhatsApp** (`https://wa.me/918789241790?text=…`).
3. The site clearly says the order is **not confirmed** until you confirm availability, price, shipping and delivery.

## 6. Project structure
```
index.html shop.html hijabs.html caps.html accessories.html new-arrivals.html
product.html cart.html checkout.html about.html contact.html
shipping.html delivery.html returns.html faq.html privacy.html terms.html
sitemap.xml robots.txt
assets/  css/style.css · js/app.js · js/products.js · products/*.jpg · hero.jpg · cat-*.jpg · story.jpg · og-image.jpg · favicon.svg
tools/   catalog.py · build_site.py (page generator) · gen_images.py (demo image renderer)
```

## 7. Tested
The shopping journey was tested in a real Chromium browser: home → shop (search, category, colour filter, sort) → product page
(colour swatches, quantity) → add to bag → refresh (bag persists) → bag (+/−/remove) → checkout validation → WhatsApp message
generation. All 18 product pages, 23 navigation/footer links, image loading and mobile (390 px) layout were checked with no
console errors. **Not tested:** actually sending a message through WhatsApp, and deployment to your own GitHub/Vercel account.

## 8. Notes
* Fonts (Cormorant Garamond, Inter) load from Google Fonts; the site falls back to Georgia / system fonts if offline.
* `tools/gen_images.py` regenerates the demo images; you do not need it once you have real photos.
