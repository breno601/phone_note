# phone_note

Use python 2.7!

Install virtualenv for environment.
$ sudo easy_install virtualenv

Enable the virtual env in your phone_note deploy folder.
$ mkdir phone_note
$ cd phone_note
$ virtualenv venv

Activate your env. 
$ . venv/bin/activate

Install Flask.
$ pip install Flask

Install requirements.
$ pip install -r requirements.txt

Run model and db deploy.
$ python models.py

Run the application.
$ python app.py

Access through localhost:5000
