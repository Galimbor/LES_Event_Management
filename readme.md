# LES

Descrição 
## Installation

Install Virtual env with [pip](https://pypi.org/project/virtualenv/).

```bash
pip install virtualenv
```

Create and activate your virtual environment
- Linux
```bash
virtualenv env
source env/bin/activate
```
- Windows
```bash
virtualenv env
env\Scripts\activate
```

Install the project in your environment
```bash
pip install -r requirements.txt
```

Dependencies
```python
pip install mysqlclient
```

Apply database migrations 
```python 
python manage.py migrate
```

## Run local server

```python 
python manage.py runserver [port number]
```
[port number] is optional, but you might have to select a different one if another program (like Xampp) is using the default local port.

## Basic management commands
```python
python manage.py makemigrations 
python manage.py migrate
python manage.py createsuperuser
python manage.py startapp
python manage.py shell
```

## Dev tips
* Never push directly to master
* Keep it simple. Invest in good code instead of complex features.
* If you install a new app, don't forget to run:
```python 
pip freeze > requirements.txt
```

## Contributing
- Artur Rodrigues
- Jean Morelli
- Ricardo Correria

## License
[MIT](https://choosealicense.com/licenses/mit/)