Visit our main page: [PINGOW.TK](http://www.pingow.tk)

#To run server
* Requirements
 * Python 2.7+
 * Install virtualenv : `pip install virtualenv`
* Running server
 * Run virtualenv:
 
> In Mac 
~~~~
  virtualenv env
  source env/bin/activate
~~~~
 
> In Windows
 ~~~~
  virtualenv env
  env\Scripts\activate
~~~~

 * Install Django and Django REST framework into the virtualenv
~~~~
pip install django
pip install djangorestframework
~~~~

  * Run server
~~~~
 python manage.py runserver
~~~~
