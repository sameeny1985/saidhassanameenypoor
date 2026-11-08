# Said hassan AMEENY POOR

Personal Portfolio Website

## Display name
**Said hassan AMEENY POOR**

## Technologies
- Python · Django
- PostgreSQL (Render) / SQLite (local)
- HTML · CSS (glassmorphism, dark theme)
- Google OAuth (admin only)
- Render + GitHub

## Website Sections
1. Articles
2. Websites
3. Videos
4. YouTube Channels
5. Telegram Channels

## Profile Photo
Place your personal photo here:

```
static/images/profile.jpg
```

(or `profile.png`)

Recommended size: **400×400 px to 800×800 px** (square).  
It will be displayed as a circular image (~200 px) on the homepage.

JPG or PNG both work.

## Contact
Email shown on site: **Shapyaarco@gmail.com**

## Admin Panel
URL: `/admin/`

- Only the Google account set in `ADMIN_EMAIL` can sign in.
- Session lasts 8 hours.
- All items (published + hidden) are listed so nothing is missing.
- Each item can have an optional **logo** uploaded from your computer (JPG/PNG).

## Logo field
When adding/editing an item you can upload a logo.  
It appears as a small image at the top of each card. Optional.

**Note for Render:** The free filesystem is ephemeral.  
Uploaded logos will be lost on redeploy unless you attach a **Persistent Disk**  
or use an external image host and paste the URL in the “Image URL” field instead.

## SEO
- Meta keywords & description cover many name variants  
  (English + Persian / سید حسن امینی پور …)
- Open Graph + Twitter cards
- JSON-LD Person schema
- robots.txt + sitemap.xml

## Environment Variables (Render)
```
SECRET_KEY=
DEBUG=False
SITE_URL=https://your-domain.onrender.com
ADMIN_EMAIL=your.google@email.com
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
DATABASE_URL=
```

## Google OAuth Callback
```
https://YOUR-DOMAIN/auth/google/callback/
```

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Deployment
1. Push to GitHub
2. Connect repo to Render Blueprint
3. Set environment variables
4. Deploy
5. Run migrations if needed
