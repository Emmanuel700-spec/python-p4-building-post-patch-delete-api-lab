import json
from flask import Flask
from app import app
from models import db, Bakery, BakedGood

class TestApp:
    '''Flask application in flask_app.py'''

    def test_creates_baked_goods(self):
        '''can POST new baked goods through "/baked_goods" route.'''

        with app.app_context():
            # Clean up any existing baked good with the same name
            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if af:
                db.session.delete(af)
                db.session.commit()

            # Create a new baked good
            response = app.test_client().post(
                '/baked_goods',
                json={  # Use json argument for proper content type
                    "name": "Apple Fritter",
                    "price": 2.00,
                    "bakery_id": 5,  # Ensure this bakery ID exists
                },
                content_type='application/json'  # Set content type to JSON
            )

            af = BakedGood.query.filter_by(name="Apple Fritter").first()

            # Assertions
            assert response.status_code == 201
            assert response.content_type == 'application/json'
            assert af is not None  # Check that the baked good was created
            assert af.id is not None  # Check that it has an ID

    def test_updates_bakeries(self):
        '''can PATCH bakeries through "bakeries/<int:id>" route.'''

        with app.app_context():
            # Update an existing bakery
            mb = Bakery.query.filter_by(id=1).first()
            if not mb:
                # Create a bakery for testing purposes if it doesn't exist
                mb = Bakery(name="Initial Bakery")
                db.session.add(mb)
                db.session.commit()

            # PATCH the bakery's name
            response = app.test_client().patch(
                '/bakeries/1',
                json={  # Use json argument for proper content type
                    "name": "Your Bakery",
                },
                content_type='application/json'  # Set content type to JSON
            )

            # Assertions
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert mb.name == "Your Bakery"

    def test_deletes_baked_goods(self):
        '''can DELETE baked goods through "baked_goods/<int:id>" route.'''

        with app.app_context():
            # Ensure the baked good exists before deleting
            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if not af:
                af = BakedGood(
                    name="Apple Fritter",
                    price=2.00,
                    bakery_id=5,  # Ensure this bakery ID exists
                )
                db.session.add(af)
                db.session.commit()

            # Delete the baked good
            response = app.test_client().delete(
                f'/baked_goods/{af.id}',
                content_type='application/json'  # Set content type to JSON
            )

            # Assertions
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert BakedGood.query.filter_by(name="Apple Fritter").first() is None  # Ensure it was deleted
