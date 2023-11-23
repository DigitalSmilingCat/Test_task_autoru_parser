# Parser for auto.ru

### Task
The parser collects the list of brands and their models from auto.ru. The 
collected data is saved in two tables. On the main page the user can select 
the brand name from the drop-down list and get the list of related models. 
If the path "update_autoru_catalog" is selected, all data from the database 
will be deleted and re-collected from the site (it will take a lot of time).


### Instuctions
    * Clone the project: git clone https://github.com/DigitalSmilingCat/Test_task_autoru_parser.git
    * Set up a virtual environment and install dependencies
    ** $ python -m venv .venv
    ** $ source .venv/bin/activate
    ** $ python -m pip install -r requirements.txt
    ** Create file .env, add "SECRET_KEY" and "DJANGO_ALLOWED_HOSTS" to it
    * Launch the app: python manage.py runserver
