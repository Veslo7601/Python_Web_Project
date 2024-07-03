# PhotoShare a web service

To run the project, you need an ```.env``` file with environment variables. Create it with the following content and replace 
with your own values.


 Create and configure your `.env` file:
```bash
cp .env.example .env
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Veslo7601/Python_Web_Project.git
```

2. Create a virtual environment (recommended) and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies using requirements.txt:

```bash
pip install -r requirements.txt
```

### **Add ```.env``` file**

4. Set up the database:

```bash
docker compose up --build
```

5. Run the application:

The launch of the application will occur in the container