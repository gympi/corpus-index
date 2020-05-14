# Corpus tvzvezda.ru

### Init corpus control environments
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip

# install core requirements
pip3 install -r ../libs/requirements.txt

# install corpus control requirements
pip3 install -r ./requirements.txt
```

### Build corpus
```bash
python ./corpus build
```

### Clear corpus
```bash
python ./corpus_control.py clear
```

### Read corpus
```bash
python ./corpus_control.py read
```