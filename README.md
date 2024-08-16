
# Bloggy

A fully featured interactive Blog made with love by [@Kimanxo](https://github.com/Kimanxo) using Django & HTMX.


![Bloggy Screenshot](https://github.com/user-attachments/assets/08bc5909-cd99-40fa-ba48-2ff3e73661d6)
![Bloggy Screenshot](https://github.com/user-attachments/assets/e551a510-28d5-4373-a938-c738c5dc0308)
![image](https://github.com/user-attachments/assets/76e2724c-fb02-43c7-8f84-50585c7a0077)
![image](https://github.com/user-attachments/assets/b934f682-0565-41bc-96b3-06625c47ab8c)
![image](https://github.com/user-attachments/assets/9706fe95-1794-4730-89b1-64188ce76014)
![image](https://github.com/user-attachments/assets/427fd5c4-fbaa-41f8-80b6-484b592db3e6)




## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Interactive user interface
- Real-time updates with HTMX
- User authentication & account management
- Create, read, update, and delete posts
- Commenting system
- Tagging and categorization
- Search functionality
- Responsive design
- Share posts
- Save posts to read later
- Add posts to favourites
- voting system
- Newsletter

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 4.0 or higher
- HTMX

### Clone the Repository

```bash
git clone https://github.com/Kimanxo/bloggy.git
cd bloggy
```

### Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run the Project Locally

1. Apply migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

2. Create a superuser to access the admin panel:

    ```bash
    python manage.py createsuperuser
    ```

3. Start the development server:

    ```bash
    python manage.py runserver
    ```

4. Open your web browser and visit:

    ```
    http://127.0.0.1:8000
    ```

## Commands

- **Run Migrations:**

  ```bash
  python manage.py migrate
  ```

- **Create Superuser:**

  ```bash
  python manage.py createsuperuser
  ```

- **Start Development Server:**

  ```bash
  python manage.py runserver
  ```



## Deployment

You can view the deployed version of this blog at [bloggy.work.gd](https://bloggy.work.gd/).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Thanks to the Django community for their extensive documentation and resources.
- Special thanks to the HTMX community for enhancing the user experience.
