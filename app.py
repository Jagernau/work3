from flask import Flask, request, render_template, jsonify
from utils import ToGet, get_text_tags
import my_logger


app = Flask(__name__)

#конфиги приложения
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_AS_ASCII"] = False

#пути файлов с json для класса ToGet
posts = ToGet("./data/posts.json")
coments = ToGet("./data/comments.json")

#внедрил свою функцию в jinja для поиска тегов
app.jinja_env.globals.update(get_tags= get_text_tags)


#вьюшки
@app.route("/")
def page_index():
    """главная страница"""
    all_posts = posts.get_posts_all()
    return render_template("index.html", posts=all_posts)


@app.route("/posts/<post>")
def page_one_post(post):
    """страница с постом, принимает 'pk'"""
    one_post = posts.get_post_by_pk(post)
    comments_of_post = coments.get_comments_by_post_id(post)
    return render_template("post.html", post=one_post, coment=comments_of_post)


@app.route("/search/")
def search_posts():
    """страница с постами найденными по слову"""
    s = request.args.get("s")

    post_from_key = posts.search_for_posts(s)
    count_posts = len(post_from_key)
    all_posts = posts.get_posts_all()
    if s == None:
        return render_template("search.html", posts=all_posts, count=count_posts)
    return render_template("search.html", posts=post_from_key, count=count_posts, searching=s)


@app.route("/users/<username>")
def user_posts(username):
    """страница с постами пользователя"""
    user_posts = posts.get_posts_by_user(username)
    
    return render_template("user-feed.html", posts=user_posts, user=username)


#api с логгером, логер пишет в /logs/api.log
@app.route("/api/posts/")
def api_posts():
    """страница выводит все посты в json"""
    my_logger.api_log_info(f"Запрос /api/posts/")
    posts_js = posts.get_posts_all()
    return jsonify(posts_js)


@app.route("/api/posts/<post_id>")
def api_one_post(post_id):
    """страница выводит один пост json"""    
    my_logger.api_log_info(f"Запрос /api/posts/{post_id}")
    one_post = posts.get_post_by_pk(post_id)
    return jsonify(one_post)


#вьюшка 
@app.route("/tag/<tagname>")
def post_tags(tagname):
    """вывод всех постов с искомым тегом"""
    plus_tag = "#" + tagname
    post_with_tags = posts.search_for_posts(plus_tag)

    return render_template("tag.html", posts=post_with_tags, plus=plus_tag, tagn=tagname)


#Обработчик ошибок
@app.errorhandler(404)
def page_not_found(e):
    return render_template("erors.html", e=e), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('erors.html', e=e), 500


if __name__ == "__main__":
    app.run()

