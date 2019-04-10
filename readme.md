# Title hasn't been decided yet...
## Require
- python >=3.6.3
- pipenv
- Django == 2.1.0
- Vue == 2.0
- VueCli == 3.5.5
- node >= 8.0
- npm >=3.5

## run the project locally
- fist clone the project
- install the js lib by npm or yarn
```
npm install
```
- install the python supply lib and activate the virtualenv
```
pipenv install --dev & pipenv shell
```
- run the vuecli app by
```bash
npm run serve 
or
yarn serve
```
- run the django backend by
```
python manage.py runserver
```
## deploy
- clone the project
- complete the vue model and pipenv building like the above.
- sh ./run.sh to start the project on the server.


## developing record 
- April 9, Initiate the developing enviornment both on local PC and Ali Cloud Web server, which contains the front framework (like node, npm, and VueCLi), the backend python suppilcations such like DjangoRestFrameWork. Use a simple demo to confirm that the developing process performs well.