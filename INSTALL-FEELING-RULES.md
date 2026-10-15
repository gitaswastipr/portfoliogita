# Feeling Rules portfolio update

Prepared from the publicly served portfolio on 15 October 2026 and verified against
https://github.com/gitaswastipr/portfoliogita. The repository HTML and CSS matched
the downloaded live source byte-for-byte.

The default branch checked was claude/portfolio-website-rul53o.
The live website and GitHub repository have not been changed.

## What changed

- Dedicated Feeling Rules section before the existing writing section.
- Navigation, biography and contact links to Feeling Rules.
- Article preview with original title, subtitle, publication date, opening excerpt,
  photograph and photographer attribution, and a Continue reading link to Substack.
- Subscribe and Browse the archive links.
- Existing experience, projects, Medium links, Nuturang links and other sections preserved.
- Responsive design using your current blush palette, fonts and light/dark themes.

The public archive returned one article when checked. All currently returned
public archive articles are included. Drafts and private posts are outside scope.
Continue reading opens the original article on Substack in a new tab; Substack
controls access to full text, including any subscription restrictions.

## Publish with automatic article refreshes (recommended)

1. Extract the ZIP on your computer.
2. Open https://github.com/gitaswastipr/portfoliogita and select the
   claude/portfolio-website-rul53o branch.
3. Click Add file -> Upload files. Upload all contents of the extracted folder,
   keeping the folder paths, including .github/workflows/feeling-rules-pages.yml.
4. Commit the changes. Keep the existing script.js, .nojekyll, fonts and other assets.
5. Go to Settings -> Pages. Under Build and deployment, set Source to GitHub Actions.
6. Open Actions -> Publish portfolio with Feeling Rules -> Run workflow.
7. After the build and deployment succeed, check your portfolio URL.

The included workflow refreshes all public article previews before publishing,
when you commit to the current default branch, run it manually, and approximately
every six hours. Scheduled runs can be delayed or disabled by GitHub; they are
not instant. The scheduled workflow must be on the default branch. If the branch
changes, update the workflow push filter.

The workflow uses the existing root-level static site and publishes through
GitHub Pages. It needs Pages deployment permissions, not a personal access token.
Its refreshed article list is published in the Pages artifact rather than
committed back into the repository. A failed article refresh produces a warning
and publishes the checked-in previews.

The workflow has been prepared locally, not uploaded, enabled or executed on
GitHub. The current Pages setting cannot be determined from the public source.
Repository policies or environment approvals may require owner action.

## Publish the static update using your existing method

1. Open the GitHub repository that publishes your portfolio.
2. Find the folder containing the existing index.html, styles.css and script.js.
   Depending on your Pages setup, it may be the repository root or a docs folder.
3. Back up the current files or use a Git branch. If changes have been made since
   15 October 2026, merge the Feeling Rules additions instead of overwriting them.
4. Replace index.html and styles.css in that folder with the provided versions.
5. Add assets/feeling-rules/, scripts/update_feeling_rules.py and
   feeling-rules-posts.json, preserving their relative paths.
6. Keep your existing script.js, fonts, images, CV and remaining assets unchanged.
7. Commit to the branch/folder configured for GitHub Pages and use your existing
   publishing process. Check the updated site after the deployment completes.

This ZIP is an update package, not a complete standalone copy of your website.
It intentionally omits unchanged assets and script.js.

## Refresh after publishing another article

Run in the website folder with Python 3 available:

    python scripts/update_feeling_rules.py

The script fetches the public Substack archive in pages, updates the article
cards and downloads cover images. Commit the updated index.html,
feeling-rules-posts.json and assets/feeling-rules/ and republish the website.
For the featured example, the original opening excerpt and photo credit are
included. Other articles receive their title, subtitle, date and reading link.

The refresh script is included and tested. The optional scheduled publishing
workflow is included under .github/workflows/, but is not installed or enabled
until you upload the files and configure GitHub Pages as described above.

The public archive endpoint is unofficial and could change. If a refresh fails,
the last successful HTML is retained. Browser-side requests to Substack and
third-party RSS proxies are not needed; previews work with JavaScript disabled.

## Verification

- One current public article fetched from the paginated archive.
- Original main portfolio sections preserved.
- Continue reading points to the supplied article.
- Desktop (1440px), mobile (390px) and desktop dark-mode preview checked.
- No JavaScript page errors or horizontal overflow in the tested layouts.
