# Constants/Parameters

In this directory it's possible to save parameters that will be read in tests at runtime.

Example:

'''python
@pytest.mark.parametrize('path', files.parametrize('my_constants_file:required_directories'))
def test_directories(self, path):
    assert Path(path).exists()
'''

## How to Use

Files saved here can be fetched by the `files.parametrize` function with a filename and a key separated by a colon (:).
The files can be YAML or JSON and this can be detected at runtime or specified if necessary.

Example:

'''python
# constants
# -- file.json
# -- other_file.yml

# (JSON file has a "key1" in it's root)
files.parametrize('file:key1') # VALID
# It's the same as typing:
files.parametrize('file.json:key1') # VALID
# Same rules apply to YAML files
files.parametrize('other_file:key1') # VALID

# However, it is not possible to nest keys
files.parametrize('file:key1:key2') # INVALID
# Or to omit files or keys
files.parametrize(':key1') # INVALID
files.parametrize('file:') # INVALID
'''

If two files have the same name but different types (i.e. `file.json` and `file.yml` ), the YAML file will be read.

### Exceptions raised

If the file is not found, a **FileNotFound** exception will be raised.
If the key is not found, a **KeyError** exception will be raised.

## JSON file example

'''json
// constants/file.json
{
    "ke1": [
        "value1",
        "value2"
    ],
    "key2": [
        "value1",
        "value2"
    ]
}
'''

## YAML file example
'''yaml
# constants/file.yml
key1:
 - value1
 - value2
key2:
 - value1
 - value2
'''
