;;; SPDX-License-Identifier: GPL-3.0-or-later

(define-module (pot)
  #:use-module (gnu packages python-build)
  #:use-module (gnu packages python-xyz)
  #:use-module (guix build-system pyproject)
  #:use-module (guix git-download)
  #:use-module ((guix licenses)
                #:prefix license:)
  #:use-module (guix packages)
  ;; Temporary, when python-textual-0.41 is upstreamed
  ;; this dependency can be dropped.
  #:use-module (small-guix packages python-xyz))

(define-public pot
  (package
    (name "pot")
    (version "0.0.2")
    (source (origin
              (method git-fetch)
              (uri (git-reference
                    (url "https://github.com/fishinthecalculator/pot")
                    (commit (string-append "v" version))))
              (file-name (git-file-name name version))
              (sha256
               (base32
                "0aqj0q501md9y09gkc0glwfw6s3l074mh9d96lvkn0qxps1g4wmx"))))
    (build-system pyproject-build-system)
    (arguments
     (list
      ;; There are no unit tests currently.
      #:tests? #f))
    (native-inputs (list poetry
                         python-debugpy
                         python-flake8
                         python-textual-dev))
    (propagated-inputs (list python-appdirs
                             python-textual-0.41
                             python-toml))
    (home-page
     "https://github.com/fishinthecalculator/pot")
    (synopsis
     "Simple text based UI for managing containers")
    (description "@code{pot} is a terminal user interface to
facilitate the most common tasks around OCI containers running on a single host.")
    (license license:gpl3)))
