from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb+srv://minhne2203:cCdkU1nRpPsQ07Q8@cluster0.twcco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["fb_cmt_manage"]  # Thay bằng tên database
collection = db["facebook_links"]  # Thay bằng tên collection

# Cập nhật tất cả document, thêm field "active": "on"
collection.update_many({}, {"$set": {"active": "on"}})

print("Đã thêm field 'active' vào tất cả document!")
