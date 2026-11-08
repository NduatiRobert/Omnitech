# Omnitech Systems website

A static website: plain HTML files that need no database or special hosting. The finished site is in `site/`. Upload the contents of that folder to your web host (cPanel, Netlify, Vercel, Cloudflare Pages, GitHub Pages and others all work).

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

After any change, run `python3 build.py`.

## SEO checklist after going live
1. Set your real domain in `SITE_URL` in `src/config.py`, then rebuild.
2. Add the site to Google Search Console, paste the verification code into `GOOGLE_SITE_VERIFICATION`, rebuild and upload, then submit `sitemap.xml`.
3. Create or claim your Google Business Profile, using the same name, phone number and address as on the website.
4. Optional: add a Google Analytics 4 ID in `GA_MEASUREMENT_ID`.
5. Publish one useful article every week and ask happy customers for Google reviews.
