param(
[string]$env,
[string]$relVrsn
)

$ErrorActionPreference = "stop"
Write-Host "Starting" $env
Try{
  $myDir = Split-Path -Parent $MyInvocation.MyCommand.Path
  $configxml = [xml] (gc $myDir\build_config.xml)
  $gitPath = $configxml.ConfigInfo.Env | ? {$_.name -eq $env} | Select-Xml gitPath
  $git_Path = $gitPath.ToString()
  $git_Path=$git_Path.ToString().replace('#{USERID}',[Environment]::Username)
  $wsLoc = $configxml.ConfigInfo.Env | ? {$_.name -eq $env} | Select-Xml wsLoc
  $releaseVrsn = $configxml.ConfigInfo.Env | ? {$_.name -eq $env} | Select-Xml branchName

  if($relVrsn){
  $releaseVrsn =$releaseVrsn.ToString().SubString(0,8) #this needs to be modified
  $releaseVrsn =$releaseVrsn+$relVrsn
  }

  set path= $git_Path
  cd $wsLoc
  git clone -b $releaseVrsn "https://<git_repo_url>/.git" $wsLoc #this needs to be modified
}
Catch [Exception]{
    Write-Host $_.Exception.Message
    exit 777
}
