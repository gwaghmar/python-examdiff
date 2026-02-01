# PowerShell script to set up GitHub repository for Python ExamDiff Pro
# Run this script after creating the repository on GitHub

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepositoryName = "python-examdiff"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python ExamDiff Pro - GitHub Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Host "✗ Error: main.py not found. Please run this script from the EXAMDIFF directory." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Found project files" -ForegroundColor Green
Write-Host ""

# Initialize git repository if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
}

# Update README.md with GitHub username
Write-Host "Updating README.md with GitHub username..." -ForegroundColor Yellow
$readmeContent = Get-Content "README.md" -Raw
$readmeContent = $readmeContent -replace "YOUR_USERNAME", $GitHubUsername
$readmeContent = $readmeContent -replace "yourusername", $GitHubUsername
Set-Content "README.md" -Value $readmeContent -NoNewline
Write-Host "✓ README.md updated" -ForegroundColor Green

# Update pyproject.toml with GitHub username
Write-Host "Updating pyproject.toml with GitHub username..." -ForegroundColor Yellow
$pyprojectContent = Get-Content "pyproject.toml" -Raw
$pyprojectContent = $pyprojectContent -replace "YOUR_USERNAME", $GitHubUsername
Set-Content "pyproject.toml" -Value $pyprojectContent -NoNewline
Write-Host "✓ pyproject.toml updated" -ForegroundColor Green

# Update CHANGELOG.md with GitHub username
Write-Host "Updating CHANGELOG.md with GitHub username..." -ForegroundColor Yellow
$changelogContent = Get-Content "CHANGELOG.md" -Raw
$changelogContent = $changelogContent -replace "YOUR_USERNAME", $GitHubUsername
Set-Content "CHANGELOG.md" -Value $changelogContent -NoNewline
Write-Host "✓ CHANGELOG.md updated" -ForegroundColor Green

# Add all files
Write-Host ""
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host ""
    Write-Host "Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: Python ExamDiff Pro - Professional file comparison tool"
    Write-Host "✓ Initial commit created" -ForegroundColor Green
} else {
    Write-Host "✓ No changes to commit" -ForegroundColor Green
}

# Set up remote
Write-Host ""
Write-Host "Setting up GitHub remote..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/$GitHubUsername/$RepositoryName.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl
Write-Host "✓ Remote added: $remoteUrl" -ForegroundColor Green

# Set default branch to main
Write-Host ""
Write-Host "Setting default branch to 'main'..." -ForegroundColor Yellow
git branch -M main 2>$null
Write-Host "✓ Branch set to 'main'" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create the repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host "   Repository name: $RepositoryName" -ForegroundColor White
Write-Host "   DO NOT initialize with README, .gitignore, or license" -ForegroundColor White
Write-Host ""
Write-Host "2. Push to GitHub:" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Add screenshots to docs/screenshots/ (optional but recommended)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Repository URL: $remoteUrl" -ForegroundColor Cyan
Write-Host ""
