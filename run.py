from app import create_app  # This should now work correctly

app = create_app()  # Create Flask instance

if __name__ == '__main__':
    app.run(debug=True)
