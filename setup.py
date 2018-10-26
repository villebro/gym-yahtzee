from setuptools import find_packages, setup


setup(
    name='gym_yahtzee',
    version='0.9.1',
    description='Yahtzee game engine for OpenAI Gym',
    author='Ville Brofeldt',
    author_email='ville.brofeldt@iki.fi',
    maintainer='Ville Brofeldt',
    maintainer_email='ville.brofeldt@iki.fi',
    url='https://github.com/villebro/gym-yahtzee',
    license='MIT',
    packages=find_packages(exclude='tests'),
    install_requires=[
        'gym',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)
