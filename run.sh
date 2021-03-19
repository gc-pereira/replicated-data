docker build -t mysql-image -f db/Dockerfile .
docker run -d --rm --name mysql-container mysql-image
python3 -m venv ~/Desktop/replicated-data/.venv
source .venv/bin/activate
pip install -r main/requirements.txt
python3 main/conf_default_tables.py