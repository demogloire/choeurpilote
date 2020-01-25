import unittest
import os
from flask_testing import TestCase
from flask import url_for, abort
from app import create_app, db

from app.models import User, Categorie
    

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='gloire', server='localhost', database='test_echo')
        )
        return app

    
class TestViews(TestBase):
        
    def test_listedroit_view(self):
        """
        Accessibilité à la liste
        """
        response = self.client.get(url_for('siteweb.index'))
        self.assertEqual(response.status_code, 200)
    
if __name__ == '__main__':
    unittest.main()