import sys
import requests
import json
from datetime import datetime

JSON_FILE_NAME = '{}-github-profile.json'
FIELDS_USER = ['login', 'name', 'html_url', 'id', 'node_id', 'company', 'blog', 'location', 'email', 'bio',
               'public_repos', 'followers', 'following', 'created_at', 'updated_at']
FIELDS_REPOSITORIES = ['name', 'html_url', 'id', 'node_id', 'description', 'language', 'topics', 'default_branch',
                       'size', 'forks', 'forks_count', 'created_at', 'updated_at', 'pushed_at']


def format_date(date_string):
    if date_string is None:
        return None

    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = date_object.strftime("%m/%d/%y")
    return formatted_date


def main():
    try:
        print('Start of script execution...')

        if len(sys.argv) < 2:
            print('Enter the username as a parameter.')
            return

        if len(sys.argv) > 2:
            print('Enter only the username as a parameter.')
            return

        username = sys.argv[1]
        print(f"Trying to get information for username {username}...")
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            user_info = response.json()
            user_info = {key: user_info.get(key) for key in FIELDS_USER if user_info.get(key) is not None}
            user_info['created_at'] = format_date(user_info.get('created_at'))
            user_info['updated_at'] = format_date(user_info.get('updated_at'))

            print('User information was successfully obtained.')

            total_repos = int(user_info.get('public_repos', 0))

            if total_repos:
                print(f"Trying to get information from repositories for username {username}...")
                user_repos_list = []
                per_page = 100
                total_pages = total_repos//per_page + 1

                for page_number in range(1, total_pages+1):
                    if total_repos < per_page:
                        per_page = total_repos

                    url = f"https://api.github.com/users/{username}/repos?page={page_number}&per_page={per_page}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        for repository in response.json():
                            repository = {key: repository.get(key) for key in FIELDS_REPOSITORIES
                                          if repository.get(key) is not None}
                            repository['created_at'] = format_date(repository.get('created_at'))
                            repository['updated_at'] = format_date(repository.get('updated_at'))
                            repository['pushed_at'] = format_date(repository.get('pushed_at'))
                            user_repos_list.append(repository)

                user_info['repositories'] = user_repos_list

                print('The repository information was successfully obtained.')
                print('Trying to save information to file...')

                with open(JSON_FILE_NAME.format(username), "w", encoding="utf-8") as json_file:
                    json.dump(user_info, json_file, indent=4, ensure_ascii=False)
                    print(f'The information was saved in file {JSON_FILE_NAME.format(username)}.')
    except:
        print('ERROR! - The script did not run correctly.')
    finally:
        print("End of script execution!")


if __name__ == "__main__":
    main()
