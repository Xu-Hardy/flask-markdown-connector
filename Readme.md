
# 🐳 flask-demo

[![Docker Image CI](https://github.com/Xu-Hardy/flask-demo/actions/workflows/docker.yml/badge.svg)](https://github.com/Xu-Hardy/flask-demo/actions/workflows/docker.yml)

A minimal, production-ready Flask app containerized with Docker.  
Supports both **x86_64** and **ARM64** platforms via Docker Buildx.  
Images are automatically published to Docker Hub on every git tag push.

---

## 🚀 Quick Start

### Pull from Docker Hub

```bash
docker pull cloudsmithy/flask-markdown-connector:latest
```

### Run the container

```bash
docker run -d --name markdown-connector \
  -p 5000:5000 \
  -v "$(pwd):/app/markdown" \
  --restart always \
  cloudsmithy/flask-markdown-connector
```

Then open your browser at [http://localhost:5000](http://localhost:5000)

---

## 🧱 Docker Compose

```yaml
services:
  markdown-connector:
    image: cloudsmithy/flask-markdown-connector
    container_name: markdown-connector
    ports:
      - "5000:5000"
    volumes:
      - ./markdown:/app/markdown
    restart: always

```

Start it:

```bash
docker-compose up -d
```

---

## 🌍 Multi-Architecture Support

This image supports the following platforms:

| Architecture | Status |
|--------------|--------|
| `linux/amd64`| ✅     |
| `linux/arm64`| ✅     |

Built using Docker Buildx and QEMU in GitHub Actions.

---

## 🔧 GitHub Actions CI

This project includes a CI pipeline that:

- Triggers on `git push` with tags like `v1.0.0`
- Builds the image for both amd64 and arm64
- Pushes **both version tag and `latest`** to Docker Hub

### To trigger a build:

```bash
git tag v1.0.0
git push origin v1.0.0
```

This will publish:

- `cloudsmithy/cloudsmithy/flask-markdown-connector:v1.0.0`
- `cloudsmithy/cloudsmithy/flask-markdown-connector:latest`

---

## 🔐 Docker Hub Authentication

To enable publishing in GitHub Actions, define the following secrets:

| Name              | Description                   |
|-------------------|-------------------------------|
| `DOCKER_USERNAME` | Your Docker Hub username      |
| `DOCKER_PASSWORD` | Your Docker Hub Access Token  |

Add them under **GitHub → Settings → Secrets → Actions**.


## APIs

### 🔹 `GET /`

**Function**: Returns service startup message  
**Description**: Used to check if the service is running properly  
**Example Response**:
```json
{ "message": "Markdown Connector is running." }
```

---

### 🔹 `GET /api/posts`

**Function**: Retrieve the generated `index.json` (cached version)  
**Description**: Returns a list of Markdown file paths and metadata, read from cache for fast response  
**Use Case**: Can be used by Coco Server as the entry point for loading the index  
**Example Response**:
```json
[
  {
    "title": "Docker Study Notes",
    "path": "dev/docker.md",
    "tags": ["docker", "study"],
    "created": "2024-11-22"
  },
  ...
]
```

---

### 🔹 `GET /index.json`

**Function**: Render the current Markdown directory structure in real-time  
**Description**: Equivalent to `/api/posts`, but reads files in real-time instead of using cache; suitable for debugging or manual use  
**Use Case**: Use when the latest data is required

---

### 🔹 `GET /api/refresh`

**Function**: Re-scan and regenerate the latest `index.json` cache  
**Description**: Used to force refresh the directory index, especially after new/updated Markdown files  
**Example Response**:
```json
{ "message": "Index cache refreshed." }
```

---

### 🔹 `GET /posts/`

**Function**: List Markdown file paths (without metadata)  
**Description**: Returns all accessible Markdown file paths, useful for building dropdowns or quick navigation  
**Example Response**:
```json
[
  "notes/linux.md",
  "dev/docker.md",
  "ideas/gpt-agent.md"
]
```

---

### 🔹 `GET /posts/{filename}`

**Function**: Get the content of a specified Markdown file  
**Parameter**:
- `{filename}`: The relative path of the Markdown file (within the mounted directory)  

**Use Case**: Used to display specific note content after clicking in the frontend  
**Example Response**:
```json
{
  "filename": "dev/docker.md",
  "content": "# Docker Study Notes\n\n## Container vs Image ..."
}
```

---

Let me know if you'd like this formatted into a Markdown doc or OpenAPI spec!
---

## 👤 Maintainer

Made with ❤️ by [cloudsmithy](https://hub.docker.com/u/cloudsmithy)  
PRs and Issues welcome!
