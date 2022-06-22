touch .env
echo 'DB_ENGINE=${{ secrets.DB_ENGINE }}' >> .env
echo 'DB_NAME=${{ secrets.DB_NAME }}' >> .env
echo 'POSTGRES_USER=${{ secrets.POSTGRES_USER }}' >> .env
echo 'POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}' >> .env
echo 'DB_HOST=${{ secrets.DB_HOST }}' >> .env
echo 'DB_PORT=${{ secrets.DB_PORT }}' >> .env
echo 'ALLOWED_HOSTS=${{ secrets.ALLOWED_HOSTS }}' >> .env
echo 'ENTER_PASS=${{ secrets.ENTER_PASS }}' >> .env
echo 'SECRET_KEY=${{ secrets.SECRET_KEY }}' >> .env