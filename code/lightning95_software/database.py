import firebase_admin
from firebase_admin import credentials, db

class Database:
    def __init__(self, credPath, databaseURL):
        # Initializing the Firebase Realtime Database
        self.credPath = credPath
        self.databaseURL = databaseURL
        self.cred = credentials.Certificate(self.credPath)
        
        firebase_admin.initialize_app(self.cred, {'databaseURL': self.databaseURL})

        # Database self values
        self.root = db.reference()
        self.values = self.Values()
    
    def update(self, child):
        self.root.child(child).update({'crossed-red-line' : self.values.crossed_red_line})
        self.root.child(child).update({'parking-state' : self.values.parking_state})
        self.root.child(child).update({'system-state' : self.values.system_state})

    def read_database(self, child):
        return self.root.child(child).get()
        
    class Values:
        def __init__(self):
            self.crossed_red_line = 0
            self.parking_state = 'EN_PARKING_NOT_COMPLETED'
            self.system_state = 'EN_SYSTEM_SEARCHING'
