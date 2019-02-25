from project import app,db


class main_run():
    def run(self):
        db.create_all()
        app.run(debug=True)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)