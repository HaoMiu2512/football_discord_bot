# ⚽ Football Discord Bot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0%2B-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Bot Discord mạnh mẽ giúp bạn theo dõi tỉ số bóng đá trực tiếp, lịch thi đấu, bảng xếp hạng và thông tin đội bóng từ khắp các giải đấu hàng đầu thế giới.

## ✨ Tính Năng Nổi Bật

- **🔔 Thông báo trực tiếp**: Tự động gửi tin nhắn khi có bàn thắng hoặc trận đấu mới bắt đầu/kết thúc (Live Score Updates).
- **📅 Lịch thi đấu & Kết quả**: Xem lịch hôm nay, kết quả các trận vừa đá xong.
- **📊 Bảng xếp hạng & Vua phá lưới**: Cập nhật BXH và danh sách ghi bàn của EPL, La Liga, Serie A, Champions League, v.v.
- **🛡️ Thông tin chi tiết**: Tra cứu thông tin Đội bóng, Cầu thủ, HLV, Sân vận động.
- **🤖 Slash Commands**: Hỗ trợ lệnh `/` hiện đại, dễ sử dụng với menu gợi ý.

## 🛠️ Cài Đặt

### 1. Yêu cầu hệ thống
- Python 3.8 trở lên.
- Đã cài đặt `git`.
- Một tài khoản [Football-Data.org API](https://www.football-data.org/) (Miễn phí).
- Một [Discord Bot Token](https://discord.com/developers/applications).

### 2. Clone và cài đặt thư viện

```bash
# Clone repository
git clone https://github.com/HaoMiu2512/football_discord_bot.git
cd football_discord_bot

# Tạo môi trường ảo (khuyến nghị)
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows:
.\venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 3. Cấu hình

Tạo file `.env` từ file mẫu `.env.example` và điền thông tin của bạn:

```bash
cp .env.example .env
```

Nội dung file `.env`:
```env
DISCORD_TOKEN=your_discord_bot_token
FOOTBALL_API_KEY=your_football_api_key
FOOTBALL_API_URL=https://api.football-data.org/v4
DISCORD_CHANNEL_ID=your_channel_id_for_notifications
```
*Lưu ý: `DISCORD_CHANNEL_ID` là ID của kênh mà bot sẽ gửi thông báo tỉ số tự động.*

### 4. Khởi chạy Bot

```bash
python main.py
```

## 🎮 Hướng Dẫn Sử Dụng

Sau khi mời bot vào server, hãy dùng lệnh `!sync` (chỉ lần đầu hoặc khi cập nhật bot) để đồng bộ các lệnh Slash.

### Các lệnh phổ biến:

| Lệnh | Mô tả | Ví dụ |
| :--- | :--- | :--- |
| `/live` | Xem các trận đấu đang diễn ra trực tiếp | `/live` |
| `/today` | Xem lịch thi đấu & kết quả hôm nay | `/today` |
| `/standings [mã]` | Xem bảng xếp hạng giải đấu | `/standings PL` |
| `/scorers [mã]` | Xem danh sách vua phá lưới | `/scorers CL` |
| `/team [id]` | Xem thông tin chi tiết đội bóng | `/team 65` |
| `/match [id]` | Xem chi tiết diễn biến trận đấu | `/match 1234` |
| `/team-next [id]` | Xem trận tiếp theo của đội | `/team-next 65` |
| `/team-last [id]` | Xem trận gần nhất của đội | `/team-last 65` |
| `/help` | Xem danh sách toàn bộ các lệnh | `/help` |

### Mã giải đấu phổ biến (Code):
- **PL**: Premier League (Anh)
- **PD**: La Liga (Tây Ban Nha)
- **SA**: Serie A (Ý)
- **BL1**: Bundesliga (Đức)
- **FL1**: Ligue 1 (Pháp)
- **CL**: UEFA Champions League

## 📂 Cấu Trúc Dự Án

```
football_discord_bot/
├── src/
│   ├── bot/
│   │   ├── cogs/          # Modules lệnh (Commands)
│   │   └── discord_bot.py # Bot core logic
│   ├── services/          # Xử lý API bóng đá
│   └── config.py          # Quản lý cấu hình
├── main.py                # File khởi chạy
├── .env                   # Biến môi trường (Token/Key)
└── requirements.txt       # Danh sách thư viện
```

## 🤝 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Hãy tạo Pull Request hoặc mở Issue nếu bạn tìm thấy lỗi.

## 📝 License

Dự án này được phát hành dưới giấy phép MIT.
