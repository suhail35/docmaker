# Инструкция по подготовке файлов для production (офлайн-режим)

## Bootstrap 5

Скачайте и распакуйте в `app/static/`:

```bash
curl -fsSL https://github.com/twbs/bootstrap/releases/download/v5.3.3/bootstrap-5.3.3-dist.zip -o /tmp/bootstrap.zip
unzip /tmp/bootstrap.zip -d /tmp/bootstrap
cp /tmp/bootstrap/bootstrap-5.3.3/dist/css/bootstrap.min.css app/static/css/
cp /tmp/bootstrap/bootstrap-5.3.3/dist/js/bootstrap.bundle.min.js app/static/js/
```

Затем в `app/templates/*.html` замените CDN-ссылки на локальные:
- `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css` → `/static/css/bootstrap.min.css`
- `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js` → `/static/js/bootstrap.bundle.min.js`

## Шрифт PT Sans

1. Перейдите на https://www.fontsquirrel.com/fonts/pt-sans
2. Нажмите "Download" → "Webfont Kit"
3. Извлеките `PTSans-Regular.ttf` и `PTSans-Bold.ttf` в `app/static/fonts/`
4. Добавьте в `app/static/css/main.css`:

```css
@font-face {
    font-family: 'PT Sans';
    src: url('/static/fonts/PTSans-Regular.ttf') format('truetype');
    font-weight: normal;
}
@font-face {
    font-family: 'PT Sans';
    src: url('/static/fonts/PTSans-Bold.ttf') format('truetype');
    font-weight: bold;
}
```

## Проверка

После подготовки файлов запустите:

```bash
docker compose up --build
```

Откройте http://localhost:8080 — всё должно работать без интернета.
