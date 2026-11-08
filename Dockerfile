# ---- Stage 1: build the static site from the Markdown/Python sources
FROM python:3.12-slim AS build
WORKDIR /app
# Pillow resizes portfolio photos and draws the social share image; DejaVu provides its font
# (both optional: if either install fails, the site still builds, just without those extras)
RUN (apt-get update && apt-get install -y --no-install-recommends fonts-dejavu-core \
     && rm -rf /var/lib/apt/lists/*) || echo "fonts skipped"; \
    pip install --no-cache-dir pillow==11.0.0 || echo "pillow skipped"
COPY . .
RUN python3 build.py

# ---- Stage 2: serve it with nginx
FROM nginx:1.27-alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/site /usr/share/nginx/html
EXPOSE 80 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
