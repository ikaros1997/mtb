DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mtb',  # 要连接的数据库，连接前需要创建好
        'USER': 'root',  # 连接数据库的用户名
        'PASSWORD': 'root123',  # 连接数据库的密码
        'HOST': '127.0.0.1',       # 连接主机，默认本级
        'PORT': 3306,   #  端口 默认3306
        "TEXT_CHARSET": "utf-8"
    }
}
