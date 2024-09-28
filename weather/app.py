import bottle
import requests
import os

# مفتاح OpenWeatherMap API الخاص بك
api_key = "5dcb3fa4c2554107b4f221801242409"

# المسار للصفحة الرئيسية
@bottle.route('/')
def index():
    return '''
    <h1>مرحباً بك في تطبيق الطقس</h1>
    <form action="/weather" method="get">
        <label for="city">أدخل اسم المدينة:</label>
        <input type="text" id="city" name="city">
        <input type="submit" value="عرض الطقس">
    </form>
    '''

# المسار لجلب بيانات الطقس
@bottle.route('/weather')
def get_weather():
    city = bottle.request.query.city or "Benghazi"  # استخدم "Benghazi" كمدينة افتراضية إذا لم يتم إدخال اسم المدينة

    # رابط جلب بيانات الطقس
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    # إرسال الطلب وجلب البيانات
    response = requests.get(base_url)
    
    # التحقق من نجاح الطلب
    if response.status_code == 200:
        data = response.json()
        
        # استخراج البيانات
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        
        # إرجاع البيانات كصفحة HTML
        return f"""
        <h1>الطقس في {city}</h1>
        <p>درجة الحرارة: {temperature}°C</p>
        <p>الرطوبة: {humidity}%</p>
        <p>وصف الطقس: {description}</p>
        <a href="/">العودة إلى الصفحة الرئيسية</a>
        """
    else:
        return "<h1>تعذر جلب بيانات الطقس. تأكد من اسم المدينة وحاول مجددًا.</h1>"

# ضبط التطبيق للعمل مع WSGI
def wsgi_app():
    """Returns the application to make available through wfastcgi."""
    return bottle.default_app()

# تشغيل التطبيق محليًا إذا تم تنفيذ الملف مباشرةً
if __name__ == '__main__':
    # إعدادات الخادم
    host = os.environ.get('SERVER_HOST', 'localhost')
    try:
        port = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        port = 5555

    # تشغيل التطبيق باستخدام خادم wsgiref
    bottle.run(host=host, port=port, debug=True)
