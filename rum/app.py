from rum.connection.database import Redshift
from rum.utils.password_generator import Password
from rum.utils.send_email import SendGrid


class RedshiftUserManagement:
    def __init__(self, username, email, access_level='read_only', send_mail=True):
        self.username = username
        self.email = email
        self.access_level = access_level
        self.sendmail = send_mail
        self.redshift = Redshift()

        # Initial Setup
        if not self._read_only_group_exists():
            self.redshift.query('CREATE GROUP read_only;')

    def _read_only_group_exists(self):
        sql = open('sqls/check_read_only_exists.sql').read()
        return self.redshift.query(sql).fetchone()[0]

    def add_user(self):
        """
        Add user to redshift, with random password and send email with connection data.
        :return: None
        """
        # Create random password for user
        password = Password().str

        # Create user
        sql = open('sqls/create_user.sql').read().format(self.username, password)
        self.redshift.query(sql)
        print('User {} created with password "{}" (without quotes).'.format(self.username, password))

        # Send email to user
        if self.sendmail:
            sendgrid = SendGrid(self.email)
            try:
                response = sendgrid.send_usercreated_mail(self.username, password)
            except Exception as error:
                raise Exception('If you do not wish to send email to users, '
                                'then set RedshiftUserManagement(send_mail=False).'
                                'Otherwise, set the correct environmental variables.', error)
            if response >= 300:
                print('Failed to send email')

        # Add user to relevant groups
        if self.access_level == 'read_only':
            self._add_user_to_read_only_group()

        return

    def remove_user(self):
        """
        Removes a user from group and then drops it
        :return: None
        """
        sql = open('sqls/remove_user.sql').read().format(self.username)

        self.redshift.query(sql)
        print('User {} dropped.'.format(self.username))

        return

    def _add_user_to_read_only_group(self):
        """
        Add a user to read only group permissions;
        :return: None
        """
        sql = open('sqls/add_user_read_only_group.sql').read().format(self.username)
        self.redshift.query(sql)
        print('User {} added to group read_only.'.format(self.username))

        return

    def create_read_only_schema(self, schema_name, owner_user):
        """
        Create a new schema and add it to read_only group
        :param schema_name: <string>
        :param owner_user: <string> user that will own the schema and have all privileges.
        :return: None
        """
        sql = open('sqls/create_read_only_schema.sql').read().format(schema_name, owner_user)
        self.redshift.query(sql)
        print('Schema {} created.'.format(schema_name))

        return

    def create_group(self, group_name):
        sql = open('sqls/create_group.sql').read().format(group_name)
        self.redshift.query(sql)
        print('Group {} created.'.format(group_name))
