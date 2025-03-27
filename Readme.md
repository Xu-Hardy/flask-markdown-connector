

# 📝 Markdown Connector API

A lightweight Flask-based Markdown API server that:

- 🧾 Recursively reads `.md` files in a directory
- ✨ Auto-fills missing frontmatter (title/date/summary/tags)
- 📦 Generates a searchable `index.json` for static sites
- 📂 Serves raw markdown files via API
- 📚 Provides Swagger UI for developers

---

## 🚀 Quick Start

### 1. Clone this project

```bash
git clone https://github.com/yourname/markdown-connector.git
cd markdown-connector
```

### 2. Place your `.md` files under the `markdown/` folder

```bash
mkdir markdown
cp your_posts/*.md markdown/
```

---

## 🐳 Run with Docker Compose

### docker-compose.yml

```yaml
version: "3"

services:
  flask-app:
    container_name: markdown-connector
    build: .
    ports:
      - "1313:5000"
    volumes:
      - ./markdown:/app/markdown
      - ./static:/app/markdown/static
    restart: always
```

### Start the service

```bash
docker-compose up --build
```

---

## 🧩 Project Structure

```
.
├── app.py               # Flask app with Swagger
├── requirements.txt
├── Dockerfile
├── start.sh
├── markdown/            # ← Your .md files go here
├── static/              # ← index.json will be generated here
└── docker-compose.yml
```

---

## 🌐 API Endpoints

| Endpoint              | Method | Description                            |
|-----------------------|--------|----------------------------------------|
| `/`                   | GET    | Health check                           |
| `/posts/`             | GET    | List all markdown files                |
| `/posts/<filename>`   | GET    | Get raw `.md` content                  |
| `/api/posts`          | GET    | Get `index.json` metadata              |
| `/api/refresh`        | GET    | Rebuild index (optional `?dryrun=true`)|
| `/index.json`         | GET    | Alias for `/api/posts`                |
| `/apidocs/`           | GET    | Swagger UI                             |

---

## 🧪 Sample `index.json` Output

```json
{
  "title": "My First Post",
  "summary": "",
  "tags": ["notes"],
  "category": "blog",
  "created": "2025-03-27T14:00:00",
  "url": "/posts/blog/first-post.md"
}
```

---

## 📚 Swagger UI

> Auto-generated docs available at:  
> 👉 `http://localhost:1313/apidocs/`

---

## 👨‍💻 Dev Tips

- `index.json` is auto-generated at server startup
- Missing frontmatter (like title, date, tags) will be filled in
- All `.md` files are served as raw markdown from `/posts/`

---

## 📦 Dependencies

```txt
flask
markdown
python-frontmatter
flasgger
```

---

## ❤️ License

MIT License. Fork & use freely. Contributions welcome!
