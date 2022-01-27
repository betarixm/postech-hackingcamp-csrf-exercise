from flask import Flask, request, render_template, abort
import os

from admin import checks_client_page, ADMIN_KEY

app = Flask(__name__)
app.secret_key = os.urandom(32)

PORT = int(os.getenv("APP_PORT", "8000"))

notices = [
    {"title": "(예금) 예적금 금리 인상 조치", "content": '<iframe width="560" height="315" src="https://www.youtube.com/embed/Twi92KYddW4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'},
    {"title": "(송금) 송금 수수료 면제 이벤트", "content": '<a href="https://github.com/betarixm">Link</a>'},
]
posts = [
    {"title": "뭐게요 맞혀봐요", "content": '<iframe width="560" height="315" src="https://www.youtube.com/embed/aZGaSrI0RoY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'},
]


@app.route("/")
def index():
    return render_template("index.html", notices=notices, posts=posts, enumerate=enumerate)


@app.route("/view/<category>/<int:idx>")
def view(category: str, idx: int):
    if category in ["notice", "post"]:
        target = notices if category == "notice" else posts
        return render_template("viewer.html", post=target[idx])

    abort(404)


@app.route("/post")
def post():
    return render_template("upload.html")


@app.route("/post/upload")
def post_upload():
    title = request.args.get("title")
    content = request.args.get("content")

    upload(title, content, posts)
    checks_client_page(title, content)

    return "<script>alert('Success!');location.href='/';</script>"


@app.route("/notice/upload")
def notice():
    if ADMIN_KEY not in request.cookies:
        abort(403)

    title = request.args.get("title")
    content = request.args.get("content")

    upload(title, content, notices)

    return "<script>alert('Success!');location.href='/';</script>"


@app.route("/check")
def check():
    title = request.args.get("title")
    content = request.args.get("content")

    return render_template("viewer.html", post={"title": title, "content": content})


def upload(title: str, content: str, target: list):
    if title is None or content is None:
        abort(400)

    target.append({"title": str(title), "content": str(content)})


app.run(host="0.0.0.0", port=PORT, debug=False)
