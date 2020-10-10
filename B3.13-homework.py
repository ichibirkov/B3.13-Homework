class HTML:
    """Собирает информацию о тегах и сохраняет её в тот способ вывода который указанн в main."""

    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n</html>"
        return html


class TopLevelTag:
    """Принимает на вход теги и добавляет их в дочернии теги."""

    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        html = "<%s>\n" % self.tag
        for child in self.children:
            html += str(child)
        html += "\n</%s>" % self.tag
        return html


class Tag:
    """Формирует правильность написания обычных тегов, с учетом дочерних."""

    def __init__(self, tag, toplevel=False, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.toplevel = toplevel
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.toplevel:
            print("<%s>" % self.tag)
            for child in self.children:
                print(child)
            print("</%s>" % self.children)

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)


def main(output=None):
    """Основной метод, в котором задаётся информация: теги, наполнение тегов, прикрепленные файлы.
     А так же способ вывода инфомрации"""

    with HTML(output=output) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
        doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img
                    body += div
                    doc += body


# Запускаем код и получаем результат в файл test.html
if __name__ == "__main__":
    main("test.html")
