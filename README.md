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
      a. ***Home Button*** :- Click here to goto home page. <br/>
      b. ***About Us*** :- Click here to go to about us page where the details regarding the developers will be present <br/>
      c. ***My Cart*** :- Click here to view your cart. This page will contain the details regarding your cart (Products in cart, Grand Total, Coupen Apply option and Proceed to checkout Option, Which on click will direct you to the payment page and product ordering) <br/>
      d. Next You will see your image and username. Which on click you will get option either to Logout or to view your Profile. <br/>
          Profile Page Will contain the user data and details <br/>
    <br/>
    Next You will see the Each category name and the products belonging to that category. When you click *Explore More* button, you will be directed to a page where you can see all the products in that category. You can filter the products based on Money Range, Sort it in ascending or descending order of price, Filter by company,etc.<br/>

    When you click the product, *Product View* Page will be opened, where you can see the product name,image,description,add to cart option. Additionally you can see the comments section where even you can contribute to it. 
    <br/>
    At the bottom you can see the Chatbot Option *Chat With Bot* which on click, a window will be present where you can talk with ***ShopEase BOT*** 
      

  
