from rum.connection.database import Redshift
from rum.utils.password_generator import Password
from rum.utils.send_email import SendGrid
from rum.utils.sql_files import open_sql_file


class RedshiftUserManagement:
    def __init__(self, username, email, access_level='read_only', send_mail=True):
        self.username = username
        self.email = email
        self.access_level = access_level
        self.sendmail = send_mail
        self.redshift = Redshift()

        if not self._read_only_group_exists():
            self.redshift.query('CREATE GROUP read_only;')

    def _read_only_group_exists(self):
        sql = open_sql_file('check_read_only_exists')
        return self.redshift.query(sql).fetchone()[0]

    def add_user(self):
        """
        Add user to redshift, with random password and send email with connection data.
        :return: None
        """
        password = Password().str

        sql = open_sql_file('create_user').format(self.username, password)
        self.redshift.query(sql)
        print('User {} created with password "{}" (without quotes).'.format(self.username, password))

        if self.sendmail:
            sendgrid = SendGrid(self.email)
            sendgrid.send_usercreated_mail(self.username, password)

        if self.access_level == 'read_only':
            self._add_user_to_read_only_group()

        return

    def remove_user(self):
        """
        Removes a user from group and then drops it
        :return: None
        """
        sql = open_sql_file('remove_user').format(self.username)

        self.redshift.query(sql)
        print('User {} dropped.'.format(self.username))

        return

    def _add_user_to_read_only_group(self):
        """
        Add a user to read only group permissions
        :return: None
        """
        sql = open_sql_file('add_user_read_only_group').format(self.username)
        self.redshift.query(sql)
        print('User {} added to group read_only.'.format(self.username))

        return


class RedshiftSchemaManagement:
    def __init__(self, schema_name):
        self.redshift = Redshift()
        self.schema_name = schema_name

    def create_read_only_schema(self, owner_user):
        """
        Create a new schema and add it to read_only group
        :param owner_user: <string> user that will own the schema and have all privileges.
        :return: None
        """
        sql = open_sql_file('create_read_only_schema').format(self.schema_name, owner_user)
        self.redshift.query(sql)
        print('Schema {} created.'.format(self.schema_name))

        return


class RedshiftGroupManagement:
    def __init__(self, group_name):
            self.redshift = Redshift()
            self.group_name = group_name

    def create_group(self):
        """
        Create a new user group
        :return: None
        """
        sql = open_sql_file('create_group').format(self.group_name)
        self.redshift.query(sql)
        print('Group {} created.'.format(self.group_name))

        return
