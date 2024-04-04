# `ocui`

[![Python package](https://github.com/fishinthecalculator/ocui/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/fishinthecalculator/ocui/actions/workflows/python-package.yml) 
![Python versions](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/python.svg)
![License](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/license.svg)

`ocui` is a terminal user interface to facilitate the most common tasks around OCI containers running on a single host.

![ocui screenshot](https://raw.githubusercontent.com/fishinthecalculator/ocui/main/.img/screenshot.png)

## Contributing

All contributions are welcome. If you have commit access please remember to setup the authentication hook with

```bash
cp etc/git/pre-push .git/hooks/pre-push
```

## License

Unless otherwise stated all the files in this repository are to be considered under the GPL 3.0 terms. You are more than welcome to open issues or send patches.

## Helpful initiatives

- This project started during SUSE's [Hack Week 23](https://hackweek.opensuse.org), where I had the time to participate [a project](https://hackweek.opensuse.org/23/projects/forklift-text-based-gui-utility-for-dealing-with-containers) to implement something like `ocui`.
- This project is clearly strongly inspired from [K9s](https://k9scli.io/). Without it I would probably never had found the inspiration for `ocui`.
- The endless nice TUI managers from the community, starting from `top` to `htop`, `glances` and all the others.
