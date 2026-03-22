from setuptools import setup

package_name = 'arm_trajectory_planner'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='qiulong',
    maintainer_email='qiulongqu@gmail.com',
    description='Joint space trajectory planner for 6-DOF robotic arm',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_trajectory_planner = arm_trajectory_planner.joint_trajectory_planner:main',
            'planned_to_joint_state = arm_trajectory_planner.planned_to_joint_state:main',
            'auto_demo_publisher = arm_trajectory_planner.auto_demo_publisher:main',
        ],
    },
)
