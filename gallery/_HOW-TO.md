# Adding photos to the gallery

Each album is a folder in this `gallery/` folder. Name the folder with the date and a short title:

    2026-11-15-montana-mall-site-visit
    2026-11-20-thika-school-cctv-installation

## Add an album on GitHub (phone or computer)
1. Open the `gallery` folder and choose **Add file → Upload files**.
2. Drag in your photos. At the top, type the new folder name followed by `/`
   (e.g. `2026-11-15-montana-mall-site-visit/`) so the photos go into a new folder.
3. Click **Commit changes**. The site rebuilds and the album appears, newest first.

Phone photos are fine: they are resized and rotated correctly automatically.
Photos appear in file-name order, so you can number them `01-...jpg`, `02-...jpg`.

## Optional extras (inside the album folder)
`album.md` sets the title, category, location and a short description:

    ---
    title: Site visit at Montana Mall
    category: Site visits
    location: Nairobi CBD
    description: One sentence shown on Google.
    ---
    A short paragraph about the visit (optional).

- **category:** use the same few words each time, e.g. `Projects`, `Site visits`, `Team`, `Events`.
  Each category becomes a filter button on the Gallery page.
- **cover:** `cover: 03-photo.jpg` picks the album's main photo (otherwise the first photo).
- **draft:** `draft: true` hides the album.

`captions.txt` adds captions shown in the full-screen viewer, one per line:

    01-gate.jpg: Installing the gate camera
    02-nvr.jpg: 16-channel recorder in the server room

Without `album.md` the title comes from the folder name and the category is "Projects".

## Delete an album
Delete its folder. To remove the sample, delete `2026-11-08-sample-site-visit`.

Always get the client's permission before posting photos of their premises,
and avoid photos that show screens with live footage, people's faces, or security weak points.
