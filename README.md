Translator App
==============

Hey guys I had a quick draft on the skeleton. Right
now it's a simple Django app. With with one view set up.
This is also set up on Tim's box so it shouldnt be a hassle.

Do development in a virtual environment
---------------------------------------

This is quite important. On your development machine set do make sure you
have pip and virtualenv installed. On campus ask me to help you with the 
anoying proxy. On a new box enter the following.

>sudo apt-get install python-pip
>sudo pip install virtualenv
>cd {workingfolder}
>vitrualenv virtual
>source virtual/bin/activate
>pip install django

Once you have done the following steps enter the virtual environment
simply by going:

>source virtual/bin/activate

Running Server
--------------

Please do not run the server on port 8080 it messes, with the
proxy. To run the server is very easy, do the following.

>python manage.py runserver 0.0.0.0:9000


 
