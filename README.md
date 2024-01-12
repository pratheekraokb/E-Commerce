# PROJECT SETUP
## Packages Installation
  
  Install all packages using the command, **pip install -r requirements.txt** in the same directory where the manage.py file exists. <br/>

## DATABASE & Twillio API SETUP Credentials
  1. Create a .env file in the same directory where manage.py file exists.
  2. Add the following lines there <br/>
      a. TWILIO_ACCOUNT_SID= < Paste Your Account sid ><br/>
      b. TWILIO_AUTH_TOKEN= < Paste Your Auth Token Here > <br/>
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


## How to Run the Project and How to Use it 
  1. Once above setups are done, now we are ready to run the project. Open the terminal in the Root (Where manage.py file exists), run the following command **python3 manage.py runserver**, now a link will be obtained. Goto given link.<br/>
  2. It will open to a Login Page. <br/>
      a. If you are already have an account, signin with the credentials <br/>
      b. If you dont have any account, click *Click Here* button to create new account. Enter the details and click Sign Up. *DONE Account is created !* <br/>
  3. Once you sucessfully signin through credentials, You will be redirected to a home page. Here on the top you can see the navigation bar <br/>
      a. *Home Button* :- Click here to goto home page. <br/>
      b. *About Us* :- Click here to go to about us page where the details regarding the developers will be present <br/>
      c. *My Cart* :- Click here to view your cart. This page will contain the details regarding your cart (Products in cart, Grand Total, Coupen Apply option and Proceed to checkout Option, Which on click will direct you to the payment page and product ordering) <br/>
      d. Next You will see your image and username. Which on click you will get option either to Logout or to view your Profile. <br/>
          Profile Page Will contain the user data and details <br/>
      

  
