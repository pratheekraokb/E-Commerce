### DATABASE & Twillio API SETUP Credentials
  1. Create a .env file in the same directory where manage.py file exists.
  2. Add the following lines there \n
      a. TWILIO_ACCOUNT_SID=AC6c882f43f1cda8b2248bf7f2a525d7c2 \n
      b. TWILIO_AUTH_TOKEN=a341bcf8e7e0031c7c2706f0a0f0c40b \n
      c. DATABASE_PASSWORD=YOUR_PASSWORD \n
        Here (a), (b) is obtained by making account in Twilio ( https://www.twilio.com/login ) \n
        DATABASE_PASSWORD is the password of your database. \n
  3. In E_Commerce (That is our project), within Settings.py
         DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'ECommerce',
                'USER': 'root',
                # 'PASSWORD': 'Pratheek@2003',
                'PASSWORD': os.getenv('DATABASE_PASSWORD'),
                'HOST': 'localhost',
                'PORT': '',
            }
        }
         Change the Name to the name of your database 

