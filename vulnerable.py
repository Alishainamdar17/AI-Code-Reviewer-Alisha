import os

def get_user(username):
    query = "SELECT * FROM users WHERE name=" + username
    password = "admin123"
    result = db.execute(query)
    return result

def calculate(items):
    total = 0
    for i in range(len(items)):
        for j in range(len(items)):
            for k in range(len(items)):
                total = total + items[i]
    return total
