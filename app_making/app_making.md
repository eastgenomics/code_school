# DNAnexus Applet Creation
[Documentation](https://documentation.dnanexus.com/developer/apps/intro-to-building-apps)
### Apps vs Applets
Applets and apps are both executables that can be run in the platform. The main difference is that applets are data objects, which live in projects, while apps do not live in a project and can be published to allow other users to run them.

#dx-app-wizard

Dnaneuxus provides a quick way of making the backbone required for an app. 

To initiate app creation run this command on your terminal:
```bash

dx-app-wizard
```

It initates an interactive app creation dialog, which aims to gather all necessary information.

It asks for:
* **App Name**: The name of your app must be unique on the DNAnexus platform. your app should be names something like my_app_v1.0.0 (change this according to your github version). Your github repo should be eggd_my_app.
* **Title:** The title, if provided, is what is shown as the name of your app on the website
* **Summary:** Short description of your app.
* **Version [0.0.1]:** Click enter - will add github section afterwards
* **Input Specification:**
  * **1st input name**: The string which will denote your input (i.e. input_bam)
    * **Label** (optional human-readable name)
    * **Input Class**:
      * applet        
      * array:file    
      * array:record   
      * file           
      * int
      * array:applet  
      * array:float   
      * array:string  
      * float          
      * record
      * array:boolean
      * array:int      
      * boolean        
      * hash           
      * string
    *  **This is an optional parameter [y/n]**
 *   It will keep asking for inputs until you press enter without an input name
 * **Output Specification:**
   * Same structure as above.
 * **Timeout Policy:** Number followed by a letter m=minutes, h=hours, d=days
   * Important to think how long your applet should run for and adjust this time accordingly
 * Programming language:
   * Bash
   * Python
 * **Access to the Internet (other than accessing the DNAnexus API).**
 * Will this app need access to the Internet? [y/N]: 
 * Think if this is necessary. 
 * If you are doing for example docker pull you would need access
 * Think if it is necessary to pull live resources or create and save them in 001_References
* **Direct access to the parent project:** This is not needed if your app specifies
outputs,     which will be copied into the project after it's done running
* **Instance Types**:
  * aws instances use memX prefix
  * Be mindful how much memory and storage you need
  * [ DNAnexus Billing Table](https://platform.dnanexus.com/profile/toutoua/settings/billing )
  * It could be useful to test your app with different instances to make them more efficient


### Structure of applet directory

The dx-app-wizard will create the following files:

example_applet/
├── dxapp.json
├── Readme.md
├── Readme.developer.md
├── resources/
│   └── usr/
│       └── bin/
│
└── src/
    └── code.sh

#### dxapp.json
The dxapp.json is a DNAnexus application metadata file. Its presence in a directory tells DNAnexus tools that it contains DNAnexus applet source code. We explain selected fields of this file below.

At the top of your file, add your githubRelease version and remove the version field so it looks like this:

```json
{
  "name": "cgppindel_v1.0.0",
  "title": "cgppindel_v1.0.0",
  "summary": "cgppindel app for DNAnexus",
  "dxapi": "1.0.0",
  "properties": {
    "githubRelease": "v1.0.0"
  },
```

Input and output filed look like this, and this is the file you would change while creating your app to alter according to your needs. No need to run dx-app-wizard everytime.

```json
"inputSpec": [
    {
      "name": "bam_file",
      "label": "bam file",
      "help": "Bam file to be indexed",
      "class": "file",
      "patterns": ["*.bam"],
      "optional": false
    },
    {
      "name": "options",
      "label": "Samtools options for user",
      "help": "",
      "class": "string",
      "optional": true
    }
  ],
  "outputSpec": [
    {
      "name": "index_file",
      "label": "index file",
      "help": "",
      "class": "file",
      "patterns": ["*"]
    }
```

Ensure your app will run in aws-eu-central-1 by changing the regionalOptions as so:

```json
},
  "regionalOptions": {
    "aws:eu-central-1": {
      "systemRequirements": {
        "*": {
          "instanceType": "mem3_ssd1_v2_x4"
        }
```
#### code.sh
This is where you write what you want to do with your app. 

Main structure would be download some inputs --> do something --> upload outputs

Useful to start your shell with :
```bash
#!/bin/bash
set -e -x -o pipefail
```
The -e flag causes bash to exit at any point if there is any error, the -o pipefail flag tells bash to throw an error if it encounters an error within a pipeline, while the -x flag causes bash to output each line as it is executed -- useful for debugging.

**If you have too many inputs:**
```bash 
dx-download-all-inputs --parallel
```

This utility will automatically download all the files supplied as input to the applet into the path /home/dnanexus/in/. Each file input parameter specified under inputSpec in the dxapp.json will have its own folder under the /home/dnanexus/in/ directory.

**If you need them all together here's a useful command**

```bash
#Add all inputs in the same folder to enable indeces to be found.
find ~/in -type f -name "*" -print0 | xargs -0 -I {} mv {} ~/input
```

**Bash app helpers:**
Useful envirnoment variables for your applets.
```bash
$input_prefix   # The name of your file without the suffix
$input_name     # The name of your file
$input_path     # The path of your file on your workstation
$input          # your actual file object

```

**dx-upload-all-outputs**
Equally if you are lazy and need to upload everything rather than declaring them separately.

Create a folder /out and inside a folder for each declared output as it is named in the dxapp.json i.e. /out/index_file

Move your output you want to upload in that folder.

_**Be mindful of what you need to do downstream, you can upload everything with one command but if they are not declared in the json you want be able to easily use the output in a workflow**_

#### /resources
This is where your resources will live. It get unpacked into your appplet'   **/home/dnanexus** as its current working directory.

This is where you would put scripts you want this app to be a wrapper for. Or you could put a docker image, package resources to avoid pip install etc.

If you have executables that you want to have accessible directly you can put them directly in /resources/usr/bin/

**Installing local packages:** 

To please Jethro make a folder at /home/dnanexus/packages to store all your packages to install and keep your home directory clean.


## Readme.md template
You don't need the Readme.developer.md, you can delete if you wanted.

```md
<!-- dx-header -->
# APP_ΝΑΜΕ (DNAnexus Platform App)
  
## What does this app do?

More information on: 

<br></br>

## What are typical use cases for this app?
<br></br>

## What data are required for this app to run?
Required inputs for this app:

<br></br>

## What does this app output?
This app outputs:

This is the source code for an app that runs on the DNAnexus Platform.
For more information about how to run or modify it, see
https://documentation.dnanexus.com/.

```

## Build your app

Inside your applet directory 

```bash
dx build

# Use -f option if you are replacing the previous version

```

Keep going until your app completes successfuly. 

You can choose to the Debug mode which will allow you to ssh in your worker and see what went wrong before terminating.

### App Examples

* In this repo there's a super simple samtools app example with input and output if you fancy playing with it.
* [bam2fqs](https://github.com/eastgenomics/eggd_bam2fqs)
* Apps with docker:
  * [cgppindel](https://github.com/eastgenomics/eggd_cgppindel)
  * [mosdepth](https://github.com/eastgenomics/eggd_mosdepth)
* Complicated one with array input and outputs:
  * [athena](https://github.com/eastgenomics/eggd_athena)