"""
Author: NSMichelJ
Crea el punto de entrada a la app
"""
from datetime import datetime

import click
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.auth.models import User

app = create_app()

@app.cli.command("createadmin", help='Create the admin to the MiniBlog')
def create_admin():
    """
    Crea el administrador del sitio
    """
    username = click.prompt('Please enter an Username', type=str, default='Admin')
    first_name = click.prompt('Please enter a First Name', type=str)
    last_name = click.prompt('Please enter a Last Name', type=str)
    email = click.prompt('Please enter an Email Address', type=str)
    password = click.prompt('Please enter a Password', hide_input=True, confirmation_prompt=True)

    if click.confirm('Do you want to continue?'):
        with app.app_context():
            try:
                admin = User(
                    username,
                    first_name,
                    last_name,
                    email,
                )

                admin.confirmed = True
                admin.confirmed_on = datetime.now()
                admin.created_password(password)
                admin.create_admin()
                admin.save()
            except IntegrityError:
                click.echo('Sorry. That username or email already exists.')

        click.echo('Well done!')
