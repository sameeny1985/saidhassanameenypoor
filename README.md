# Said Hassan Ameeny Poor

Personal Portfolio Website

## Technologies

- Python
- Django
- PostgreSQL
- HTML
- CSS
- Google OAuth
- Render
- GitHub

## Website Sections

1. Articles
2. Websites
3. Videos
4. Telegram Channels

## Admin Panel

/admin/

Google OAuth authentication is required.

Only the verified email configured in ADMIN_EMAIL
can access the management panel.

## Deployment

1. Upload project files to GitHub.
2. Connect GitHub repository to Render.
3. Create a Render Blueprint.
4. Configure environment variables.
5. Deploy.

## Google OAuth Callback

https://YOUR-DOMAIN/auth/google/callback/

## Environment Variables

SECRET_KEY
DEBUG
SITE_URL
ADMIN_EMAIL
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
DATABASE_URL

## Database

PostgreSQL on Render.

SQLite fallback for local development.
