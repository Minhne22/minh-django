from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb+srv://minhne2203:cCdkU1nRpPsQ07Q8@cluster0.twcco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["mydatabase"]
users_collection = db["users"]

# Tạo tài khoản admin
username = "user"
password = "user123"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

admin_user = {
    "username": username,
    "password": hashed_password,
    "role": "user"
}

# Kiểm tra và thêm admin nếu chưa tồn tại
if not users_collection.find_one({"username": username}):
    users_collection.insert_one(admin_user)
    print("Admin account created successfully!")
else:
    print("Admin account already exists.")
