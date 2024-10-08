import argparse
from db.session import Session
import os
from prod_seeder import (
    seed_disciplines,
    seed_country_and_nationality,
    seed_gender_prod,
    seed_cities_prod,
    seed_states_prod,
    seed_country_codes,
    seed_degrees, seed_degree_sought,
    seed_courses, seed_package,
    seed_pricing, seed_languages, seed_universities,
    seed_admin_user, seed_colleges, seed_us_states, seed_locations,
    seed_degree_types, seed_university_cities
)

def run_all_seeders(db):
    if not os.environ['TESTING']:
        seed_disciplines(db)
        seed_country_and_nationality(db)
        seed_cities_prod(db)
        seed_gender_prod(db) 
        seed_states_prod(db)
        seed_country_codes(db)
        seed_degrees(db)
        seed_degree_sought(db)
        seed_courses(db)
        seed_package(db)
        seed_pricing(db)
        seed_languages(db)
        seed_admin_user(db)
        seed_universities(db)
        seed_colleges(db)
        seed_us_states(db)
        seed_locations(db)
        seed_degree_types(db)
        seed_university_cities(db)
    
def run_seeder(seeder: str = None):
    db = Session()
    if not os.environ['TESTING']:
        if seeder == 'disciplines':
            seed_disciplines(db)
        elif seeder == 'country_and_nationality':
            seed_country_and_nationality(db)
        elif seeder == 'cities':
            seed_cities_prod(db)
        elif seeder == 'gender':
            seed_gender_prod(db)
        elif seeder == 'states':
            seed_states_prod(db)
        elif seeder == 'codes':
            seed_country_codes(db)
        elif seeder == 'degrees':
            seed_degrees(db)
        elif seeder == 'degree_sought':
            seed_degree_sought(db)
        elif seeder == 'courses':
            seed_courses(db)
        elif seeder == 'package':
            seed_package(db)
        elif seeder == 'pricing':
            seed_pricing(db)
        elif seeder == 'languages':
            seed_languages(db)
        elif seeder == 'universities':
            seed_universities(db)
        elif seeder == 'admin':
            seed_admin_user(db)
        elif seeder == 'colleges':
            seed_colleges(db)  
        elif seeder == 'us_states':
            seed_us_states(db)
        elif seeder == 'locations':
            seed_locations(db)
        elif seeder == "degree_types":
            seed_degree_types(db)
        elif seeder == "university_city":
            seed_university_cities(db)
        elif seeder is None or seeder.strip() == "":
            run_all_seeders(db)
            
    db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a specific seeder.')
    parser.add_argument('seeder', type=str, help='The name of the seeder to run.')
    args = parser.parse_args()
    run_seeder(args.seeder)
