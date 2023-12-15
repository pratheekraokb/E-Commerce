# PROJECT SETUP
## Packages Installation
  1. pip install Django==4.2.4 <br> 
  2. pip install dnspython==2.4.2  <br> 
  3. pip install idna==3.3 <br>
  4. pip install anyio==3.7.1 <br> 
  5. pip install pydantic==2.4.2 <br>
  6. pip install Flask==3.0.0 <br>
  7. pip install pymongo==4.6.0 <br>
  8. pip install requests==2.25.1 <br>
  9. pip install opencv-python==4.8.1.78 <br>
  10. pip install numpy==1.26.0 <br>
  11. pip install orjson==3.9.7 <br>
  12. pip install pandas==2.1.1 <br>
  13. pip install paramiko==2.9.3 <br>
  14. pip install pip==23.3.1 <br>
  15. pip install pygame==2.5.2 <br>
  16. pip install PyGithub==2.1.1 <br>
  17. pip install PyYAML==5.4.1 <br>
  18. pip install scikit-learn==1.3.1 <br>
  19. pip install SecretStorage==3.3.1 <br>
  20. pip install setuptools==59.6.0 <br>
  21. pip install twilio==8.10.2 <br>
  22. pip install uvicorn==0.23.2 <br>
  23. pip install uvloop==0.17.0 <br>
  24. pip install websockets==11.0.3 <br>
  25. pip install wheel==0.37.1 <br>
  Or you can install it by the command, **pip install -r requirements.txt** in the same directory where the manage.py file exists. <br/>

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

