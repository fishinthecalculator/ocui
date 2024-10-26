;;; SPDX-License-Identifier: GPL-3.0-or-later

(define-module (ocui)
  #:use-module (gnu packages python-build)
  #:use-module (gnu packages python-xyz)
  #:use-module (guix build-system pyproject)
  #:use-module (guix gexp)
  #:use-module (guix git-download)
  #:use-module ((guix licenses)
                #:prefix license:)
  #:use-module (guix packages)
  #:use-module (guix utils)
  ;; Temporary, when python-textual-0.41 is upstreamed
  ;; this dependency can be dropped.
  #:use-module (small-guix packages python-xyz))

(define %source-dir
  (dirname (dirname (current-source-directory))))

;; From https://guix.gnu.org/en/blog/2023/from-development-environments-to-continuous-integrationthe-ultimate-guide-to-software-development-with-guix/
(define vcs-file?
  ;; Return true if the given file is under version control.
  (or (git-predicate %source-dir)
      (const #t)))                                ;not in a Git checkout

(define-public ocui.git
  (package
   (name "ocui.git")
   (version "0.1.1")
   (source
    (local-file "../.." "ocui-checkout"
                #:recursive? #t
                #:select? vcs-file?))
   (build-system pyproject-build-system)
   (arguments
    (list
     ;; There are no unit tests currently.
     #:tests? #f))
   (native-inputs (list python-debugpy
                        python-flake8
                        python-flit
                        python-textual-dev))
   (propagated-inputs (list python-appdirs
                            python-textual-0.41
                            python-toml))
   (home-page
    "https://github.com/fishinthecalculator/ocui")
   (synopsis
    "Simple text based UI for managing containers")
   (description "@code{ocui} is a terminal user interface to
facilitate the most common tasks around OCI containers running on a single host.")
   (license license:gpl3)))

ocui.git
