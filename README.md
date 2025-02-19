# Universal APT Repository
A Universal Public repository for people to distribute .deb packages with.

Based on https://github.com/palfrey/discord-apt

To use just run 
```curl -sSL https://apt.hostmc4free.com/debian/install.sh | bash```

Then just install your package eg. 
```apt install discord```

**Current Packages**
```
discord
discord-ptb
discord-canary
surrealist
flowkeeper
globalprotect-openconnect
```

**To add new package modify sources.json via the following**

**Github repository**

```
{
        "name": "SoftwareName",
        "url": "https://api.github.com/repos/Owner/Repository/releases/latest",
        "package_json": "package-lists/SoftwareName/packages.json"
}
```

eg.
```
{
        "name": "Surrealist",
        "url": "https://api.github.com/repos/surrealdb/surrealist/releases/latest",
        "package_json": "package-lists/surrealist/packages.json"
      }
```

**Any other link**

```
{
        "name": "SoftwareName",
        "url": "link to download page specifying linuz and deb file",
        "package_json": "package-lists/SoftwareName/packages.json"
      }
```
eg.
```
 {
        "name": "discord-stable",
        "url": "https://discord.com/api/download?platform=linux&format=deb",
        "package_json": "package-lists/discord/stable_packages.json"
      }
```


**This is just a repoistory to distribute software I do not claim ownership or provide support for any software distributed if you are the owner of a software distributed via this repository and do not wish for it to be distributed this way simply open an issue and the software will be removed**
