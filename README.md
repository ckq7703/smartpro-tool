# SmartPro Tools - Nền tảng SaaS Tự động hóa Văn bản Word chuyên nghiệp

SmartPro Tools là một giải pháp SaaS mạnh mẽ giúp tự động hóa quy trình định dạng (reformat) và quản lý tài liệu Microsoft Word. Được thiết kế dành cho các báo cáo kỹ thuật phức tạp, ứng dụng giúp đồng bộ phong cách văn bản chỉ trong vài giây.

![Logo](static/img/logo.png)

## 🚀 Tính năng nổi bật

- **Smart Reformat**: Tự động nhận diện cấu trúc bản thảo dựa trên kích thước font chữ và gán các Style định danh của SmartPro (H1, H2, H3, Bullet points...).
- **Quản lý Template**: Cho phép người dùng tải lên, lưu trữ và xem trước (preview) các mẫu văn bản Word trực tiếp trên trình duyệt.
- **Xác thực Google OAuth2**: Đăng nhập an toàn và nhanh chóng thông qua tài khoản Google.
- **Lịch sử báo cáo**: Lưu trữ và quản lý tập trung toàn bộ các phiên bản báo cáo đã xuất bản.
- **Hệ thống Phân quyền (RBAC)**: Phân biệt quyền hạn giữa Admin (toàn quyền quản trị) và User (quản lý dữ liệu cá nhân).
- **Hỗ trợ Docker**: Sẵn sàng triển khai nhanh chóng với Docker và Docker Compose.

## 🛠️ Công nghệ sử dụng

- **Backend**: Python (FastAPI)
- **Database**: MySQL (XAMPP / Docker)
- **Frontend**: HTML5, Vanilla CSS, Javascript (với Lucide Icons)
- **Xử lý văn bản**: `python-docx`, `docxcompose`
- **Xác thực**: JWT (JSON Web Tokens), Google Identity Services
- **Hạ tầng**: Docker, Docker Compose

## 📦 Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
- Python 3.10+
- MySQL Server (XAMPP) hoặc Docker Desktop

### 2. Cài đặt thủ công (Local)
1. Clone dự án:
   ```bash
   git clone https://github.com/ckq7703/smartpro-tool.git
   cd smartpro-tool
   ```
2. Cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```
3. Cấu hình file `.env`:
   - Copy file `.env` và điền các thông tin: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `GOOGLE_CLIENT_ID`, `SECRET_KEY`.
4. Khởi chạy server:
   ```bash
   uvicorn main:app --reload
   ```

### 3. Cài đặt bằng Docker (Khuyên dùng)
Dự án đã được cấu hình sẵn Docker Compose bao gồm cả App và Database:
```bash
docker-compose up -d
```
Ứng dụng sẽ khả dụng tại địa chỉ: `http://localhost:8000`

## 🔐 Cấu hình bảo mật và Admin
- Mặc định khi khởi chạy lần đầu, hệ thống sẽ tự động tạo tài khoản Admin:
  - **User**: `smartproadmin`
  - **Pass**: `smartproadmin`
- Hãy đảm bảo thay đổi `SECRET_KEY` trong file `.env` trước khi đưa lên môi trường Production.

## 📄 Giấy phép
Sản phẩm được phát triển bởi **SmartPro Team**. Bản quyền thuộc về ckq7703.

---
📫 **Liên hệ hỗ trợ**: [GitHub ckq7703](https://github.com/ckq7703)
