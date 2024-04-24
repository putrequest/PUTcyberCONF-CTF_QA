# Source file path
$sourceFile = "./PUTr_5050_mm.png"

# Output directory for generated icons
$outputDirectory = "./icons"

# Sizes of icons to generate
$iconSizes = @(16, 32, 48, 64, 96, 128, 256)

# Create a string list of icon names
$iconNames = $iconSizes.ForEach({ "./icons/$_.png" }) -join " "

# Create the output directory if it doesn't exist
if (-not (Test-Path -Path $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}

$inkscapePath = "inkscape"

# Generate icons of specified sizes
foreach ($size in $iconSizes) {
    Write-Host "Generating icon of size $size x $size pixels..."
    $arguments = "-w $size -h $size -o $outputDirectory/$size.png $sourceFile"
    Start-Process -FilePath $inkscapePath -ArgumentList $arguments -NoNewWindow -Wait
}

Write-Host "Icons generated successfully!"

# Generate ico file from the generated icons

$convertPath = "magick"

Start-Process -FilePath $convertPath -ArgumentList "$iconNames icon.ico" -NoNewWindow -Wait

# Check icon contents
Start-Process -FilePath "identify" -ArgumentList "icon.ico" -NoNewWindow -Wait

rm -r icons