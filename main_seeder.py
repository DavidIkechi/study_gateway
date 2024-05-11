from db.session import Session
import os
from prod_seeder import (
    seed_disciplines,
    seed_country_and_nationality,
    seed_gender_prod,
    seed_cities_prod
)

def run_seeder():
    db = Session()
    if not os.environ['TESTING']:
        seed_disciplines(db)
        seed_country_and_nationality(db)
        seed_cities_prod(db)
        seed_gender_prod(db)
    db.close()
    
run_seeder()