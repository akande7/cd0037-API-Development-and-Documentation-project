# Brainy Brawl API

Welcome to the Brainy Brawl API, powered by Flask! This API offers a range of features, including:

- Retrieving questions and categories.
- Searching for specific questions or categories.
- Performing CRUD (Create, Read, Update, Delete) operations on questions.

## Getting Started

Follow these steps to fork and run this app on your local machine:

1. **Clone the Repository**: Open your terminal and navigate to your preferred directory. Clone the repository to your local machine using this command:

    ```
    git clone https://github.com/akande7/brainy-brawl.git
    ```

2. **Create a Virtual Environment**: Isolate your project dependencies within a virtual environment. Run these commands:

    ```
    cd brainy-brawl
    python -m venv venv
    ```

3. **Activate the Virtual Environment**: Activate the virtual environment based on your operating system:

    - On Windows:

      ```
      venv\Scripts\activate
      ```

    - On macOS and Linux:

      ```
      source venv/bin/activate
      ```

4. **Install Dependencies**: Utilize pip to install the project's necessary dependencies:

    ```
    pip install -r requirements.txt
    ```

5. **Set Up the Database**: Configure the database connection. For a personalized experience, consider using SQLite and run this command:

    ```
    export DATABASE_URL=sqlite:///mydatabase.db  # Using SQLite
    ```

6. **Run the Application**: Initiate the Flask app with this simple command:

    ```
    flask run
    ```

7. **Access the App**: Open your web browser and visit [http://localhost:5000](http://localhost:5000).