from setuptools import setup, find_packages, Command

class DisabledCommands(Command):
    user_options = []

    def initialize_options(self):
        raise Exception('This command is disabled')

    def finalize_options(self):
        raise Exception('This command is disabled')

setup(name='djedu',
        version='0.0.1',
        description='Contrived TDD example for django',
        author='Paul Collins',
        author_email='paul.collins.iii@gmail.com',
        license='MIT',
        package_dir = {'': 'votingbooth'},
        packages=find_packages('votingbooth'),
        cmdclass = {'register': DisabledCommands,
                    'upload': DisabledCommands}
        )
