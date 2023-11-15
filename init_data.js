db = db.getSiblingDB('test_db')
db.templates.remove({});
db.createCollection('templates');
db.templates.insert(
        {
            "name": "Birthday form",
            "user_name":"text",
            "birthday": "date"
        });

db.templates.insert(
        {
            "name": "Birthday form with gift",
            "user_name":"text",
            "birthday": "date",
            "gift": "text"
        });
db.templates.insert(
    {
      "name": "Meeting with friend",
      "friend_phone": "phone",
      "meeting_date": "date",
      "meeting_place":"text"
    });
db.templates.insert(
    {
      "name": "User register",
      "user_email": "email",
      "user_phone": "phone",
      "user_password": "text",
      "register_date":"date"
    });