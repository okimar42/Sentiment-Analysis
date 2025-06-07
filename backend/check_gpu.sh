#!/bin/bash
set -e

echo "Starting GPU availability check..."

# Function to check if running in WSL2
is_wsl2() {
    if [ -f /proc/version ]; then
        grep -q "Microsoft" /proc/version
        return $?
    fi
    return 1
}

# Function to get GPU info using nvidia-smi
get_gpu_info() {
    if command -v nvidia-smi &> /dev/null; then
        echo "Using nvidia-smi to get GPU info..."
        nvidia-smi
        return $?
    fi
    return 1
}

# Function to get GPU info using PowerShell (WSL2 fallback)
get_gpu_info_powershell() {
    if command -v powershell.exe &> /dev/null; then
        echo "Using PowerShell to get GPU info..."
        powershell.exe -Command "nvidia-smi"
        return $?
    fi
    return 1
}

# Main logic
if is_wsl2; then
    echo "Running in WSL2 environment"
    if ! get_gpu_info; then
        echo "nvidia-smi failed, trying PowerShell..."
        if ! get_gpu_info_powershell; then
            echo "Failed to get GPU info through both nvidia-smi and PowerShell"
            exit 1
        fi
    fi
else
    echo "Running in native Linux environment"
    if ! get_gpu_info; then
        echo "Failed to get GPU info"
        exit 1
    fi
fi

echo "GPU check completed successfully" 