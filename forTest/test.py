from urllib.request import urlopen
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
f = urlopen('https://yandex.ru')
data = f.read().decode('utf-8')
print('_')