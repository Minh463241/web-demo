import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load biến môi trường (nếu dùng .env)
load_dotenv()

# Lấy URI từ biến môi trường (hoặc bạn có thể hardcode)
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI chưa được thiết lập trong biến môi trường")

client = MongoClient(MONGO_URI)

# Lấy tên DB từ biến môi trường, mặc định là 'qlksda'
db_name = os.environ.get("DB_NAME", "qlksda")
db = client[db_name]

# ---------------------------
# Các collection
# ---------------------------
customers_collection        = db['customers']
room_images_collection      = db['room_images']
bookings_collection         = db['bookings']
services_collection         = db['services']
invoices_collection         = db['invoices']
invoice_services_collection = db['invoice_services']
room_types_collection       = db['room_types']
staff_collection            = db['staff']
rooms_collection            = db['rooms']

# ---------------------------
# Khách hàng
# ---------------------------
def get_customer_by_email(email):
    """Tìm user theo 'Email'."""
    return customers_collection.find_one({'Email': email})

def create_customer(customer_data):
    """
    Ví dụ customer_data:
      {
        'HoTen': 'Nguyễn Văn A',
        'Email': 'abc@gmail.com',
        'password': '123456',
        'DienThoai': '0123456789',
        'DiaChi': 'Hà Nội',
        'CMND': '123456789',
        'last_login': None,
        'avatar': None
      }
    """
    result = customers_collection.insert_one(customer_data)
    return str(result.inserted_id)

def update_last_login(email):
    """Cập nhật thời gian đăng nhập cuối cùng dựa trên Email."""
    result = customers_collection.update_one(
        {'Email': email},
        {'$set': {'last_login': datetime.utcnow()}}
    )
    return result.modified_count

def update_user_avatar(email, avatar_filename):
    """Cập nhật avatar cho user dựa trên Email."""
    result = customers_collection.update_one(
        {'Email': email},
        {'$set': {'avatar': avatar_filename}}
    )
    return result.modified_count

# ---------------------------
# Ảnh phòng
# ---------------------------
def create_room_image(room_image_data):
    """Thêm document ảnh phòng."""
    result = room_images_collection.insert_one(room_image_data)
    return result.inserted_id

def get_room_images_by_room(ma_phong):
    return list(room_images_collection.find({'MaPhong': ma_phong}))

# ---------------------------
# Đặt phòng
# ---------------------------
def create_booking(booking_data):
    """
    Ví dụ booking_data:
      {
        'MaDatPhong': 123,
        'MaKH': 456,
        'MaPhong': 789,
        'NgayDat': datetime(...),
        'NgayNhan': datetime(...),
        'NgayTra': datetime(...),
        'SoLuongKhach': 2,
        'TinhTrang': 'Chờ xác nhận'
      }
    """
    result = bookings_collection.insert_one(booking_data)
    return str(result.inserted_id)

def get_booking_by_id(ma_dat_phong):
    return bookings_collection.find_one({'MaDatPhong': ma_dat_phong})

def update_booking(ma_dat_phong, update_data):
    result = bookings_collection.update_one(
        {'MaDatPhong': ma_dat_phong},
        {'$set': update_data}
    )
    return result.modified_count

def is_room_booked(ma_phong, checkin_date, checkout_date):
    """
    Kiểm tra phòng (MaPhong) có bị đặt trong khoảng [checkin_date, checkout_date) không?
    """
    booking = bookings_collection.find_one({
        'MaPhong': ma_phong,
        'NgayNhan': {'$lt': checkout_date},
        'NgayTra': {'$gt': checkin_date}
    })
    return booking is not None

# ---------------------------
# Dịch vụ
# ---------------------------
def get_service_by_id(ma_dich_vu):
    return services_collection.find_one({'MaDichVu': ma_dich_vu})

def create_service(service_data):
    result = services_collection.insert_one(service_data)
    return str(result.inserted_id)

def get_all_services():
    return list(services_collection.find())

