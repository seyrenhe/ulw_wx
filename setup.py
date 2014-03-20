import uliweb
from uliweb.utils.setup import setup
import apps

__doc__ = """doc"""

setup(name='ulw_wx',
    version=apps.__version__,
    description="Description of your project",
    package_dir = {'ulw_wx':'apps'},
    packages = ['ulw_wx'],
    include_package_data=True,
    zip_safe=False,
)
