# Aditya-L1 Science Support Cell: Data Analysis Tools

This is a [Django](https://www.djangoproject.com/) application for the Data Analysis tools of the Aditya-L1 Science Support Cell (website).

## Local Setup

### Pre-requisites

- LINUX or MacOS operating system with Git installed
- Python version >= 3.6 (i.e. often present by default on above systems and is accessible in terminal as `python3`)
- MySQL v5.7 (follow [installation guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) in MySQL docs)

### Setting up project

1. Clone the repository to your machine:

   ```bash
   git clone https://github.com/aries-res/al1ssc-tools.git
   cd al1ssc-tools

   ```

2. Create a python virtual environment named `env` (since it's already gitignored), activate it, and install all dependencies of the project:

   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Launch the [MySQL command-line client](https://dev.mysql.com/doc/refman/5.7/en/mysql.html) in your terminal and create a new empty database that will be used with this project. Exit the MySQL client.

4. Setup environment variables necessary to run the project:

   1. Copy the contents of `.env.example` in a `.env` file at the root of project.

   2. In the `.env` file, set the value of `SECRET_KEY` to a random string. It's recommended to generate it by running following command in your terminal:

      ```bash
      python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
      ```

   3. Set the `DATABASE_NAME` to the name of database you created earlier and `DATABASE_USER`, `DATABASE_PASSWORD` to username, password you used to create database respectively.

   4. (Optional) You can change the value of `DEBUG` and `ALLOWED_HOSTS` as per your needs.

5. Open the Django project directory `al1ssc_tools` and apply all of the database migrations:

   ```bash
   cd al1ssc_tools
   python manage.py migrate
   ```

6. Create an admin user (for 1st time only) who can acess the admin site:

   ```bash
   python manage.py createsuperuser
   ```

   You'll be prompted for a username, email id and password to create the account. Keep a note of them for future logins.

7. Run the development server of the project (with auto-reload enabled):

   ```bash
   python manage.py runserver
   ```

   This will start the server at http://localhost:8000 (unless you specified another port).

8. Go to http://127.0.0.1:8001/admin in your browser to open the admin site. Click on the "Bodies" model and add new bodies by filling all the input fields. Then you can make changes in [Django views](https://docs.djangoproject.com/en/3.2/topics/http/views/) logic and open the associated URL to see the effect.

### Additional Information

To learn about all the things you can do, visit [Django documentation](https://docs.djangoproject.com/en/3.2/).

<!-- TODO:
List the API routes possible
Making client-side affecting changes
 -->
