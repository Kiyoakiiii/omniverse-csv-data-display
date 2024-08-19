# Extension Project Template


- `app` - It is a folder link to the location of your *Omniverse Kit* based app.
- `exts` - It is a folder where you can add new extensions. It was automatically added to extension search path. (Extension Manager -> Gear Icon -> Extension Search Path).

Open this folder using Visual Studio Code. It will suggest you to install few extensions that will make python experience better.

Look for "csv_data_display" extension in extension manager and enable it. Try applying changes to any python files, it will hot-reload and you can observe results immediately.

Alternatively, you can launch your app from console with this folder added to search path and your extension enabled, e.g.:

```
> app\omni.code.bat --ext-folder exts --enable company.hello.world
```

# App Link Setup

If `app` folder link doesn't exist or broken it can be created again. For better developer experience it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. Convenience script to use is included.

Run:

```
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```
> link_app.bat --app create
```

You can also just pass a path to create link to:

```
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```


# Get data from the server

Run the script.py file. Note that the prerequisite is to install the driver for the corresponding browser. The example here uses the Chorme browser, so you need to download the Google Chorme driver. [Download it from this link] (https://googlechromelabs.github.io/chrome-for-testing/).

