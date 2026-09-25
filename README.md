# Gita Swasti — Portfolio

Personal portfolio website for Gita Swasti, a sustainability and social-impact program coordinator based in Bali, Indonesia.

It's a static site (plain HTML, CSS and JavaScript) with no build step.

## Structure

```
index.html                     Page content
styles.css                     Styles, including light/dark themes and responsive layout
script.js                      Theme toggle, mobile menu, scroll animations
assets/                        Photos and the downloadable CV
assets/fonts/                  JHC Rasbora, Type Machine and Jost, with their license files
```

## Run locally

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploy with GitHub Pages

1. Push to GitHub.
2. In the repository, go to **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select the branch (e.g. `main`) and the `/ (root)` folder, then save.
4. The site will be published at `https://<username>.github.io/<repository>/`.

## Updating content

All text lives in `index.html`, one `<section>` per block: intro, journey, wins, practice areas, experience, works, writing, skills, honors, volunteering, education and contact. To add a role, copy one `<article class="job reveal">` block in Experience and edit it. To replace the CV, overwrite the file in `assets/` and keep the same name, or update the two links that point to it.
