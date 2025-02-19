# Universal APT Repository  

A **Universal Public Repository** for distributing `.deb` packages. This repository allows users to easily install software without needing to manually download `.deb` files.  

This project is based on [palfrey/discord-apt](https://github.com/palfrey/discord-apt).  

---

## **Usage**  

To add this repository to your system, run:  
```bash
curl -sSL https://apt.hostmc4free.com/debian/install.sh | bash
```
Then install your desired package:  
```bash
apt install <package-name>
```

---

## **Available Packages**  
The following software is currently available:  
- `discord`  
- `discord-ptb`  
- `discord-canary`  
- `surrealist`  
- `flowkeeper`  
- `globalprotect-openconnect`
- `reactive-graph`

---

## **Adding New Packages**  

To add a new package, modify `sources.json` using the following format:  

### **For GitHub-hosted software:**  
```json
{
    "name": "SoftwareName",
    "url": "https://api.github.com/repos/Owner/Repository/releases/latest",
    "package_json": "package-lists/SoftwareName/packages.json"
}
```
#### Example:
```json
{
    "name": "Surrealist",
    "url": "https://api.github.com/repos/surrealdb/surrealist/releases/latest",
    "package_json": "package-lists/surrealist/packages.json"
}
```

### **For Other Download Links:**  
```json
{
    "name": "SoftwareName",
    "url": "Direct link to the .deb file or download page",
    "package_json": "package-lists/SoftwareName/packages.json"
}
```
#### Example:
```json
{
    "name": "discord-stable",
    "url": "https://discord.com/api/download?platform=linux&format=deb",
    "package_json": "package-lists/discord/stable_packages.json"
}
```

---

## **Legal Disclaimer**  

- This repository serves **only as a distribution point** and does **not modify** any software.  
- **No ownership is claimed** over any software distributed here.  
- **No support** is provided for any software included in this repository.  
- If you are the **owner of any software** distributed here and **do not wish for it to be included**, simply open an issue, and the package will be promptly removed.  

---

## **License**  

The repository structure, scripts, and metadata are licensed under the **MIT License**. However, all software packages remain under their **respective original licenses**.  

For more details, see the [`LICENSE`](./LICENSE) file.  
