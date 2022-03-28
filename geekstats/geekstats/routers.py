class GeekRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_db_tablespaces = {'geek','geekfest'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read geek data.
        """
        if model._meta.db_tablespace in self.route_db_tablespaces:
            return 'geek'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write geek data.
        """
        if model._meta.db_tablespace in self.route_db_tablespaces:
            return 'geek'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the geek apps is
        involved.
        """
        if (
            obj1._meta.db_tablespace in self.route_db_tablespaces or
            obj2._meta.db_tablespace in self.route_db_tablespaces
        ):
           return True
        return None

    def allow_migrate(self, db, db_tablespace, model_name=None, **hints):
        """
        Make sure the geek apps only appear in the
        'auth_db' database.
        """
        if db_tablespace in self.route_db_tablespaces:
            return db == 'geek'
        return None