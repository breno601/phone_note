# phone_note

Use python 2.7!

* Install virtualenv for environment.
```sh
$ sudo easy_install virtualenv
```

* Enable the virtual env in your phone_note deploy folder.
```sh
$ mkdir phone_note
$ cd phone_note
$ virtualenv venv
```

* Activate your env. 
```sh
$ . venv/bin/activate
```

* Install Flask.
```sh
$ pip install Flask
```

* Install requirements.
```sh
$ pip install -r requirements.txt
```

* Run model and db deploy.
```sh
$ python models.py
```

* Run the application.
```sh
$ python app.py
```

Access through localhost:5000
