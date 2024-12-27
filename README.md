

# YouTube Downloader API  

## Description  
**YouTube Downloader API** is a RESTful API built with **Django** and **Django REST Framework (DRF)** that allows downloading YouTube videos and generating a unique URL for each downloaded video.  

### Features:  
- Download YouTube videos by providing a URL.  
- Return a URL to access the downloaded video.  
- Automatically generate unique names for videos in the format `uuid4_video_name.mp4`.  

---

## Technologies Used  
- **Python 3.10+**  
- **Django 4.x**  
- **Django REST Framework**  

---

## Installation  

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/your-repo/youtube-downloader-api.git
   cd youtube-downloader-api
   ```

2. **Create and activate a virtual environment**:  
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install the dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply the migrations**:  
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:  
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints  

### 1. **Video Download**  
**POST** `/api/download/`  

- **Payload**:  
  ```json
  {
    "url": "https://www.youtube.com/watch?v=example"
  }
  ```  

- **Response**:  
  ```json
  {
    "message": "Download successful.",
    "media_url": "http://127.0.0.1:8000/media/videos/4429f76ca0114078a69f9511dfd76e2b_video_name.mp4"
  }
  ```  

---

## Deployment Example  
The project can be deployed on platforms like **Docker**, **Nginx**, or cloud services such as **Google Cloud Platform** or **AWS**.  

---

## Contribute  
Contributions are welcome! If you would like to make improvements, feel free to create a branch or submit a pull request.  

---  

## Author  
Bono Mbelle Aurélien - Full-stack developer and AI enthusiast.  