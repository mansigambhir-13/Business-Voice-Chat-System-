# 🔐 GitHub Token Setup & Push Instructions

## Step 1: Create Personal Access Token

1. **Go to GitHub Settings:**
   - Click this link: https://github.com/settings/tokens
   - Or manually: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token:**
   - Click "Generate new token (classic)"
   - Note: `Business Voice System Push`
   - Expiration: 30 days (or your preference)

3. **Select Scopes:**
   - ✅ **repo** (all checkboxes under repo)
   - ✅ **workflow** (if you plan to use GitHub Actions)

4. **Generate & Copy Token:**
   - Click "Generate token"
   - **IMPORTANT:** Copy the token immediately (it won't be shown again!)
   - Token looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 2: Use Token to Push

### Option A: One-time Push (Recommended)
```bash
# Replace YOUR_TOKEN with your actual token
git remote set-url origin https://mansigambhir-13:YOUR_TOKEN@github.com/mansigambhir-13/Business-Voice-Chat-System-.git

# Push the code
git push -u origin main
```

### Option B: Store Credentials (Windows)
```bash
# This will prompt for username and password
git config --global credential.helper manager
git push -u origin main

# When prompted:
# Username: mansigambhir-13
# Password: YOUR_TOKEN (paste your token here, not your GitHub password)
```

### Option C: Use Environment Variable
```bash
# Set token as environment variable (Windows PowerShell)
$env:GITHUB_TOKEN = "YOUR_TOKEN"

# Then push using:
git remote set-url origin https://mansigambhir-13:$env:GITHUB_TOKEN@github.com/mansigambhir-13/Business-Voice-Chat-System-.git
git push -u origin main
```

## Step 3: Verify Success

After pushing, your repository will be available at:
**https://github.com/mansigambhir-13/Business-Voice-Chat-System-**

## 🛡️ Security Notes

- **Never commit tokens** to your repository
- **Use tokens with minimal scope** needed
- **Set expiration dates** on tokens
- **Revoke tokens** when no longer needed

## Quick Copy-Paste Command

Once you have your token, run this (replace `YOUR_TOKEN_HERE`):

```bash
git remote set-url origin https://mansigambhir-13:YOUR_TOKEN_HERE@github.com/mansigambhir-13/Business-Voice-Chat-System-.git && git push -u origin main
```

## Troubleshooting

### If you get "Support for password authentication was removed"
- You're using password instead of token. Use the token!

### If you get "Permission denied"
- Check token has `repo` scope
- Verify you're using the right account name

### If token doesn't work
- Make sure you copied the entire token
- Check it hasn't expired
- Ensure no extra spaces when pasting