# Redshift User Management

Tool to help managing users, groups and schemas on AWS Redshift. It creates random passwords to new users and send them 
by email alongside the database credentials.

## Environmental Variables
To start define the environmental variables:

```
HOST: Redshift host
USER: Superuser name (must have create user privileges
PWD: Superuser password
PORT: Redshift port
DBNAME: Redshift database name
(optional)SENDGRID_API_KEY: To send emails to users
(optional)FROM_EMAIL_ADDR: your email address, or the email you wich to send from
(optional)COMPANY_NAME: Set with your company name
```

## Usage Examples 
To create a new user:

```
rum = RedshiftUserManagement(<username>, <user@email.com>)
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
create_read_only_schema(<schema_name>, <username>)
```
