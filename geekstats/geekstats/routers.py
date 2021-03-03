class GeekRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'geek'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read geek data.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'geek'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write geek data.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'geek'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the geek apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the geek apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'geek'
        return None