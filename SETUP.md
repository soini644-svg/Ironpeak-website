# IRONPEAK Social Robot — Setup Guide

## What it does (and does not do)

| Platform | Automatic? |
|---|---|
| **Facebook Page** | ✅ Yes — posts a picture + caption twice a day (09:00 and 18:00 Namibia time) |
| **Instagram** (Business/Professional account) | ✅ Yes — same posts |
| **TikTok** | ❌ Not by robot. TikTok only lets *approved* apps post publicly; an unapproved app's posts are visible only to you. The approval review takes weeks. Use TikTok's own scheduler with the ready-made pictures and captions (Part 7). |
| WhatsApp, LinkedIn, X, others | ❌ Manual / scheduling tools (Part 7) |

It runs free on GitHub, even when your computer is off. It posts only to **your own** pages, using Facebook's official system — so it is allowed and your accounts stay safe.

The queue has **33 ready posts** (every service, packages, CEO, contact). At 2 per day they last ~16 days, then repeat. Edit them any time (Part 6).

---

## Part 1 — Put the robot on GitHub (about 10 minutes)

1. Unzip `IRONPEAK_Social_Robot.zip` on your computer.
2. Open your repo: `github.com/soini644-svg/Ironpeak-website`.
3. **Add file → Upload files.** Drag the whole **`social`** folder into the box (it contains `post.py`, `posts.json`, `config.json` and an `images` folder). Click **Commit changes**.
4. Create the schedule file (do this part by typing — hidden folders don't upload well):
   - **Add file → Create new file**
   - In the name box type exactly: `.github/workflows/daily-post.yml` (typing each `/` makes the folders)
   - Open `COPY_THIS_daily-post.yml` from the zip in Notepad, copy everything, paste it in the big box.
   - Click **Commit changes**.
5. Wait 2 minutes, then open this in your browser — you should see a picture:
   `https://soini644-svg.github.io/Ironpeak-website/social/images/welcome.jpg`
   (If it says 404, wait a few more minutes. The robot cannot post until pictures open.)

## Part 2 — Facebook Page and Instagram

1. You need a **Facebook Page** for the business (not your personal profile). Create one at facebook.com/pages/create if you don't have it.
2. You need an **Instagram Professional (Business) account**. In the Instagram app: Settings → Account type and tools → Switch to professional account → Business.
3. **Link Instagram to the Facebook Page** (Instagram app → Edit profile → Page, or Facebook Page → Settings → Linked accounts). Instagram posting by robot does not work without this link.

## Part 3 — Get your access keys (the fiddly part — go slowly)

Meta changes menu names often; if a button has moved, search for the name shown here.

1. Go to **developers.facebook.com**, log in with the Facebook account that manages the Page, and accept the developer terms.
2. **Create App** → choose the business/Pages option → give it a name like "IRONPEAK Poster". Leave it in **Development mode**.
3. Open **App settings → Basic**. Note the **App ID** and **App Secret** (click Show). *Treat the secret like a password.*
4. Open **Tools → Graph API Explorer** (developers.facebook.com/tools/explorer).
   - Choose your app.
   - Under Permissions add: `pages_show_list`, `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`, `business_management`.
   - Click **Generate Access Token**. When asked, tick your **Page** and your **Instagram account**, then continue.
   - Copy the token (it only lasts about an hour — we make it long-lasting next).
5. Make it long-lasting. Paste this in your browser address bar, replacing the three capital words, and press Enter:
   `https://graph.facebook.com/v26.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN`
   Copy the `access_token` it shows (long-lived user token).
6. Get your Page keys:
   `https://graph.facebook.com/v26.0/me/accounts?access_token=LONG_USER_TOKEN`
   Find your Page in the list:
   - its **`id`** = your **FB_PAGE_ID**
   - its **`access_token`** = your **FB_PAGE_TOKEN** (a Page token made this way does not expire)
7. Get your Instagram key:
   `https://graph.facebook.com/v26.0/PAGE_ID?fields=instagram_business_account&access_token=PAGE_TOKEN`
   The number after `"instagram_business_account": {"id":` = your **IG_USER_ID**.

You now have three values: **FB_PAGE_ID**, **FB_PAGE_TOKEN**, **IG_USER_ID**.

> If Meta says you must complete "Page Publishing Authorization", do that on the Page first. If it says a permission needs *App Review*, the free alternative is **Meta Business Suite's scheduler** (Part 7) — it needs no keys.

## Part 4 — Give the keys to the robot (safely)

In your repo: **Settings → Secrets and variables → Actions → New repository secret**. Create three secrets with these exact names and paste the values:

- `FB_PAGE_ID`
- `FB_PAGE_TOKEN`
- `IG_USER_ID`

Never paste these into your website, posts.json, or send them to anyone. GitHub hides them from everyone, including the logs.

## Part 5 — Test it

1. Repo → **Actions** tab → **Daily social posts** → **Run workflow**.
2. First tick **Dry run** → Run. Open the finished run: it shows exactly what would be posted.
3. Run again with **Dry run** unticked and type `1` in *post_id* → it posts the Welcome post. Check your Facebook Page and Instagram.
4. If it works, you're done. From now on it posts at 09:00 and 18:00 automatically. If a post fails, GitHub emails you.

## Part 6 — Everyday changes

- **Edit a caption / add a post:** repo → `social` → `posts.json` → pencil icon → edit → Commit. Each post has `id`, `image`, `text`, `tags`.
- **New picture:** must be a **JPEG (.jpg)**, ideally 1080×1080. Instagram rejects PNG. Upload it to `social/images/` and use its name in posts.json.
- **Posts per day:** `social/config.json` → `"posts_per_day": 1` or `2`.
- **Times:** in `.github/workflows/daily-post.yml` change the `cron` lines. They use UTC; Namibia is UTC+2 (so 07:00 UTC = 09:00 Namibia).
- **Start date:** `config.json` → `start_date`.
- **Pause everything:** Actions → Daily social posts → ⋯ → Disable workflow.
- If prices or services change, update **posts.json and the website** so they match.
- Check each caption before launch — especially prices and the registration number. Verify your registration with BIPA before advertising it as a compliance claim.

## Part 7 — TikTok and the other platforms

**TikTok (manual, ~10 minutes a week):**
1. On a computer open **TikTok Studio** (tiktok.com/tiktokstudio) and use *Upload / Schedule* to line up posts ahead of time.
2. Use the pictures in `social/images/` as photo posts, with captions copied from `posts.json`.
3. For better reach later, short videos (6–15 seconds) work best — ask and I can make video versions of these pictures.

**Facebook + Instagram without keys:** **Meta Business Suite** (business.facebook.com) has a free *Schedule post* tool for both. Use it if Part 3 is too much.

**Other platforms:** WhatsApp Status, LinkedIn page, X — post manually or with a scheduling tool such as Buffer or Later (plans and prices change; check their sites).

**Please do NOT use** "growth bots" that auto-follow, auto-like, auto-comment or message strangers, or tools that spam Facebook groups. They break the platforms' rules and get business accounts banned.

## Troubleshooting

| Message | Meaning / fix |
|---|---|
| `Image not reachable yet` | The site hasn't published the pictures yet. Open the `welcome.jpg` link from Part 1; wait until it shows. |
| `Invalid OAuth access token` | Token wrong or expired. Repeat Part 3 and update the secret. |
| `(#200)` / `permission` error | A permission wasn't ticked in Part 3 step 4. Generate a new token with all permissions. |
| Instagram `media type not supported` | The picture isn't a plain JPEG. Re-save as .jpg. |
| Facebook works, Instagram fails | Instagram isn't Business/Professional or isn't linked to the Page (Part 2). |
| Robot stopped after months | GitHub pauses idle repos; the weekly keep-alive prevents this. Check Actions → enable the workflow. |
| Limits | Instagram allows up to 100 API posts per day; 2 a day is far below it. |
