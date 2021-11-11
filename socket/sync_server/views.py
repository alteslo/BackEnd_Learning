def index():
    with open('socket/templates/index.html', 'r') as template:
        return template.read()


def blog():
    with open(r'socket\templates\pushkin.html', 'r') as template:
        return template.read()
