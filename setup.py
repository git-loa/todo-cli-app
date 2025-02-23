from setuptools import setup, find_packages

setup(name="todo-cli-app",
      version="0.1.0",
      author="Leonard Okyere Afeke"
      author_email="leo.afeke@outlook.com"
      description="A command-line to-d list application",
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      url="https://github.com/git-loa/todo-cli-app",
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'psycopg2',
          #Add other dependencies here
      ],
      
)