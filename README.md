# Quote Image Generator

A Django web application that allows users to upload a JSON file containing quotes and generates images with those quotes overlaid on background images of authors. This app is perfect for creating visually appealing Instagram posts with inspirational quotes.

## Features

- **Upload Quotes**: Users can upload a JSON file with quotes.
- **Image Generation**: Automatically generates images with quotes styled for Instagram.
- **Error Handling**: Provides feedback on upload success or failure.
- **Responsive Design**: User-friendly templates styled with CSS.

## Technologies Used

- **Django**: Web framework for building the application.
- **Pillow**: Python Imaging Library for image processing.
- **HTML/CSS**: For front-end layout and styling.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/zarjevski/quote_image_generator.git
   cd quote_image_generator
   ```
2. **Create a Virtual Environment:**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\\Scripts\\activate`
   ```
3. **Install Dependencies:**:
   ```bash
   pip install django pillow
   ```
4. **Set Up the Database:**:
   ```bash
   python manage.py migrate
   ```
5. **Run the Development Server:**:
   ```bash
   python manage.py runserver
   ```
6. **Access the App**:
   Open your web browser and go to http://127.0.0.1:8000/quotes/upload/ to start uploading quotes.

## Usage

Upload Quotes: Use the upload form to submit a JSON file containing quotes. The format should look like this:


## License

This project is licensed under the MIT License