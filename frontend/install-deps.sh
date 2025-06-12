#!/bin/bash

# Frontend dependency installation script
# This script helps troubleshoot and fix common dependency installation issues

set -e

echo "🚀 Frontend Dependency Installation Script"
echo "=========================================="

# Function to print colored output
print_info() {
    echo -e "\033[34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[32m[SUCCESS]\033[0m $1"
}

print_warning() {
    echo -e "\033[33m[WARNING]\033[0m $1"
}

print_error() {
    echo -e "\033[31m[ERROR]\033[0m $1"
}

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    print_error "package.json not found. Please run this script from the frontend directory."
    exit 1
fi

print_info "Current directory: $(pwd)"
print_info "Node.js version: $(node --version 2>/dev/null || echo 'Node.js not found')"
print_info "npm version: $(npm --version 2>/dev/null || echo 'npm not found')"

# Check for existing node_modules and package-lock.json
if [ -d "node_modules" ]; then
    print_warning "node_modules directory exists. Removing for clean install..."
    rm -rf node_modules
fi

if [ -f "package-lock.json" ]; then
    print_info "package-lock.json found. This will be used for reproducible installs."
else
    print_warning "package-lock.json not found. This may cause version inconsistencies."
fi

# Clear npm cache
print_info "Clearing npm cache..."
npm cache clean --force

# Install dependencies
print_info "Installing dependencies..."
if npm ci --no-audit --no-fund; then
    print_success "Dependencies installed successfully!"
else
    print_warning "npm ci failed. Trying npm install as fallback..."
    if npm install --no-audit --no-fund; then
        print_success "Dependencies installed with npm install!"
    else
        print_error "Both npm ci and npm install failed. Please check the error messages above."
        exit 1
    fi
fi

# Run audit and show vulnerabilities
print_info "Checking for vulnerabilities..."
npm audit --audit-level=moderate || print_warning "Some vulnerabilities found. Run 'npm audit fix' to address them."

# Verify installation
print_info "Verifying installation..."
if [ -d "node_modules" ] && [ -n "$(ls -A node_modules)" ]; then
    print_success "node_modules directory is populated."
else
    print_error "node_modules directory is empty or missing."
    exit 1
fi

# Check if main dependencies are available
print_info "Checking key dependencies..."
for dep in "react" "vite" "@types/react"; do
    if [ -d "node_modules/$dep" ]; then
        print_success "$dep is installed"
    else
        print_error "$dep is missing"
    fi
done

print_success "✅ Frontend dependencies installation completed!"
print_info "You can now run:"
print_info "  - npm run dev (for development)"
print_info "  - npm run build (for production build)"
print_info "  - npm run test (for testing)"