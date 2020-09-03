# replay-script

## Using Docker
### build the docker container
`./build-docker.sh`

```
Sending build context to Docker daemon  9.728kB
 Step 1/6 : FROM gcr.io/google.com/cloudsdktool/cloud-sdk
  ---> 0cce5e19e548
 Step 2/6 : COPY replay-data.py /
  ---> Using cache
  ---> 1dc39ddf3740
 Step 3/6 : COPY entrypoint.sh /
  ---> Using cache
  ---> 3393fc2cd1d0
 Step 4/6 : RUN mkdir /logfiles &&     chmod +x /entrypoint.sh
  ---> Using cache
  ---> 7dc557219ba1
 Step 5/6 : VOLUME /logfiles
  ---> Using cache
  ---> 0f8585fd2381
 Step 6/6 : WORKDIR /logfiles
  ---> Using cache
  ---> d654b72d7eac
 Successfully built d654b72d7eac
 Successfully tagged replay-data:latest
```

### Set up your google cloud credentials
`./set-up-auth.sh`

```
Welcome! This command will take you through the configuration of gcloud.

Your current configuration has been set to: [default]

You can skip diagnostics next time by using the following flag:
  gcloud init --skip-diagnostics

Network diagnostic detects and fixes local network connection issues.
Checking network connection...done.
Reachability Check passed.
Network diagnostic passed (1/1 checks passed).

You must log in to continue. Would you like to log in (Y/n)?  Y

Go to the following link in your browser:

    https://accounts.google.com/o/oauth2/auth?code_challenge=D4S2DCe6bIm9ftQiIp_-y4TU9n0XXxTQti21rpn7KtI&prompt=select_account&code_challenge_method=S256&access_type=offline&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&client_id=32555940559.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fappengine.admin+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcompute+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Faccounts.reauth


Enter verification code:
```

```
You are logged in as: [paul.kane@roxorgaming.com].

Pick cloud project to use:
 [1] gamesys-eu-dev01-rgp
 [2] gamesys-eu-live-rgp
 [3] gamesys-eu-live-rgp-b2b
 [4] gamesys-eu-pp-rgp-b2b
 [5] gamesys-eu-pp02-rgp
 [6] gamesys-eu-pp03-rgp
 [7] gameys-eu-games-devint-rgp
 [8] roxor-global-pp-1
 [9] Create a new project
Please enter numeric choice or text value (must exactly match list
item):  2

Your current project has been set to: [gamesys-eu-live-rgp].

Do you want to configure a default Compute Region and Zone? (Y/n)?  n

Created a default .boto configuration file at [/root/.boto]. See this file and
[https://cloud.google.com/storage/docs/gsutil/commands/config] for more
information about configuring Google Cloud Storage.
Your Google Cloud SDK is configured and ready to use!

* Commands that require authentication will use paul.kane@roxorgaming.com by default
* Commands will reference project `gamesys-eu-live-rgp` by default
Run `gcloud help config` to learn how to change individual settings

This gcloud configuration is called [default]. You can create additional configurations if you work with multiple accounts and/or projects.
Run `gcloud topic configurations` to learn more.

Some things to try next:

* Run `gcloud --help` to see the Cloud Platform services you can interact with. And run `gcloud help COMMAND` to get help on any gcloud command.
* Run `gcloud topic --help` to learn about advanced features of the SDK like arg files and output formatting
```

#### Get the replay data
``./get-replay-data.sh -p 21656563 -g js-mfg-daily-free-parking -d 2019-11-30 -t 00:10:47``

#### Logfiles
All logs files are written the ***logfiles*** folder

## Install python3
brew install python
## Install gsutil
[gsutil](https://cloud.google.com/storage/docs/gsutil_install)
## Usage
`python3 replay-data.py -p PLAYER_ID -g GAME_ID -d DATE -t TIME -i GAME_PLAY_ID`
## Example
`python3 replay-data.py -p 21308622 -g double-bubble-triple-jackpot -d 2019-11-03 -t 20:56:50 -i b98df721-f9ef-43dc-a6aa-6c3411ce47c8191a`
## Notes
Time format: hh:mm:ss  
Date format: year-mm-dd  
if date is before 2019-10-27, then -s or --daylight-saving should be set to 1  
`python3 replay-data.py -p 21308622 -g double-bubble-triple-jackpot -d 2019-10-26 -t 20:56:50 -i b98df721-f9ef-43dc-a6aa-6c3411ce47c8191a -s 1`  




