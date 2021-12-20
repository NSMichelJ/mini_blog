import argparse

from app import create_app
from app.auth.models import User

app = create_app()

def create_admin():
    parser = argparse.ArgumentParser(
        prog="MiniBlog CLI",
        usage="python entrypoint.py createadmin",
        description="Create the admin to the MiniBlog"
    )
    parser.add_argument("createadmin")
    args = parser.parse_args()
    if args.createadmin == 'createadmin':
        with app.app_context():
            username = input('Username: ')
            email = input('Email: ')
            password = input('Password: ')

            admin = User(
                username,
                'Admin',
                'Admin',
                email,
            )
            admin.created_password(password)
            admin.create_admin()
            admin.save()

    else:
        print(f'command {args.createadmin} not found, run python entrypoint.py --help')

if __name__ == '__main__':
    create_admin()
