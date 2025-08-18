RESOURCE_GROUP_NAME='iu-python-flask-memoryvault'
APP_SERVICE_NAME='iu-python-flask-memoryvault'

az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $APP_SERVICE_NAME \
    --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true