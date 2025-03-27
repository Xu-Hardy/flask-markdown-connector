
# 🐳 flask-demo

[![Docker Image CI](https://github.com/Xu-Hardy/flask-demo/actions/workflows/docker.yml/badge.svg)](https://github.com/Xu-Hardy/flask-demo/actions/workflows/docker.yml)

A minimal, production-ready Flask app containerized with Docker.  
Supports both **x86_64** and **ARM64** platforms via Docker Buildx.  
Images are automatically published to Docker Hub on every git tag push.

---

## 🚀 Quick Start

### Pull from Docker Hub

```bash
docker pull cloudsmithy/flask-demo:latest
```

### Run the container

```bash
docker run -p 5000:5000 cloudsmithy/flask-demo:latest
```

Then open your browser at [http://localhost:5000](http://localhost:5000)

---

## 🧱 Docker Compose

```yaml
services:
  flask-app:
    image: cloudsmithy/flask-demo:latest
    ports:
      - "5000:5000"
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

- `cloudsmithy/flask-demo:v1.0.0`
- `cloudsmithy/flask-demo:latest`

---

## 🔐 Docker Hub Authentication

To enable publishing in GitHub Actions, define the following secrets:

| Name              | Description                   |
|-------------------|-------------------------------|
| `DOCKER_USERNAME` | Your Docker Hub username      |
| `DOCKER_PASSWORD` | Your Docker Hub Access Token  |

Add them under **GitHub → Settings → Secrets → Actions**.

---

## 🧪 Sample Output

```bash
Hello from multi-arch Flask Docker in production mode!
```

---

## 👤 Maintainer

Made with ❤️ by [cloudsmithy](https://hub.docker.com/u/cloudsmithy)  
PRs and Issues welcome!
