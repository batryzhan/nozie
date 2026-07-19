# Nozie Faultline Kit

Nozie is an autonomous AI DevOps agent: it catches a container crash, finds
the root cause, opens a fix PR in your GitHub repo, and — once you merge —
redeploys the container itself.

This kit spins up a tiny app with an **intentional bug** plus the Nozie
agent, so you can see the full loop in a couple of minutes:
**crash → AI investigation → fix PR → auto-redeploy**.

You need: Docker + Docker Compose, and a GitHub account.

---

## Setup (5 steps)

### 1. Sign up
Go to **https://nozie.xyz** and sign in with GitHub.

### 2. Get an API key
Dashboard → **Settings → API Keys** → create a key (starts with `nz_k_`).

Then, in this folder:
```bash
cp .env.example .env
```
Paste your key into `.env` as `NOZIE_API_KEY`. Nothing else in `.env` needs
to change — `NOZIE_DASHBOARD_URL` already defaults to `https://nozie.xyz`.

### 3. Push this folder to your own GitHub repo
Nozie needs a repo of yours to open the fix PR against:
```bash
# create an empty repo on GitHub, then:
git init && git add . && git commit -m "faultline demo"
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```
In the dashboard: connect GitHub, then **link this repo** to the `faultline`
container (the "Link repo" button next to it).

### 4. Start it
```bash
docker compose up -d --build
```
The `faultline` container shows up in the dashboard within ~30 seconds. If
it doesn't, see **Troubleshooting** below.

### 5. Break it (and watch Nozie fix it)
```bash
curl http://localhost:8081/crash
```
Now watch the dashboard: incident → AI investigation → fix PR. With
Auto-merge / Auto-restart turned on (Settings), Nozie merges the PR and
redeploys `faultline` from the fixed code by itself — `/crash` starts
returning `200`.

---

## Troubleshooting

**Container doesn't appear in the dashboard / agent logs say
`Nozie backend unreachable`:**
- Check `NOZIE_DASHBOARD_URL` in `.env` — it must be `https://nozie.xyz`
  (no `test.` prefix, no trailing slash).
- Check the agent's own logs: `docker logs faultline-agent`.
- Confirm your machine can reach the dashboard at all: `curl -I https://nozie.xyz`.

**No Telegram alerts:** email and the in-dashboard incident feed always
work; Telegram may not be reachable from every deployment — don't rely on
it as your only signal here.

**Start over:** `docker compose down`, then `docker compose up -d --build`
again re-introduces the bug and a fresh container.
