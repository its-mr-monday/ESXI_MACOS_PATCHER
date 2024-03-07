$p = &{python -V} 2>&1
# check if an ErrorRecord was returned
$version = if($p -is [System.Management.Automation.ErrorRecord])
{
    # grab the version string from the error message
    $p.Exception.Message
}
else 
{
    # otherwise return as is
    $p
}

if ($version -like "*Python 3*") {
} else {
    Write-Host "[!] Python 3 is not installed\nPlease install it and then run macos_vmx.ps1" -ForegroundColor Red
    Write-Host "[!] You may install python3 with the following command:"
    Write-Host "[!] winget install -e --id Python.Python.3.12" -ForegroundColor Yellow
    exit 1    
}

$path = $PSScriptRoot
$currentDir = Get-Location
Set-Location $path
if (Test-Path venv) {
} else {
	&{pip install virtualenv}
	&{python -m venv venv}
	&{.\venv\Scripts\activate}
	&{pip install -r requirements.txt}
	&{deactivate}
}

&{.\venv\Scripts\activate}
&{python macos_vmx.py}
$EXIT_CODE = $LASTEXITCODE
&{deactivate}
Set-Location $currentDir
exit $EXIT_CODE

