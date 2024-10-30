#!/usr/bin/env python3

from app import app
from models import db, Bakery, BakedGood

with app.app_context():
    # Clear existing data
    BakedGood.query.delete()
    Bakery.query.delete()
    
    # Create bakeries
    bakery1 = Bakery(name='Delightful Donuts')
    bakery2 = Bakery(name='Incredible Crullers')
    
    # Add bakeries to the session
    db.session.add(bakery1)
    db.session.add(bakery2)
    db.session.commit()  # Commit to save the bakeries to the database

    # Create baked goods associated with the bakeries
    baked_goods = [
        BakedGood(name='Chocolate Dipped Donut', price=2.75, bakery_id=bakery1.id),
        BakedGood(name='Apple-Spice Filled Donut', price=3.50, bakery_id=bakery1.id),
        BakedGood(name='Glazed Honey Cruller', price=3.25, bakery_id=bakery2.id),
        BakedGood(name='Chocolate Cruller', price=3.40, bakery_id=bakery2.id)
    ]

    # Add baked goods to the session
    db.session.add_all(baked_goods)
    db.session.commit()  # Commit to save the baked goods to the database

    print("Database seeded successfully!")
