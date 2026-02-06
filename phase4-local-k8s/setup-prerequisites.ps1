# Phase 4 Prerequisites Setup Script
# This script will guide you through installing the required tools for Phase 4 deployment

Write-Host "===========================================" -ForegroundColor Green
Write-Host "Cloud Native Todo Chatbot - Phase 4 Setup" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

Write-Host "This script will help you install the required tools for Phase 4 deployment:" -ForegroundColor Yellow
Write-Host "1. Docker Desktop" -ForegroundColor White
Write-Host "2. kubectl" -ForegroundColor White
Write-Host "3. Minikube" -ForegroundColor White
Write-Host "4. Helm" -ForegroundColor White
Write-Host ""

Write-Host "Prerequisites:" -ForegroundColor Cyan
Write-Host "- Windows 10/11 with WSL 2 (for Docker)" -ForegroundColor Gray
Write-Host "- Administrator rights to install software" -ForegroundColor Gray
Write-Host "- Internet connection" -ForegroundColor Gray
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  Warning: This script should be run as Administrator for proper installations." -ForegroundColor Red
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "Please run this script as Administrator and try again." -ForegroundColor Red
        exit
    }
}

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $exists = $null -ne (Get-Command $command -ErrorAction SilentlyContinue)
    return $exists
}

# Check current status
Write-Host "`nChecking current installation status..." -ForegroundColor Cyan

$dockerInstalled = Test-CommandExists "docker"
$kubectlInstalled = Test-CommandExists "kubectl"
$minikubeInstalled = Test-CommandExists "minikube"
$helmInstalled = Test-CommandExists "helm"

Write-Host "Docker: " -NoNewline
if ($dockerInstalled) { Write-Host "INSTALLED" -ForegroundColor Green } else { Write-Host "MISSING" -ForegroundColor Red }

Write-Host "kubectl: " -NoNewline
if ($kubectlInstalled) { Write-Host "INSTALLED" -ForegroundColor Green } else { Write-Host "MISSING" -ForegroundColor Red }

Write-Host "Minikube: " -NoNewline
if ($minikubeInstalled) { Write-Host "INSTALLED" -ForegroundColor Green } else { Write-Host "MISSING" -ForegroundColor Red }

Write-Host "Helm: " -NoNewline
if ($helmInstalled) { Write-Host "INSTALLED" -ForegroundColor Green } else { Write-Host "MISSING" -ForegroundColor Red }

Write-Host ""
$installAll = Read-Host "Would you like to install all missing tools? (y/n)"

if ($installAll -eq 'y' -or $installAll -eq 'Y') {
    # Install Chocolatey if not present (package manager for Windows)
    $chocoInstalled = Test-CommandExists "choco"
    if (-not $chocoInstalled) {
        Write-Host "`nInstalling Chocolatey package manager..." -ForegroundColor Cyan
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }

    # Install tools using Chocolatey
    if (-not $dockerInstalled) {
        Write-Host "`nInstalling Docker Desktop..." -ForegroundColor Cyan
        Write-Host "Note: This will download and install Docker Desktop." -ForegroundColor Yellow
        Write-Host "After installation, you will need to restart your computer." -ForegroundColor Yellow
        Write-Host "Docker requires WSL 2 on Windows. Make sure WSL 2 is enabled." -ForegroundColor Yellow

        $confirm = Read-Host "Continue with Docker installation? (y/n)"
        if ($confirm -eq 'y' -or $confirm -eq 'Y') {
            choco install docker-desktop -y
            Write-Host "Docker Desktop installed. Please restart your computer before continuing." -ForegroundColor Green
        } else {
            Write-Host "Skipping Docker installation." -ForegroundColor Yellow
        }
    }

    if (-not $kubectlInstalled) {
        Write-Host "`nInstalling kubectl..." -ForegroundColor Cyan
        choco install kubernetes-cli -y
        Write-Host "kubectl installed." -ForegroundColor Green
    }

    if (-not $minikubeInstalled) {
        Write-Host "`nInstalling Minikube..." -ForegroundColor Cyan
        choco install minikube -y
        Write-Host "Minikube installed." -ForegroundColor Green
    }

    if (-not $helmInstalled) {
        Write-Host "`nInstalling Helm..." -ForegroundColor Cyan
        choco install kubernetes-helm -y
        Write-Host "Helm installed." -ForegroundColor Green
    }

    Write-Host "`nInstallation process completed!" -ForegroundColor Green
    Write-Host "Please restart your computer if Docker was installed." -ForegroundColor Yellow
    Write-Host "After restarting, run this script again to verify installations." -ForegroundColor Yellow
} else {
    Write-Host "`nYou chose not to install tools automatically." -ForegroundColor Yellow
    Write-Host "Here are manual installation instructions:" -ForegroundColor Cyan

    Write-Host "`n1. Docker Desktop:" -ForegroundColor White
    Write-Host "   - Go to https://www.docker.com/products/docker-desktop" -ForegroundColor Gray
    Write-Host "   - Download and install Docker Desktop" -ForegroundColor Gray
    Write-Host "   - Make sure to enable WSL 2 integration if on Windows" -ForegroundColor Gray

    Write-Host "`n2. kubectl:" -ForegroundColor White
    Write-Host "   - Go to https://kubernetes.io/docs/tasks/tools/install-kubectl/" -ForegroundColor Gray
    Write-Host "   - Download the latest release for Windows" -ForegroundColor Gray
    Write-Host "   - Add to your PATH environment variable" -ForegroundColor Gray

    Write-Host "`n3. Minikube:" -ForegroundColor White
    Write-Host "   - Go to https://minikube.sigs.k8s.io/docs/start/" -ForegroundColor Gray
    Write-Host "   - Download the Windows installer" -ForegroundColor Gray
    Write-Host "   - Add to your PATH environment variable" -ForegroundColor Gray

    Write-Host "`n4. Helm:" -ForegroundColor White
    Write-Host "   - Go to https://helm.sh/docs/intro/install/" -ForegroundColor Gray
    Write-Host "   - Download the Windows binary" -ForegroundColor Gray
    Write-Host "   - Add to your PATH environment variable" -ForegroundColor Gray
}

Write-Host "`nOnce all tools are installed, verify with:" -ForegroundColor Cyan
Write-Host "docker --version" -ForegroundColor Gray
Write-Host "kubectl version --client" -ForegroundColor Gray
Write-Host "minikube version" -ForegroundColor Gray
Write-Host "helm version" -ForegroundColor Gray

Write-Host "`nAfter installing all prerequisites, you can continue with Phase 4 deployment." -ForegroundColor Green