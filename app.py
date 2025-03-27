import os
import json
import datetime
import markdown
import frontmatter
from urllib.parse import unquote
from flask import Flask, jsonify, send_file, request, send_from_directory, abort
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

POSTS_DIR = "/app/markdown"
OUTPUT_FILE = f"{POSTS_DIR}/static/index.json"


# 递归查找所有 .md 文件
def find_markdown_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files


# 自动补全 frontmatter，如果 dry_run=True 则不写入
def parse_and_fix_markdown(filepath, dry_run=False):
    post = frontmatter.load(filepath)
    changed = False
    now = datetime.datetime.now().isoformat()
    filename = os.path.splitext(os.path.basename(filepath))[0]

    if not post.metadata:
        post.metadata = {}
        changed = True

    if "title" not in post.metadata:
        post.metadata["title"] = filename
        changed = True
    if "date" not in post.metadata:
        post.metadata["date"] = now
        changed = True
    if "summary" not in post.metadata:
        post.metadata["summary"] = ""
        changed = True

    if "category" not in post.metadata or "tags" not in post.metadata:
        rel_path = os.path.relpath(filepath, POSTS_DIR)
        slug = os.path.splitext(rel_path)[0].replace("\\", "/")
        parts = slug.split("/")

        if "category" not in post.metadata:
            post.metadata["category"] = parts[0] if len(parts) > 1 else None
            changed = True
        if "tags" not in post.metadata:
            post.metadata["tags"] = parts[1:-1] if len(parts) > 2 else []
            changed = True

    if changed and not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

    body = post.content
    html = markdown.markdown(body)
    return post.metadata, body, html, changed


# 生成 index.json
def generate_index(dry_run=False):
    posts = []
    updated_files = []

    for filepath in find_markdown_files(POSTS_DIR):
        metadata, body, _, changed = parse_and_fix_markdown(filepath, dry_run=dry_run)

        if changed and not dry_run:
            updated_files.append(filepath)

        rel_path = os.path.relpath(filepath, POSTS_DIR)
        slug = os.path.splitext(rel_path)[0].replace("\\", "/")

        post_obj = {
            "category": metadata.get("category"),
            "tags": metadata.get("tags", []),
            "content": body[:1000],
            "summary": metadata.get("summary"),
            "title": metadata.get("title", slug.split("/")[-1]),
            "created": metadata.get("date", datetime.datetime.now().isoformat()),
            "updated": metadata.get("date", datetime.datetime.now().isoformat()),
            "url": f"/posts/{slug}.md"
        }
        posts.append(post_obj)

    if not dry_run:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)

    for path in updated_files:
        print("✅ update:", os.path.relpath(path, POSTS_DIR))


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """
    获取生成的 index.json
    ---
    tags:
      - Posts
    responses:
      200:
        description: 返回 JSON 索引
    """
    return send_file(OUTPUT_FILE)


@app.route("/api/refresh", methods=["GET"])
def refresh_index():
    """
    重新生成 index.json
    ---
    tags:
      - Posts
    parameters:
      - name: dryrun
        in: query
        type: boolean
        default: false
    responses:
      200:
        description: 返回刷新状态
    """
    dry_run = request.args.get("dryrun", "false").lower() == "true"
    generate_index(dry_run=dry_run)
    return jsonify({
        "message": "index.json 已刷新（dry-run 模式: %s）" % dry_run
    }), 200


@app.route("/posts/<path:filename>")
def get_markdown(filename):
    """
    获取指定 Markdown 文件内容
    ---
    tags:
      - Posts
    parameters:
      - name: filename
        in: path
        type: string
        required: true
    responses:
      200:
        description: 返回 Markdown 文件
    """
    base_dir = os.path.abspath("/app/markdown")
    filename = unquote(filename)
    try:
        return send_from_directory(base_dir, filename)
    except FileNotFoundError:
        abort(404, description="文件未找到")


@app.route("/posts/", methods=["GET"])
def list_markdown_files():
    """
    列出 Markdown 文件路径列表
    ---
    tags:
      - Posts
    responses:
      200:
        description: 返回 Markdown 文件路径及访问链接
    """
    base_dir = os.path.abspath("/app/markdown")
    md_files = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")

                md_files.append({
                    "name": rel_path,
                    "url": f"/posts/{rel_path}"
                })

    return jsonify({
        "count": len(md_files),
        "files": md_files
    })


@app.route("/index.json", methods=["GET"])
def index_file():
    """
    等价于 /api/posts， 列出 Markdown 文件路径列表
    ---
    tags:
      - Posts
    responses:
      200:
        description: 返回 Markdown 文件路径及访问链接
    """
    return send_file(OUTPUT_FILE)


@app.route("/", methods=["GET"])
def home():
    """
    服务已经启动提示
    ---
    tags:
      - Posts
    responses:
      200:
        description: 服务已经启动提示
    """
    return jsonify({"code": 0, "message": "服务已经启动..."})


if __name__ == "__main__":
    generate_index()
    app.run(port=1313, host='0.0.0.0')
