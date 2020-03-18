from setuptools import setup
from setuptools.command.install import install
from os.path import join, dirname
import shutil
import json
import os
import sys

from michelson_kernel import __version__

kernel_json = {
    "argv": [sys.executable, "-m", "michelson_kernel", "-f", "{connection_file}"],
    "display_name": "Michelson",
    "language": "michelson",
    "codemirror_mode": "michelson"
}
kernel_js_path = join(dirname(__file__), 'michelson_kernel', 'kernel.js')


class install_with_kernelspec(install):
    def run(self):
        install.run(self)

        from jupyter_client.kernelspec import KernelSpecManager
        from tempfile import TemporaryDirectory
        kernel_spec = KernelSpecManager()
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755)  # Starts off as 700, not user readable
            shutil.copy(kernel_js_path, join(td, 'kernel.js'))
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)

            kernel_spec.install_kernel_spec(td, 'michelson', user=self.user)


with open('README.md') as f:
    readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)


setup(name='michelson-kernel',
      version=__version__,
      license='MIT',
      description='Jupyter kernel for the Michelson language',
      long_description=readme,
      long_description_content_type='text/markdown',
      author='Michael Zaikin (Baking Bad)',
      author_email='mz@baking-bad.org',
      url='https://github.com/baking-bad/michelson-kernel',
      packages=['michelson_kernel'],
      cmdclass={'install': install_with_kernelspec},
      keywords=['Tezos', 'Michelson', 'Jupyter'],
      package_data={
          'michelson_kernel': ['kernel.js'],
          '': ['README.md']
      },
      install_requires=[
          'pytezos>=2.3.5',
          'tabulate>=0.7.5',
          'jupyter-client',
          'ipykernel'
      ],
      classifiers=[
          'Intended Audience :: Developers',
          'Topic :: System :: Shells',
          'Framework :: IPython',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ])
