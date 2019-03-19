# Redshift User Management

Tool to help managing users, groups and schemas on AWS Redshift. It creates random passwords to new users and send them 
by email alongside the database credentials.


## Installing the project locally
1. Clone the repository and create a new virtual environment:
```
git clone https://github.com/emcasa/rum.git
cd rum
python3 -m virtualenv env
source env/bin/activate
```

2. Install all dependencies by running:
```
pip install -r requirements.txt
```

3. Use the template_local.env to set the environment variables to a file called 
local.env. Then export the env vars using:

```
cp template_local.env local.env
set -a source local.env set +a
```

4. Run the code in your preferred IDE. 

## Usage Examples 
To create a new user:

```
from app import RedshiftUserManagement
 
rum = RedshiftUserManagement('<username>', '<user@email.com>')
rum.add_user()
>>> User <username> created with password "randompassword" (without quotes).
```

To remove a user:
```
rum.remove_user()
>>> User <username> dropped.
```

To create a new schema with ownership to <username>:
```
from app import RedshiftSchemaManagement

rsm = RedshiftSchemaManagement('<schema_name>')
create_read_only_schema('<username>')
>>> Schema <schema_name> created.
```


