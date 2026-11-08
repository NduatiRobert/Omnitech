# Omnitech Systems website

A static website: plain HTML files that need no database or special hosting. The finished site is in `site/`. Upload the contents of that folder to your web host (cPanel, Netlify, Vercel, Cloudflare Pages, GitHub Pages and others all work).

## Deploying on Coolify (VPS)
The repository includes a `Dockerfile`. It runs `build.py`, then serves the site with nginx, using compression, caching, short addresses without `.html` (`/cctv-installation`) and the custom 404 page.

1. Push this folder to a GitHub repository (private is fine).
2. In Coolify, go to **Project → + New → Resource** and choose **Private Repository (with GitHub App)**, or **Public Repository**.
3. Select the repository and the `main` branch, and set **Build Pack** to **Dockerfile**.
4. Under **Domains**, enter `https://omnitechsystems.co.ke,https://www.omnitechsystems.co.ke`. Coolify issues the SSL certificates. Then set **Redirect** to *Redirect to non-www* so Google sees one version.
5. Make sure the DNS **A records** for `@` and `www` point to your VPS IP.
6. Set **Ports Exposes** to `80`, then click **Deploy**.
7. Turn on **Auto Deploy** (it's on by default with the GitHub App). Every push to `main` then updates the live site within a minute or two.

### Publishing a blog article from your phone (no computer needed)
On GitHub, open the `blog` folder and choose **Add file → Create new file**. Name it `YYYY-MM-DD-title.md`, paste the template from `_TEMPLATE.md`, write the article, then **Commit**. Coolify rebuilds and publishes it automatically. To add a photo, upload it to `blog/images` the same way.

### Scheduled articles (optional)
Articles with a future date appear on the first rebuild on or after that date. `.github/workflows/daily-rebuild.yml` triggers a rebuild every morning. To turn it on, add these two repository secrets on GitHub (**Settings → Secrets and variables → Actions**):
- `COOLIFY_WEBHOOK`: the Deploy Webhook URL from your Coolify app's **Webhooks** tab
- `COOLIFY_TOKEN`: a Coolify API token with deploy permission (**Keys & Tokens → API tokens**)

## Pages
- `index.html`: home page
- `services.html` and one page per service, each with its own FAQs
- `blog.html`: blog list (page 2, 3 and so on are added automatically, 9 articles per page)
- `blog/<article>.html`: one page per article
- `contact.html`, `privacy-policy.html`, `terms-and-conditions.html`, `404.html`
- `sitemap.xml`, `robots.txt`, `feed.xml` (RSS): created automatically for Google

## Publishing a blog article (weekly)
1. Copy `blog/_TEMPLATE.md` and rename the copy to `YYYY-MM-DD-short-title.md`, e.g. `2026-11-15-cctv-for-schools.md`.
2. Fill in the title, date, description, category and related service at the top of the file.
3. Write the article using `##` for headings, `-` for bullet points and `[text](page.html)` for links.
4. To include a photo, put it in `blog/images/` and add `image: images/photo.jpg` at the top of the file.
5. Delete the `draft: true` line, then run:

   ```bash
   python3 build.py
   ```

6. Upload the updated `site/` folder to your host.

Articles with a future date stay hidden until that date, so you can write several weeks ahead. They appear the next time you run the build on or after that date.

The build adds each new article to the blog page, the home page ("From the blog"), its related service page, the sitemap and the RSS feed.

## Editing everything else
| What | File |
| --- | --- |
| Phone, email, location, hours, domain, social links, Google IDs | `src/config.py` |
| Service pages, FAQs and home page text | `src/content.py` |
| Privacy Policy, Terms and Conditions | `src/pages/*.md` |
| Colours and fonts | top of `site/assets/css/styles.css` |
| Hero pictures | put a photo in `site/assets/img/hero/` named after the page, e.g. `home.jpg`, `cctv-installation.jpg`, `zoho-consulting.webp` (4:3, about 1280 × 960 px). It replaces that page's illustration automatically. |

After any change, run `python3 build.py`.

## SEO checklist after going live
1. Set your real domain in `SITE_URL` in `src/config.py`, then rebuild.
2. Add the site to Google Search Console, paste the verification code into `GOOGLE_SITE_VERIFICATION`, rebuild and upload, then submit `sitemap.xml`.
3. Create or claim your Google Business Profile, using the same name, phone number and address as on the website.
4. Optional: add a Google Analytics 4 ID in `GA_MEASUREMENT_ID`.
5. Publish one useful article every week and ask happy customers for Google reviews.
