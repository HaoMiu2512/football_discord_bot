# Football Discord Bot

Bot Discord để thông báo tỉ số bóng đá trực tiếp.

## Tính năng
- Kết nối Discord Bot.
- Lấy dữ liệu trận đấu trực tiếp từ API bóng đá.
- Tự động kiểm tra mỗi phút và gửi thông báo khi có trận đấu mới hoặc bàn thắng/thay đổi trạng thái.

## Cài đặt

1. **Cài đặt Python và Dependencies**:
   ```bash
   # Tạo virtual environment (nếu chưa có)
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Cài đặt thư viện
   pip install -r requirements.txt
   ```

2. **Cấu hình**:
   - Bot hỗ trợ file `.env`. Hãy copy file `.env.example` thành `.env` và điền thông tin:
     ```env
     DISCORD_TOKEN=your_token
     FOOTBALL_API_KEY=your_api_key
     FOOTBALL_API_URL=https://api.football-data.org/v4 (hoặc URL api của bạn)
     DISCORD_CHANNEL_ID=id_channel_muon_gui_thong_bao
     ```

3. **Chạy Bot**:
   ```bash
   python main.py
   ```

## Cấu trúc thư mục
- `src/bot`: Logic của Discord Bot.
- `src/services`: Xử lý API bóng đá.
- `src/config.py`: Quản lý biến môi trường.
- `main.py`: File chạy chính.
