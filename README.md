# 🎵 Open Source Music Platform — Django Backend

A RESTful API backend for a collaborative music platform, built with Django & Django Rest Framework.
Enables artists to upload tracks, manage profiles, and allows users to browse, like, and interact with music content.

---

## 📂 Project Structure

```
music_platform/         # Django Project Settings
catalog/                # App for Track Management & API
    models.py           # Track & Artist Models
    views.py            # API Views
    serializers.py      # DRF Serializers
    urls.py             # App URLs
    migrations/         
manage.py               # Django CLI
requirements.txt        # Project Dependencies
db.sqlite3              # Dev Database (SQLite)
```

---

## 🛠 Features

* ✅ **User Authentication (JWT)**
* ✅ **Track Upload with Metadata & Cover**
* ✅ **Artist Profiles**
* ✅ **Track Listing & Filtering**
* ✅ **Like System**
* ✅ **Playlist Creation (Coming Soon)**
* ✅ **Open Contribution Ready**

---

## 🚀 API Endpoints Overview

| Endpoint              | Method | Description         |
| --------------------- | ------ | ------------------- |
| `/api/tracks/`        | GET    | List All Tracks     |
| `/api/tracks/upload/` | POST   | Upload a New Track  |
| `/api/auth/register/` | POST   | Register a New User |
| `/api/auth/login/`    | POST   | Obtain JWT Token    |

---

## 🔑 Authentication

Uses **JWT Authentication** provided by `djangorestframework-simplejwt`.

Example Auth Headers:

```
Authorization: Bearer <your_token>
```

---

## 📥 Installation & Setup

```bash
# Clone Repo
git clone https://github.com/your-repo/open-music-platform.git
cd open-music-platform

# Install Dependencies
pip install -r requirements.txt

# Apply Migrations
python manage.py migrate

# Create Superuser (Optional)
python manage.py createsuperuser

# Run Dev Server
python manage.py runserver
```

---

## 🛡 Contributing

We welcome contributions from the community!

* Fork this repo
* Open an issue for discussion
* Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

