param(
[parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][ValidateSet("Prod","UAT","Local")][string]$env,
[parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][array]$reportNames,
[string]$relVrsn
)

Function copyScripts($buildPath,$deployPath){
    if(Test-Path $buildPath\scripts){
        Copy-Item $buildPath\scripts\* $deployPath -Force -Recurse
     }   
}

Function copyStyleSheets($buildPath,$deployPath,$repName){
    if(Test-Path $buildPath\style){
        Copy-Item $buildPath\style\* $deployPath\$repName\Input -Force -Recurse
     }   
}

Function copyConfigFiles($buildPath,$deployPath,$repName){
    if(Test-Path $buildPath\$repName\config\){
        Copy-Item $buildPath\$repName\config\* $deployPath\$repName -Force -Recurse
     }   
}

Function copyJasperFiles($buildPath,$deployPath,$repName){
    if(!(Test-Path $deployPath\$repName)){
        New-Item $deployPath\$repName -ItemType Directory -Force
        New-Item $deployPath\$repName\Input -ItemType Directory -Force
        New-Item $deployPath\$repName\Output -ItemType Directory -Force
        New-Item $deployPath\$repName\Output\ReportPDFs -ItemType Directory -Force
     } 
     Copy-Item $buildPath\$repName\* $deployPath\$repName\Input -Exclude '*.xml' -Force 
}

$ErrorActionPreference = "stop"
Write-Host "Starting" $env
Try{
  $myDir = Split-Path -Parent $MyInvocation.MyCommand.Path
  $configxml = [xml] (gc $myDir\build_config.xml)
  $gitPath = $configxml.ConfigInfo.Env | ? {$_.name -eq $env} | Select-Xml gitPath
  $git_Path = $gitPath.ToString()
  $git_Path=$git_Path.ToString().replace('#{USERID}',[Environment]::Username)
  $buildPath = $configxml.ConfigInfo.Env | ? {$_.name -eq $env} | Select-Xml buildPath
  $deployPath = $configxml.ConfigInfo.Env | ? {$_.name -eq $env} | Select-Xml deployPath
  $releaseVrsn = $configxml.ConfigInfo.Env | ? {$_.name -eq $env} | Select-Xml branchName

  if($relVrsn){
  $releaseVrsn =$releaseVrsn.ToString().SubString(0,8) #this needs to be modified
  $releaseVrsn =$releaseVrsn+$relVrsn
  }
  
  $configxml.ConfigInfo.Env.excludeFOlders.folderName |
        foreach {
            $exclFolders += ',' + $_
            }
   $exclFolders = $exclFolders -split ","
  set path= $git_Path
  cd $buildPath.ToString()
  git branch
  git pull origin $releaseVrsn
  
  $inclFiles = $reportNames -split ","
  
  if( $inclFiles -eq 'All'){
      $copyCriteria = Get-ChildItem $buildPath | where-object {$exclFolders -notcontains $_.Name -and $_.PSIsContainer}
      Remove-Item $deployPath\* -recurse
  }else{
    $copyCriteria = Get-ChildItem $buildPath | where-object {$exclFolders -notcontains $_.Name - and $inclFiles -contains $_.Name -and $_.PSIsContainer}
  }
  $copyCriteria |
      foreach {
            copyJasperFiles $buildPath $deployPath $_
            copyStyleSheets $buildPath $deployPath $_
            copyConfigFiles $buildPath $deployPath $_
      }
  copyScripts $buildPath $deployPath
}
Catch [Exception]{
    Write-Host $_.Exception.Message
    exit 777
}
