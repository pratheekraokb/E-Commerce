# PROJECT SETUP

## DATABASE & Twillio API SETUP Credentials
  1. Create a .env file in the same directory where manage.py file exists.
  2. Add the following lines there <br/>
      a. TWILIO_ACCOUNT_SID=AC6c882f43f1cda8b2248bf7f2a525d7c2 <br/>
      b. TWILIO_AUTH_TOKEN=a341bcf8e7e0031c7c2706f0a0f0c40b <br/>
      c. DATABASE_PASSWORD=YOUR_PASSWORD <br/>
        Here (a), (b) is obtained by making account in Twilio ( https://www.twilio.com/login ) <br/>
        DATABASE_PASSWORD is the password of your database. <br/>
  3. In E_Commerce (That is our project), within Settings.py <br/>
         DATABASES = { <br/>
            'default': { <br/>
                'ENGINE': 'django.db.backends.mysql', <br/> 
                'NAME': 'ECommerce', <br/>
                'USER': 'root', <br/>
                'PASSWORD': os.getenv('DATABASE_PASSWORD'),<br/> 
                'HOST': 'localhost', <br/>
                'PORT': '', <br/>
            }
        } <br/>
         Change the Name to the name of your database, Set User to your username (In my case it is root) <br/>

