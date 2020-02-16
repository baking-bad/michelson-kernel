import yaml
import requests
from os.path import dirname, join
from pprint import pprint

target_path = join(dirname(dirname(__file__)), 'michelson_kernel', 'docs.py')
meta_url = 'https://gitlab.com/nomadic-labs/michelson-reference/-/raw/master/michelson-meta.yaml'
sema_url = 'https://gitlab.com/nomadic-labs/michelson-reference/-/raw/master/michelson.json'
extra = {
    'RENAME': '',
    'CAST': '',
    'TOP': '',
    'EXPAND': ''
}


def format_entry(title, descr):
    return f'{title}\n{descr}' if descr else None


def generate():
    meta_src = requests.get(meta_url).text
    meta = yaml.load(meta_src, Loader=yaml.SafeLoader)
    sema = requests.get(sema_url).json()
    docs = extra.copy()

    for section in ['instructions', 'types']:
        args_key = {'instructions': 'op_args', 'types': 'ty_args'}[section]
        for primitive, body in meta[section].items():

            docs[primitive] = format_entry(
                title=sema[section].get(primitive, dict()).get(args_key, ''),
                descr=body.get('documentation_short'))

    with open(target_path, 'w+') as f:
        f.write('docs = ')
        pprint(docs, stream=f, indent=4, width=120)


if __name__ == '__main__':
    generate()
