# ---- Stage 1: build the static site from the Markdown/Python sources
FROM python:3.12-slim AS build
WORKDIR /app
COPY . .
RUN python3 build.py

# ---- Stage 2: serve it with nginx
FROM nginx:1.27-alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/site /usr/share/nginx/html
EXPOSE 80 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
