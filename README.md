Pyblog
-----
### Introduction
Personal Blogging web-application to Post, Delete, Update Blogs in Admin Dashboard and public can see blogs.

### Overview

you should have a fully functioning site that is at least capable of doing the following, if not more, using a Pymongo database:

* Admin login.
* Contact to admin.
* Insert new blog.
* Update blog.
* delete blog.

### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **Pymongo** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask** for web-app development
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

 ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. 
                    "python app.py" to run after installing dependences
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── img
  │   ├── vendor *** js files
  |
  └── templates *** html files
  |
  └── config.json *** include information of admin login and database connection
  |
  └── Procfile *** use in deploy application at heroku
  ```
### Setup
1. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```
2. setup your database:
  ```
  "pri_uri": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",

  ```
  change in config.json file. use ![Mongodb](https://docs.atlas.mongodb.com/driver-connection/ "Connect cluster driver")

3. Run the development server:
  ```
  $ python app.py
  ```

#### Web-App Screenshot 
![Home page](https://github.com/imshubh17/Pyblog/blob/master/static/img/home.PNG "Home")

![Contact Form](https://github.com/imshubh17/Pyblog/blob/master/static/img/contact.PNG "Contact")

![Login page](https://github.com/imshubh17/Pyblog/blob/master/static/img/login.PNG "Login page")

![Dashboard page](https://github.com/imshubh17/Pyblog/blob/master/static/img/dashboard.PNG "Dashboard aticivity page")

* Happy to share in public to use as a starter project and improve this project. Thanks!!!
