Write-Output "Exporting MySQL database..."
mysqldump -u $env:DB_USER -p$env:DB_PASSWORD -h $env:DB_HOST $env:DB_NAME > database_dump.sql

Write-Output "Database exported. Pushing to GitHub..."
git add database_dump.sql
git commit -m "Updated database schema"
git push origin database

Write-Output "Done!"