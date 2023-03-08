
cd ..

# prepare libraries
python3.9 -m pip install --upgrade pip
pip install -r requirements.txt

# example 1
python3.9 private_pod_client.py

# example 2
python3.9 public_profile_reader.py