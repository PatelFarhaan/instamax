from project import db
from project.admin.models import Admin


Admin.query.delete()
new_admin = Admin(email='admin',
                  password='admin')
db.session.add(new_admin)
db.session.commit()

print("Done!!!")