# Passive-subdomain-enumeration-tool
An automatic tool that uses 4 different tools to get info about a target.

You will need to download 4 tools to use this one :
1.sudo apt update && sudo apt install jq -y
2.sudo apt install subfinder -y
3.sudo apt install httpx-toolkit -y
4.go install github.com/gwen001/github-subdomains@latest (also you will need to move this one sudo cp ~/go/bin/github-subdomains /usr/local/bin/)

You are gonna need a github token to use the github tool which you create from github then in kali linux you run
nano ~/.zshrc
inside the file you paste this in the end
export GITHUB_TOKEN="ghp_your_actual_token_here"
once you save the file you run
source ~/.zshrc
you run it in the command line with this:
recon -d thetargetdomain
you can use multiple domains by seperating them with commas
