# To start the containers, run the command below from the root directory
### You might have to fix some dependencies

# Command: sudo docker-compose -f docker-compose.yml up  --build

Now that everything is up-and-running create the database models using this command:
docker-compose -f docker-compose.yml run api python manage.py recreate-db

Now lastly, train the machine learning model with this command:
docker-compose -f docker-compose.yml run model python manage.py train

# To run the application you can look at the readme in the application map.

# In the module_code map you will find the code that runs on the sensor and pygate
