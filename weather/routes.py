from bottle import route

@route('/')
def index():
    return "<h1>مرحباً بك في تطبيق الطقس</h1>"

