from github import Github
from getpass import getpass
import re, sys, os

def login(username, password):
    try:
        login = Github(username, password)
        user = login.get_user()
    except Exception as error:
        print(error)
    repos = []
    repo_full_names = []
    for repo in user.get_repos():
        repos.append(repo)
        repo_full_names.append(repo.full_name)
    print("Logged in successfully !")
    print("Your repos:\n" + "\n".join(repo_full_names))
    return user, repos

def create_repo_by_name(user, repo_name):
    try:
        user.create_repo(repo_name)
        print("Repo created as: ", end="")
        print(user.get_repo(repo_name).full_name)
    except Exception as error:
        print("Error in creating repo")
        print(error)

def delete_repo_by_name(user, name):
    try:
        user.get_repo(name).delete()
        print("Deleted")
    except Exception as error:
        print(error)

def border(number=None):
    if number == None:
        print("="*50) 
    else:
        print("="*number)

def start_github_vault():
    username = input("Enter your username: ").strip()
    password = getpass()
    border()
    global user
    try:
        user, repos = login(username, password)
    except Exception as error:
        print(error)
        return start_github_vault()
    while True:
        command = input("Enter command: ").strip()
        # patterns go here
        pattern_create = r"create \[([a-zA-Z0-9\s_\.,\$\-/]+)\]" # create [Test_Project]
        pattern_delete = r"delete \[([a-zA-Z0-9\s_\.,\$\-/]+)\]" # delete [Test_Project]
        pattern_get = r"get \[([a-zA-Z0-9\s_\.,\$\-/]+)\]" # get repo name
        # patterns till here
        repo_creation = re.search(pattern_create, command)
        repo_deletion = re.search(pattern_delete, command)
        repo_getter = re.search(pattern_get, command)
        if repo_creation != None:
            repo_name = repo_creation.group(1).strip()
            create_repo_by_name(user, repo_name)

        elif repo_deletion != None:
            repo_name = repo_deletion.group(1).strip()
            delete_repo_by_name(user, repo_name)
        
        elif repo_getter != None:
            try:
                repo = user.get_repo(repo_getter.group(1).strip())
                print("Repo present as: ", end="")
                print(repo.full_name)
            except Exception as error:
                print(error)

        elif "exit" in command:
            print("Exiting...")
            sys.exit(0)
        
        elif "show" in command:
            repos = user.get_repos()
            print()
            for repo in repos:
                print(repo.full_name)
            print()
        
        elif "log" in command and "out" in command:
            return start_github_vault()

        else:
            print("Command not recognized")
        border()

def get_repo_by_name(user, repo_name):
    try:
        repo = user.get_repo(repo_name)
        print(repo.full_name)
    except Exception as error:
        print(error)

def main():
    try:
        os.system("clear")
    except Exception:
        pass
    while True: start_github_vault()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram ended !")