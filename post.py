#!/usr/bin/env python3
"""IRONPEAK social robot - posts the day's scheduled post to Facebook and Instagram.

Runs on GitHub Actions (see .github/workflows/daily-post.yml). Uses only the Python
standard library. Edit social/posts.json to change what gets posted and
social/config.json to change settings. See social/SETUP.md.
"""
import argparse, datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
POSTS = json.load(open(os.path.join(HERE, "posts.json"), encoding="utf-8"))


def now_local():
    tz = datetime.timezone(datetime.timedelta(hours=CFG.get("timezone_offset_hours", 2)))
    return datetime.datetime.now(tz)


def choose_post(now, forced_id=None):
    """Pick today's post. Same date+slot always gives the same post; the queue loops."""
    if forced_id:
        for p in POSTS:
            if str(p["id"]) == str(forced_id):
                return p
        raise SystemExit(f"No post with id {forced_id} in posts.json")
    per = 2 if CFG.get("posts_per_day", 1) >= 2 else 1
    start = datetime.date.fromisoformat(CFG["start_date"])
    days = max((now.date() - start).days, 0)
    slot = 0 if per == 1 else (0 if now.hour < 13 else 1)
    return POSTS[(days * per + slot) % len(POSTS)]


def caption_for(post, platform):
    phone = CFG["phone"]
    link = f"🌐 {CFG['website_url']}" if platform == "facebook" else "🔗 Link in bio"
    tags = " ".join("#" + t.lstrip("#") for t in post.get("tags", []))
    return f"{post['text']}\n\n📞 Call / WhatsApp {phone}\n{link}\n\n{tags}".strip()


def image_url(post):
    base = (os.environ.get("SITE_BASE") or CFG["site_base"]).rstrip("/")
    return f"{base}/social/images/{post['image']}"


def graph_base():
    return os.environ.get("GRAPH_BASE") or f"https://graph.facebook.com/{CFG['graph_version']}"


def api(method, url, params):
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        url, data = url + "?" + data.decode(), None
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} from {url.split('?')[0]}: {e.read().decode()[:400]}")


def check_image(url):
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ctype = r.headers.get("Content-Type", "")
            if r.status != 200 or not ctype.startswith("image/jpeg"):
                raise RuntimeError(f"Image not usable ({r.status}, {ctype}): {url}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Image not reachable yet: {url} ({e}). Has the site finished publishing?")


def post_facebook(post, page_id, token):
    res = api("POST", f"{graph_base()}/{page_id}/photos",
              {"url": image_url(post), "caption": caption_for(post, "facebook"),
               "published": "true", "access_token": token})
    return res.get("post_id") or res.get("id")


def post_instagram(post, ig_id, token):
    c = api("POST", f"{graph_base()}/{ig_id}/media",
            {"image_url": image_url(post), "caption": caption_for(post, "instagram"),
             "access_token": token})
    cid = c["id"]
    for _ in range(12):
        st = api("GET", f"{graph_base()}/{cid}", {"fields": "status_code", "access_token": token})
        code = st.get("status_code")
        if code == "FINISHED":
            break
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Instagram could not process the image (status {code})")
        time.sleep(5)
    res = api("POST", f"{graph_base()}/{ig_id}/media_publish",
              {"creation_id": cid, "access_token": token})
    return res.get("id")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="show what would be posted, post nothing")
    ap.add_argument("--post-id", help="post this id from posts.json instead of today's")
    a = ap.parse_args()
    dry = a.dry_run or os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")
    forced = a.post_id or os.environ.get("POST_ID") or None

    now = now_local()
    post = choose_post(now, forced)
    page, ptoken, ig = (os.environ.get(k, "").strip() for k in ("FB_PAGE_ID", "FB_PAGE_TOKEN", "IG_USER_ID"))
    plan = []
    if "facebook" in CFG["platforms"]:
        plan.append(("facebook", bool(page and ptoken)))
    if "instagram" in CFG["platforms"]:
        plan.append(("instagram", bool(ig and ptoken)))

    print(f"[{now:%Y-%m-%d %H:%M} Namibia time] Post #{post['id']} ({post['image']})")
    print("Image:", image_url(post))
    if not any(ok for _, ok in plan):
        dry = True
        print("No credentials found - running as a dry run.")
    errors = []
    if not dry:
        try:
            check_image(image_url(post))
        except RuntimeError as e:
            print("ERROR:", e); sys.exit(1)
    for name, ok in plan:
        print(f"\n--- {name.upper()} ---\n{caption_for(post, name)}\n")
        if dry:
            print("(dry run - not posted)"); continue
        if not ok:
            print(f"Skipped: {name} credentials not set."); continue
        try:
            rid = post_facebook(post, page, ptoken) if name == "facebook" else post_instagram(post, ig, ptoken)
            print(f"Posted to {name}: {rid}")
        except Exception as e:  # keep going so one platform can't block the other
            errors.append(f"{name}: {e}"); print(f"FAILED on {name}: {e}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"### Post #{post['id']}\n" + ("\n".join(f"- ❌ {e}" for e in errors) or "- ✅ done" if not dry else "- dry run") + "\n")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
