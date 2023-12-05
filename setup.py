from setuptools import find_packages, setup

package_name = 'pointCloud2_to_csv'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='curious',
    maintainer_email='curious.ks.jp@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
          'point_cloud2_to_csv_converter = pointCloud2_to_csv.point_cloud2_to_csv_converter:main',
        ],
    },
)
