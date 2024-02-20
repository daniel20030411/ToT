# How to initialize git temp
cd "your directory"
git init

# First time using git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git remote add origin "repository URL"
#check existing URL: git remote -v
#reset URL: git remote set-url origin "New URL"
  
# Pushing file
git add "Directory of file to upload"  #git add . if wish to push whole directory
git commit -m "message"
git branch -M main
git push -u origin main

# Pull request
git checkout -b feature  #Switch to new branch "feature"
