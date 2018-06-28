# flox

## Development 

```bash
git clone
python setup.py develop
```

### Install plugins in develop mode

```bash
pip install -e plugin-repository#plugin-name --src=.
```

example:

```bash
pip install -e git+ssh://git@github.com:getflox/flox-terraform#flox-terraform --src=.
```
