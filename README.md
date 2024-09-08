# ShopEase - an advanced eCommerce Application

## Brief Introduction

ShopEase is an advanced eCommerce platform developed to provide a seamless and user-friendly online shopping experience. Designed to meet the evolving demands of the modern market, ShopEase leverages cutting-edge technologies to ensure secure transactions, authentic user reviews, and efficient product categorization. The platform aims to empower small local businesses by enhancing their online presence and expanding their reach.

### Key Features

- **User Authentication System:**
  - **Secure Sign-in and Sign-up Pages:** User-friendly interfaces for account creation and login.
  - **Hashed Password Storage:** Utilizes bcrypt for secure password handling.
  - **Role-Based Access Control:** Differentiates between admin and normal users for tailored experiences.


- **Product Management:**
  - **Dynamic Product Catalog:** Regular updates and maintenance of product listings.
  - **Product Categorization:** Machine learning algorithms for accurate and personalized product categorization.

- **Comment Section:**
  - **Hierarchical Comment System:** Recursive algorithm and tree data structure for nested comments and structured discussions.
  - **Verified Purchaser Badge:** Marks comments from users who have purchased the product, ensuring authenticity.

- **Admin Dashboard:**
  - **Comprehensive Analytics:** Visualizations such as bar and pie charts for sales analysis, category-wise and company-wise metrics.
  - **Product Management:** Tools for managing products, categories, and companies.

- **User Experience Enhancements:**
  - **Downloadable Product Brochures:** Access detailed product information in PDF format.
  - **Invoice and Bill Downloads:** Clear and organized records of transactions available in PDF format.
  - **Responsive Chatbot:** Assists with order tracking, product searches, and technical queries.
  - **MyCart Page:** Manage selected items before checkout.

- **Security Features:**
  - **Encrypted Password Storage:** Protection of user credentials using advanced encryption.
  - **Secure Data Transmission:** Encryption protocols to ensure safe data handling.

- **Help and Support:**
  - **Help Section with Tutorials:** Embedded YouTube videos for site usage and feature explanations.
  - **About Section:** Information about the project, its objectives, and the development team.

## Technologies Used

- **Backend Framework:** Django
- **Database:** MySQL
- **Machine Learning:** scikit-learn
- **Frontend Technologies:** HTML, CSS, JavaScript, AJAX
- **Testing Tools:** Selenium, ThunderClient (VS Code extension)




## PROJECT SETUP
### Packages Installation
  
  Install all packages using the command, **pip install -r requirements.txt** in the same directory where the manage.py file exists. <br/>

### DATABASE & Twillio API SETUP Credentials
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
    Next You will see the Each category name and the products belonging to that category. When you click Explore More button, you will be directed to a page where you can see all the products in that category. You can filter the products based on Money Range, Sort it in ascending or descending order of price, Filter by company,etc.<br/>
    When you click the product, Product View Page will be opened, where you can see the product name,image,description,add to cart option. Additionally you can see the comments section where even you can contribute to it.<br/>
    At the bottom you can see the Chatbot Option *Chat With Bot* which on click, a window will be present where you can talk with ***ShopEase BOT*** 
      

  ## API Documentation
  ### Overview
  The ShopEase API provides endpoints for managing users, products, and sales statistics. It includes functionalities for user management (checking availability, creating, updating, and deleting users), product management (creating, updating, and deleting products), and retrieving sales statistics (by category, company, and amount).

### Key Endpoints

**User Management**
- **Check Email**: `/api/check_email/`
- **Check Username**: `/api/check_username/`
- **Create User**: `/api/create_user/`
- **Update User**: `/api/update_user/`
- **Delete User**: `/api/delete_user/<int:user_id>/`

**Product Management**
- **Create Product**: `/api/create_product/`
- **Update Product**: `/api/update_product/<int:product_id>/`
- **Delete Product**: `/api/delete_product/<int:product_id>/`

**Sales Statistics**
- **Category Sales Stats**: `/api/stats/category/`
- **Company Sales Stats**: `/api/stats/company/`
- **Sales Amount Stats**: `/api/stats/amountWiseSales/`

For detailed information, please refer to the [full API documentation](https://drive.google.com/file/d/1A5l-ebL2DxDH0GgU9w75zU_r5NMhMP1R/view?usp=drive_link).