---
title: Your article title (aim for 50-60 characters, include the main keyword)
date: 2026-11-15
description: One or two sentences (about 150 characters) that appear on Google under your title.
category: CCTV & Security
service: cctv-installation
author: Omnitech Systems Team
image:
draft: true
---

HOW TO PUBLISH A NEW ARTICLE
1. Copy this file and rename it, e.g. 2026-11-15-my-article-title.md
   (the part after the date becomes the web address: my-article-title.html)
2. Fill in the details between the --- lines above:
   - category: one of  CCTV & Security | Internet & Networking | Hotspot Business |
     Websites | Software | Digital Marketing | Automation | Zoho | Business Tips
   - service: the related service page (cctv-installation, internet-installation,
     hotspot-business, website-development, software-development, digital-marketing,
     business-automation, zoho-consulting). A link to it appears on the article,
     and the article appears on that service page.
   - image: optional. Put the photo in blog/images/ and write e.g. images/my-photo.jpg
   - draft: true hides the article. Delete that line (or set false) to publish.
   - A date in the future keeps the article hidden until that date (rebuild on the day).
3. Write the article below, then run:  python3 build.py

Writing tips for Google ranking:
- Use ## for main section headings and ### for sub-headings.
- Answer one clear question per article, the way customers would search for it.
- Link to your service pages, e.g. [CCTV installation](cctv-installation.html).
- 800-1,500 words works well. Keep paragraphs short.

## Example heading

Normal paragraph text. **Bold text**, *italic text* and a [link](contact.html).

- Bullet point one
- Bullet point two

1. Numbered step one
2. Numbered step two

> A highlighted quote or tip.

![Description of the photo for Google](images/example.jpg)
