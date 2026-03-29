#!/bin/sh
set -e

# Create the DB if it doesn't exist yet (runs after the volume is mounted)
python -c "
import sys
sys.path.insert(0, '/app/src')
from database.repository import init_db, DB_PATH
init_db()
print(f'DB ready: {DB_PATH}')
"

exec python -m streamlit run src/app.py \
    --server.port=8501 \
    --server.address=0.0.0.0
