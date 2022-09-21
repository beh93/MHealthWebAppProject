<-- Plan Generation --> 

Please note that, due to time constraints, only the Productivity category will generate a complete user Plan. When selecting interests upon registration, please
select this option for testing Plan funcionality.  Other Categories can easily be populated with topics via the Django admin portal.



<-- Database Initialisation -->

The database is not provided due to size.  It needs to be initialised and populated from the working directory.  

python manage.py migrate
python manage.py makemigrations light
python manage.py migrate

Test data is included via the population script populate_light.py
