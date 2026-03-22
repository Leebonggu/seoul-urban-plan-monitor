import os

WP_URL = os.environ.get("WP_URL", "")           # e.g. https://your-site.wordpress.com
WP_USER = os.environ.get("WP_USER", "")          # WordPress 사용자명
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")  # Application Password
WP_API_BASE = f"{WP_URL}/wp-json/wp/v2"

def validate_config():
    missing = []
    if not WP_URL:
        missing.append("WP_URL")
    if not WP_USER:
        missing.append("WP_USER")
    if not WP_APP_PASSWORD:
        missing.append("WP_APP_PASSWORD")
    if missing:
        raise EnvironmentError(f"Missing env vars: {', '.join(missing)}")
