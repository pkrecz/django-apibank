SELECT 'CREATE DATABASE apibankdb' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'apibankdb')\gexec
