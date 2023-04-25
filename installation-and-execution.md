# Installation & Execution

## Cloning the repository

* The repository is available in this [github repo](https://github.com/wajo10/PCT).&#x20;
* Using your terminal you can simply use the command:&#x20;
  * `git clone` [`https://github.com/wajo10/PCT.git`](https://github.com/wajo10/PCT.git)
* Or you can download the repo as a zip file from [the repo URL](https://github.com/wajo10/PCT) and decompress it.

## Installing FUXA

Open a terminal and run the following command:

```
npm install -g --unsafe-perm @frangoteam/fuxa
```

## Installing Prerequisites

* Open a terminal on the "Server API" folder
* Run the command:
  * `npm install`
* Go to the "Controller" folder and execute:
  * `pip install -r requirements.txt`

## Running the system

IMPORTANT: all sensors must be connected and turned on for this to work.

* If you are using windows just run the file `WindowsExec.bat`&#x20;
* If you are using Linux/Raspbian execute:&#x20;
  * `sudo chmod +x RaspbianExec.sh`
  * `./RaspbianExec.sh`

