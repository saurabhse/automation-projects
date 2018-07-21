 * Create a folder
 * Copy build_initial.ps1, build_config.xml, build.ps1
 * Create two folders build and deploy
 * build folder will have scripts folder inside which all scripts reside
 
 
 # Intial Build : #
 * Open Command Prompt and run below command
 
    `powershell.exe -ExecutionPolicy ByPass <script_path>/build_initial.ps1 <env>`
    
 # Build & Deploy: #
 
 * It will pull from git if workspace is outdated and will only deploy reports mentioned in commandline. 
 * For all file suse "All".
 * This will create report folder in deploy folder and inside report folder it will create In put & Output folder and ReportPDFs in output folder
 * Input folder will have all jrxml,jrtx files, output folder will get all jasper files when run script is called and reportpdfs folder will have
    generated pdf.
 * config files will be stored directly into Output folder
 * run, archive etc scripts will be copied into output folder
 
     `powershell.exe -ExecutionPolicy ByPass <script_path>/build.ps1 <env> "Report1,Report2`
