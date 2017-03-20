Visit our main page: [PINGOW.TK](http://www.pingow.tk)

#To run server
* Requirements
 * Python 2.7+
 * Install virtualenv : `pip install virtualenv`
* Running server
 * Run virtualenv:
 
> In Mac 
~~~~
  virtualenv env
  source env/bin/activate
~~~~
 
> In Windows
 ~~~~
  virtualenv env
  env\Scripts\activate
~~~~

 * Install Django and Django REST framework into the virtualenv
~~~~
pip install django
pip install djangorestframework
~~~~

  * Run server
~~~~
 python manage.py runserver
~~~~


# Install using Pingow one click script
## For Mac
(not available yet)
## For Windows 
1. Download set up scripts from our repo at: `pingow-web-service/setup_scripts/`
2. Run script to setup: 
- **OPTION 01**: `setup_WINDOWS_LOCALHOST.bat` Run server on `172.0.0.1:8000` ; but cannot listen to request ourside. That's done.
- **OPTION 02**: `setup_WINDOWS_LISTEN.bat.bat` Run server on `0.0.0.0:8000` ; can listen to request from same network. Do extra setups as:
   - After running set up, the script will fetch folder "`pingow-web-service`" to the same directory. Later you will need to change files in this folder.
   - Now, Check your IP address, by typing IPCONFIG to commandline (IPv4 Address)
   - Copy and Paste this IP to a file name **`settings.py`** located at "`pingow-web-service\src\blog\settings.py`"; find a variable name "`ALLOWED_HOST`" to add this IP to that. 
   - Save the file. That's done.
   
   
# APIs:

~~~~
/position?
cusId=bob&
targetPos=6&
currentPos=6&
trxId=1&
asst=True
Response: 
[exit: False,
nearby: True]

/send_review?
cusId=bob&
shopId=1&
shopStar=5&
shopAsstStar=3&
trxId=1
reviewText="this place is nice"
Response:
[success:True]

/get_recommendation_for_shop?
cusId=bob&
shopId=1
Response:
[shops: [2,3,5]]

/get_recommendation_for_product?
cusId=bob&
productCatId=1
Response:
[shops: [2,3,5]]

/init_trip_with_shop?
cusId=bob&
shopId=1
Response:
[transactionId: 1]


/init_trip_with_shop_and_product?
cusId=bob&
shopId=1&
productCatId=1
Response:
[transactionId: 1]


/get_shop_asst?
cusId=bob&
trxId=1
Response:
[shopAsstName: "Tracy",
shopAsstDesc:"Tracy sells shoes"]
~~~~
