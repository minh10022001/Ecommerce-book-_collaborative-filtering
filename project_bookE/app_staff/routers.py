class MyAppRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'app_staff':
            if model._meta.model_name == 'Account':
                if model.is_staff == False:
                    return 'default'
                else:
                    return 'admin'
            return 'admin'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'app_staff':
            return 'admin'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'app_staff' or
            obj2._meta.app_label == 'app_staff'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'app_staff':
            return db == 'admin'
        return None
    # def db_for_model(self, model, **hints):
    #     if model._meta.model_name == 'Account':
    #         if model.is_staff == False:
    #             return 'default'
    #         else:
    #             return 'admin'
    #     return None