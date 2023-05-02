from website import create_app

app = create_app()

# if the file is started from a script acrivate the debug
if __name__ == '__main__':
    app.run(debug=True)