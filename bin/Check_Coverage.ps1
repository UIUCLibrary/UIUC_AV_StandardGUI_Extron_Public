param (
    [string]$module='',
    [switch]$append=$false,
    [switch]$blank=$false,
    [string]$path=".",
    [string]$testPath="tests"
)

Set-Location $path

$testLog = ".\TEST_LOG.log"
if (Test-Path $testLog) {
    Remove-Item $testLog
}

$coverage = ".\.coverage"
if ((Test-Path $coverage) -and $blank) {
    Remove-Item $coverage
}

Write-Output @"
======================================================================
Discovering and running unit tests
----------------------------------------------------------------------
"@

$env:PYTHONPATH = '.\\src;.\\tests;.\\tests\\reqs'

if ($module -eq '') {
    if ($append) {
        coverage run --source=uofi_gui,utilityFunctions --append -m unittest discover -v -b -s .\$testPath\ -p test_*.py
} else {
        coverage run --source=uofi_gui,utilityFunctions -m unittest discover -v -b -s .\$testPath\ -p test_*.py
    }
} else {
    $testModule = $module.Replace('.', '_')
    if ($append) {
        coverage run --source=$module --append --context=$module -m unittest -b -v test_$testModule
    } else {
        coverage run --source=$module --context=$module -m unittest -b -v test_$testModule
    }
}
Write-Output @"
======================================================================
Generating coverage report
----------------------------------------------------------------------
"@
coverage html

Write-Output @"
======================================================================
Opening coverage report
----------------------------------------------------------------------
"@
Invoke-Item .\htmlcov\index.html