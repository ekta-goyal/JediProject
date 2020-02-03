class ExtraCss:
    extra_css = [
        'https://stackpath.bootstrapcdn.com/bootswatch/3.3.5/flatly/bootstrap.min.css',
        "https://fonts.googleapis.com/css?family=Megrim&display=swap"
        ]

    def add_extra_css(self, css):
        self.extra_css.extend(css)
        print(self.extra_css)