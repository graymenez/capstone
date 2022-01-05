from models import db,User,MedicalCenter,UserMedicalCenter
from app import app

# def drop_everything():
#     """(On a live db) drops all foreign key constraints before dropping all tables.
#     Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
#     (https://github.com/pallets/flask-sqlalchemy/issues/722)
#     """
#     from sqlalchemy.engine.reflection import Inspector
#     from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

#     con = db.engine.connect()
#     trans = con.begin()
#     inspector = Inspector.from_engine(db.engine)

#     # We need to re-create a minimal metadata with only the required things to
#     # successfully emit drop constraints and tables commands for postgres (based
#     # on the actual schema of the running instance)
#     meta = MetaData()
#     tables = []
#     all_fkeys = []

#     for table_name in inspector.get_table_names():
#         fkeys = []

#         for fkey in inspector.get_foreign_keys(table_name):
#             if not fkey["name"]:
#                 continue

#             fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

#         tables.append(Table(table_name, meta, *fkeys))
#         all_fkeys.extend(fkeys)

#     for fkey in all_fkeys:
#         con.execute(DropConstraint(fkey))

#     for table in tables:
#         con.execute(DropTable(table))

#     trans.commit()

# drop_everything()
db.drop_all()
db.create_all()

first_name = ['Chris','Katy','John','Richard']
last_name = ['Kyle','Ferris','Wick','Dickerson']
title = ['Paramedic','Firefighter','Police Officer','EMT-B']
email = ['ChrisK@example.com','KatyF@example.com','JohnW@example.com','RichardD@example.com']
pwd = ['Paramedic101','Firefighter101','Police101','EMT101']

new_users = [User.register(first_name=f,last_name=l,title=t,email=e,pwd=p)for f,l,t,e,p in zip(first_name,last_name,title,email,pwd)]

db.session.add_all(new_users)
db.session.commit()