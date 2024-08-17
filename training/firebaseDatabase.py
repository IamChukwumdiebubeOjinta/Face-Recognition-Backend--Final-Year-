import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facial-r-default-rtdb.firebaseio.com/'
})


ref = db.reference('facial-r-users')

data = {
    "321654": {
        "name": "Murtaza Hassan", 
        "major": "Robotics",      
        "type": "Visitor",
        "invited_by": "Jane Smith",
        "ref_no": "2022/21009COS",  
        "registered": "first time added to db",
        "last_recorded_time": "2022-12-11 00:54:34" 
    },
    "852741": {
        "name": "Emly Blunt",      
        "major": "Economics",      
        "type": "Visitor",
        "invited_by": "Jane Smith",
        "ref_no": "2022/21009COS",
        "registered": "first time added to db",
        "last_recorded_time": "2022-12-11 00:54:34"
    },
    # "963852": {
    #     "name": "Elon Musk",       
    #     "major": "Physics",        
    #     "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD...",
    #     "type": "Visitor",
    #     "invited_by": "Jane Smith",
    #     "ref_no": "2022/21009COS",  
    #     "registered": "first time added to db",
    #     "last_recorded_time": "2022-12-11 00:54:34"
    # }
}

for key, value in data.items():
    ref.child(key).set(value)


# https://facial-r-default-rtdb.firebaseio.com/