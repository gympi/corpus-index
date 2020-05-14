# Corpus tvzvezda.ru

### Init corpus control environments
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip

# install tvzvezda core requirements
pip3 install -r ../../tvzvezda/libs/requirements.txt

# install tags graph requirements
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