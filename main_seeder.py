from db.session import Session
import os
from prod_seeder import (
    seed_disciplines
)

def run_seeder():
    db = Session()
    if not os.environ['TESTING']:
        seed_disciplines(db)
    db.close()
    
run_seeder()