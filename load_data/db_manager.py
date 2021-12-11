from db_context import db_context

#DO NOT ADD ANYTHING HERE - THIS FILE IS DONE
class db_manager:
    def __init__(self, is_drop = False):
        self.is_drop = is_drop

    def __enter__(self):
        self.db = db_context(is_drop = self.is_drop)
        self.db.connect()
        return self.db
  
    def __exit__(self, *args, **kwargs):
        self.db.disconnect()
