from json import load, JSONDecodeError
import re


class ToGet:
    def __init__(self, path):
        """Инициализирует все посты сразу по месту нахождения json"""
        if type(path) != str:
            raise TypeError("должно быть str")
        self.path = path

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                all_ = load(file)
            self.all_posts = all_

        except FileNotFoundError:
            print("не правильный путь")
        except JSONDecodeError:
            print("ошибка в json")


    def get_posts_all(self):
        """выводит все посты"""
        try:
            return self.all_posts
        except AttributeError:
            ("не был загружен атрибут")


    def get_posts_by_user(self, user_name):
        """возвращает посты юзера"""
        user_posts = []
        for i in self.all_posts:
            if user_name == i["poster_name"]:
                user_posts.append(i)
        return user_posts


    def get_post_by_pk(self, pk):
        """возвращает один пост по идентефикатору"""
        pk = int(pk)
        for i in self.all_posts:
            if pk == i["pk"]:
                return i


    def search_for_posts(self, query):
        """возвращает посты по ключевому слову"""
        query = str(query)
        posts_from_keys = []
        if query.startswith("#"):
            for i in self.all_posts:
                if query in get_text_tags(i["content"]):
                    posts_from_keys.append(i)
        else:
            for i in self.all_posts:
                if query in i["content"]:
                    posts_from_keys.append(i)    
        return posts_from_keys


    def get_comments_by_post_id(self, post_id):
        """возвращает коментарии к посту"""
        post_id = int(post_id)
        comments = []
        for i in self.all_posts:
            if post_id == i["post_id"]:
                comments.append(i)
        return comments


#функция
def get_text_tags(text):
    """возвращает теги в тексте если есть"""
    patern = re.compile(r'\#\w+', re.U)
    tags = set(re.findall(patern, text))
    return tags

