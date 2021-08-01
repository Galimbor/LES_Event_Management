# LES

## Descrição

This project is the final project of my bachelors in Informatic Engineering. It is an event management web-app, developed with Django for the back-end, Vue.JS, pure Javascript and Bulma for the front-end, and MySQL for the database. It was developed in an agile enviroment, were Scrum was used methodology and Trello was selected as the scrum board.

The project started with user and system requirement gathering, building of use-cases and lastly the scenarios for each of the use cases. With the use-cases written, we started the processing of modeling the system via use of an application called ```Visual Paradgim```. With this tool many diagrams weve developed, namely class and object diagrams, state diagrams, activity diagrams , sequence diagrams , components diagrams and finally installation diagrams.

At the same time, a interface was developed, where several surveys were delivered to several possible clients of this application, scenarios of interaction were developed and prototypes were created. The used tool was Axure RP. 

After this stages, the development of the code started. This web-app is divided into 5 django applications : 

+ Forms App, which is reponsible for the creation of templates and actual forms that participants will then fill
+ Enroll App, which allows participants to enroll in an event
+ Event App, which is responsible for the whole process of an event submission
+ Users App, responsible for the login and register and users logic.
+ Feedback App, allows participants to send feedback to a certain event they participated.
+ Resource App, responsible for handling the attribution of rooms, equipments and services to events.
+ Notifications App, responsible for handling automatic notifications creating when specific actions happen.This project is an MCTS implementation on the TIC-TAC-TOE game using JAVA, developed for the subject of Artifical Inteligente belonging to the bachelors degree of Informatic Engineering.

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


Must add to ``__init__.py``
```python
import pymysql

pymysql.install_as_MySQLdb()
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


## License
[MIT](https://choosealicense.com/licenses/mit/)
