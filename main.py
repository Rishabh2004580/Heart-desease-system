import os
import random
import subprocess
from datetime import datetime, timedelta

def get_positive_int(prompt, default=20):
    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ")
            if not user_input.strip():
                return default
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_repo_path(prompt, default="."):
    while True:
        user_input = input(f"{prompt} (default current directory): ")
        if not user_input.strip():
            return default
        if os.path.isdir(user_input):
            return user_input
        else:
            print("Directory does not exist. Please enter a valid path.")

def get_filename(prompt, default="data.txt"):
    user_input = input(f"{prompt} (default {default}): ")
    if not user_input.strip():
        return default
    return user_input

def get_date_input(prompt):
    while True:
        user_input = input(prompt + " (YYYY-MM-DD): ")
        try:
            return datetime.strptime(user_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_date_range():
    print("Enter date range for commits:")
    start_date = get_date_input("Start date")
    end_date = get_date_input("End date")
    if end_date < start_date:
        print("End date cannot be before start date. Swapping automatically.")
        start_date, end_date = end_date, start_date
    return start_date, end_date

def random_time_on_date(base_date):
    random_seconds = random.randint(0, 23*3600 + 3599)
    return base_date + timedelta(seconds=random_seconds)

def random_time_in_range(start_date, end_date):
    total_seconds = int((end_date - start_date).total_seconds())
    random_seconds = random.randint(0, total_seconds)
    return start_date + timedelta(seconds=random_seconds)

def make_commit(date, repo_path, filename, messages):
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")
    subprocess.run(["git", "add", filename], cwd=repo_path)

    # Random commit message
    message = random.choice(messages)

    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env)

def main():
    print("=" * 60)
    print("🌱 Welcome to graph-greener - GitHub Contribution Graph Commit Generator 🌱")
    print("=" * 60)

    # Pool of commit messages
    commit_messages = [
        "Algorithm Implementation Added",
        "Project File Added",
        "Algorithm Implementation Added",
        "Template File Added",
        "Notebook Added",
        "Documentation File Added",
        "Template File Added",
        "Template File Added",
        "Notebook Added",
        "New Files Added",
        "Documentation File Added",
        "New Files Added",
        "Template File Added"
    ]


    print("Choose commit mode:")
    print("1. Specific date (commits on one date at random times)")
    print("2. Date range (commits randomly across range)")

    while True:
        mode = input("Enter 1 or 2: ")
        if mode in ["1", "2"]:
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    num_commits = get_positive_int("How many commits do you want to make", 20)
    repo_path = get_repo_path("Enter the path to your local git repository", ".")
    filename = get_filename("Enter the filename to modify for commits", "data.txt")

    if mode == "1":
        base_date = get_date_input("Enter the specific date")
        commit_dates = [random_time_on_date(base_date) for _ in range(num_commits)]
    else:
        start_date, end_date = get_date_range()
        commit_dates = [random_time_in_range(start_date, end_date) for _ in range(num_commits)]

    commit_dates.sort()

    print(f"\nMaking {num_commits} commits in repo: {repo_path}\nModifying file: {filename}\n")
    for i, commit_date in enumerate(commit_dates, 1):
        print(f"[{i}/{num_commits}] Committing at {commit_date.strftime('%Y-%m-%d %H:%M:%S')}")
        make_commit(commit_date, repo_path, filename, commit_messages)

    print("\nPushing commits to your remote repository...")
    subprocess.run(["git", "push"], cwd=repo_path)
    print("✅ All done! Check your GitHub contribution graph in a few minutes.\n")
    print("Tip: Use a dedicated repository for best results. Happy coding!")

if __name__ == "_main_":
    main()