# 1. Check current status (see what's changed)
git status

# 2. Initialize a git repo (only needed ONCE per project, if not already a repo)
git init

# 3. Stage your changes
git add .              # stages everything
# or
git add filename.py    # stages just one file

# 4. Commit the staged changes with a message
git commit -m "Add Book and Member classes"

# 5. Link your local repo to GitHub (only needed ONCE, first time)
git remote add origin https://github.com/yourusername/your-repo.git

# 6. Push to GitHub
git branch -M main         # rename default branch to 'main' (first time only)
git push -u origin main    # first push, sets upstream



git status
git add .
git commit -m "your message here"
git push