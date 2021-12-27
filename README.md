## MiniBlog
Proyecto de desarrollo web con Flask.

## Objetivo
Practicar con el framework web Flask

## Algunas capturas de pantalla
### Home
![Previous view](./capturas/img1.jpg)

### Login / Signup
![Previous view](./capturas/img2.jpg)

### Dasboard
![Previous view](./capturas/img3.jpg)

### View user
![Previous view](./capturas/img4.jpg)

### Admin user
![Previous view](./capturas/img5.jpg)

### Admin post
![Previous view](./capturas/img6.jpg)

### Show post
![Previous view](./capturas/img7.jpg)

## Como empezar
Clona este repo:
```
git clone https://github.com/NSMichelJ/mini_blog.git
```

Instala las dependencias:
```
pip install req.txt
```

Establece las siguientes variables de entorno:
```
set FLASK_APP=entrypoint.py
set FLASK_ENV=development

set MAIL_USERNAME=test@test.com
set MAIL_PASSWORD=yourpassword
```
* para mas configuraciones vea el config/default.py

Corre las migraciones:
```
flask db upgrade
```

Cree un admin:
```
flask createadmin
```

Corra la app:
```
flask run
```

## Nota: Esta aplicación no esta lista para producción, en caso de algún error por favor, dejarlo en los issue