# ---------------------------
# Hóa đơn
# ---------------------------
def create_invoice(invoice_data):
    result = invoices_collection.insert_one(invoice_data)
    return str(result.inserted_id)

def get_invoice_by_id(ma_hoa_don):
    return invoices_collection.find_one({'MaHoaDon': ma_hoa_don})

def get_all_invoices():
    return list(invoices_collection.find())

# ---------------------------
# Hóa đơn dịch vụ
# ---------------------------
def create_invoice_service(invoice_service_data):
    result = invoice_services_collection.insert_one(invoice_service_data)
    return str(result.inserted_id)

def get_invoice_services_by_invoice(ma_hoa_don):
    return list(invoice_services_collection.find({'MaHoaDon': ma_hoa_don}))

# ---------------------------
# Loại phòng
# ---------------------------
def get_all_room_types():
    return list(room_types_collection.find())

def get_room_type_by_id(ma_loai_phong):
    return room_types_collection.find_one({'MaLoaiPhong': ma_loai_phong})

def create_room_type(room_type_data):
    """
    Ví dụ room_type_data:
      {
        'MaLoaiPhong': 123,
        'name': 'Phòng VIP',
        'price': 1000000,
        'description': 'Phòng siêu đẹp'
      }
    """
    result = room_types_collection.insert_one(room_type_data)
    return str(result.inserted_id)

# Alias để dùng trong app.py
add_room_type = create_room_type

# ---------------------------
# Nhân viên (Admin)
# ---------------------------
def get_staff_by_email(email):
    return staff_collection.find_one({'Email': email})

def create_staff(staff_data):
    result = staff_collection.insert_one(staff_data)
    return str(result.inserted_id)

def get_all_staff():
    return list(staff_collection.find())

def get_admin_by_email_and_password(email, password):
    admin = staff_collection.find_one({'Email': email})
    if admin and admin.get('password') == password:
        return admin
    return None

# ---------------------------
# Phòng
# ---------------------------
def get_all_rooms():
    return list(rooms_collection.find())

def get_room_by_id(ma_phong):
    return rooms_collection.find_one({'MaPhong': ma_phong})

def create_room(room_data):
    """
    Ví dụ room_data:
      {
        'MaPhong': None,
        'SoPhong': '101',
        'MaLoaiPhong': 1,
        'TrangThai': 'Trống',
        'MoTa': 'Phòng view biển',
        'created_at': datetime.utcnow()
      }
    """
    result = rooms_collection.insert_one(room_data)
    return str(result.inserted_id)

def update_room(ma_phong, update_data):
    result = rooms_collection.update_one({'MaPhong': ma_phong}, {'$set': update_data})
    return result.modified_count

def add_room_to_db(so_phong, ma_loai_phong, mo_ta, trang_thai):
    """
    Tạo document phòng mới.
    """
    room_data = {
        'MaPhong': None,  # Hoặc bạn có thể tự sinh
        'SoPhong': so_phong,
        'MaLoaiPhong': int(ma_loai_phong),
        'TrangThai': trang_thai,
        'MoTa': mo_ta,
        'created_at': datetime.utcnow()
    }
    return create_room(room_data)

def add_room_with_image(file_path, filename, so_phong, ma_loai_phong, mo_ta, image_description, trang_thai):
    """
    Tạo phòng mới kèm upload ảnh qua drive_upload.
    """
    room_id = add_room_to_db(so_phong, ma_loai_phong, mo_ta, trang_thai)
    
    # Upload file lên Drive (hoặc dịch vụ khác) để lấy URL
    from drive_upload import upload_file_to_drive
    image_url = upload_file_to_drive(file_path, filename)

    # Tạo document ảnh
    room_image_data = {
        'MaAnh': None,
        'MaPhong': room_id,  # Ở đây room_id là _id của MongoDB
        'DuongDanAnh': image_url,
        'MoTa': image_description,
        'uploaded_at': datetime.utcnow()
    }
    create_room_image(room_image_data)
    return room_id
