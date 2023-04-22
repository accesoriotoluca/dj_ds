""" 
* EJEMPLO
! EJEMPLO
? EJEMPLO
TODO: EJEMPLO

? VIRTUAL ENV:
virtualenv venv
.\venv\Scripts\activate

? PIP
py.exe -m pip install --upgrade pip
pip install django
pip install django-crispy-forms
pip install pandas
pip install matplotlib
pip install pillow
pip install seaborn
pip install xhtml2pdf
pip install crispy-bootstrap4

pip freeze > requirements.txt

? PROJECT
django-admin startproject reports_proj .
py manage.py migrate
py manage.py createsuperuser

? MANAGE
py manage.py startapp sales
py manage.py startapp reports
py manage.py startapp profiles
py manage.py startapp products
py manage.py startapp customers

py manage.py runserver

"""