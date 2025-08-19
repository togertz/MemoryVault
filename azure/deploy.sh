RESOURCE_GROUP_NAME='iu-python-flask-memoryvault'
APP_SERVICE_NAME='iu-python-flask-memoryvault'

zip -r app.zip src requirements.txt app.py

az webapp deploy \
    --name $APP_SERVICE_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --src-path app.zip

rm app.zip