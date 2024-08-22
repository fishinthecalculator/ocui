# `ocui`

[![Python package](https://github.com/fishinthecalculator/ocui/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/fishinthecalculator/ocui/actions/workflows/python-package.yml) 
![Python versions](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/python.svg)
[![PyPI version](https://raw.githubusercontent.com/fishinthecalculator/ocui/master/.img/pypi.svg)](https://pypi.org/project/ocui/)
![License](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/license.svg)

`ocui` is a terminal user interface to facilitate the most common tasks around OCI containers running on a single host. You can create, start and kill containers with few keystrokes, as well as look at logs in real time, or inspect images. `ocui` continually watches the system for changes and offers adequate commands to interact with the system resources.

## Screenshots

### Containers running in the system

![ocui containers](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/screenshot.png)

### Real time logs

![ocui logs](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/logs.png)

### Container creation

![ocui create container](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/container_creation.png)

### Container inspection

![ocui inspect container](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/container_inspection.png)

## Contributing

All contributions are welcome. If you have commit access please remember to setup the authentication hook with

```bash
guix git authenticate --cache-key=channels/ocui --stats "10ed759852825149eb4b08c9b75777111a92048e" "97A2 CB8F B066 F894 9928  CF80 DE9B E0AC E824 6F08"
```

## License

Unless otherwise stated all the files in this repository are to be considered under the GPL 3.0 terms. You are more than welcome to open issues or send patches.

## Helpful initiatives

- This project started during SUSE's [Hack Week 23](https://hackweek.opensuse.org), where I had the time to participate [a project](https://hackweek.opensuse.org/23/projects/forklift-text-based-gui-utility-for-dealing-with-containers) to implement something like `ocui`.
- This project is clearly strongly inspired from [K9s](https://k9scli.io/). Without it I would probably never had found the inspiration for `ocui`.
- The endless nice TUI managers from the community, starting from `top` to `htop`, `glances` and all the others.
