## On the Raspberry Pi

### INSTALL DEPENDENCIES

Create a new virtual environment and install the dependencies

```bash
cd simple-web-control
mkvirtualenv -p python3 simple-web-control
workon simple-web-control
pip install -r requirements.txt
```

### RUN

```bash
python sliders.py
```

:information_source: Keep an eye on the terminal for the output of the script. Wait for the script to verify that the ROV has been armed

## On your laptop

- Open a browser and go to http://backseat.local:7860
