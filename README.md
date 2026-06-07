# Flask Projects

A collection of web applications built with [Flask](https://flask.palletsprojects.com/), organized as standalone projects under this repository. Each project lives in its own directory with its own dependencies and entry point.

## Projects

| Project | Description | Stack |
|---------|-------------|-------|
| [**Blog**](Blog/) | **Nexus Tech** — a responsive blog-style site with home, about, post, and contact pages; contact submissions are stored in MySQL and emailed via Gmail SMTP | Flask 3.1, SQLAlchemy, Flask-Mail, Bootstrap, Jinja2 |

## Getting Started

### Prerequisites

- Python 3.10 or later
- `pip` (Python package manager)
- [MySQL](https://dev.mysql.com/downloads/) (for the Blog app)

### Run the Blog app

Each project is self-contained. To run the Blog app:

```bash
cd Blog
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

**1. Configure the database**

Create a MySQL database (default name: `nexus`) and set the connection string in [`Blog/config.json`](Blog/config.json):

```json
{
    "params": {
        "local_server": true,
        "local_uri": "mysql+pymysql://root:@localhost/nexus",
        "prod_uri": null,
        "fb_url": "https://www.facebook.com/...",
        "github_url": "https://github.com/..."
    }
}
```

Set `local_server` to `true` for local development (`local_uri`) or `false` for production (`prod_uri`).

**2. Set environment variables**

Create a `.env` file in the `Blog/` directory (see [`.gitignore`](Blog/.gitignore)):

```env
GMAIL_USERNAME=your@gmail.com
GMAIL_PASSWORD=your-app-password
```

Gmail SMTP is used to notify you when someone submits the contact form. Use a [Google App Password](https://support.google.com/accounts/answer/185833) if two-factor authentication is enabled.

**3. Start the server**

```bash
python main.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. The development server runs with debug mode enabled by default. On first run, SQLAlchemy creates the `contacts` table automatically.

## Repository Structure

```
Flask_Projects/
├── Blog/
│   ├── main.py              # Flask app, routes, database model, mail
│   ├── config.json          # Database URIs and site links
│   ├── requirements.txt     # Python dependencies
│   ├── .gitignore           # Ignores venv/ and .env
│   ├── templates/
│   │   ├── layout.html      # Shared layout (nav, footer)
│   │   ├── index.html       # Home
│   │   ├── about.html       # About
│   │   ├── post.html        # Sample post
│   │   └── contact.html     # Contact form
│   └── static/
│       ├── css/styles.css
│       ├── js/scripts.js
│       └── assets/favicon.ico
└── README.md
```

## Blog — routes

| Route | Method | Page |
|-------|--------|------|
| `/` | GET | Home |
| `/index.html` | GET | Home |
| `/about.html` | GET | About |
| `/post.html` | GET | Sample post |
| `/contact.html` | GET, POST | Contact (POST saves to DB and sends email) |

## Tech stack

- **Backend:** [Flask](https://flask.palletsprojects.com/) 3.1, [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) 3.1, [Flask-Mail](https://pythonhosted.org/Flask-Mail/)
- **Database:** MySQL via [PyMySQL](https://pypi.org/project/PyMySQL/)
- **Config:** [python-dotenv](https://pypi.org/project/python-dotenv/) for secrets, `config.json` for site settings
- **Templates:** Jinja2
- **Frontend:** Bootstrap, Font Awesome, custom CSS/JS

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-change`)
3. Commit your changes with a clear message
4. Push to your fork and open a pull request

## License

This repository is for personal and educational use. Individual projects may include third-party themes or assets; refer to each project’s files for attribution details.
