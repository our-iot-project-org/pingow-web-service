@echo off
cmd /k "^
rmdir /q /s pingow-web-service & ^
git clone https://github.com/our-iot-project-org/pingow-web-service.git & ^
pip install virtualenv & ^
virtualenv env & ^
env\Scripts\activate & ^
pip install freeze -r pingow-web-service\requirements.txt & ^
python pingow-web-service\src\manage.py runserver"