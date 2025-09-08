from peewee import *
from playhouse.migrate import *
from backend.database import db
from backend.models import Screen

def add_sample_r1r2_column():
    with db.atomic():
        if not Screen._meta.database.table_exists('screen'):
            print("Table 'screen' does not exist. Creating it...")
            Screen._meta.database.create_tables([Screen])
            print("Table 'screen' created.")
        
        migrator = SchemaMigrator(db)
        
        # Check if the column already exists to prevent errors on re-run
        columns = db.get_columns('screen')
        column_names = [col.name for col in columns]

        if 'sample_r1r2' not in column_names:
            print("Adding 'sample_r1r2' column to 'screen' table...")
            migrate(
                migrator.add_column('screen', 'sample_r1r2', TextField(null=True))
            )
            print("'sample_r1r2' column added successfully.")
        else:
            print("'sample_r1r2' column already exists in 'screen' table. Skipping migration.")

if __name__ == "__main__":
    db.connect()
    add_sample_r1r2_column()
    db.close()
