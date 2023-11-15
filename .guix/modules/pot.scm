;;; SPDX-License-Identifier: GPL-3.0-or-later

(define-module (pot)
  #:use-module (gnu packages python-build)
  #:use-module (gnu packages python-xyz)
  #:use-module (guix build utils)
  #:use-module (guix build-system pyproject)
  #:use-module (guix gexp)
  #:use-module (guix git-download)
  #:use-module ((guix licenses)
                #:prefix license:)
  #:use-module (guix packages)
  #:use-module (guix utils)
  ;; Temporary, when python-textual-0.41 is upstreamed
  ;; this dependency can be dropped.
  #:use-module (small-guix packages python-xyz)
  #:use-module (ice-9 popen)
  #:use-module (ice-9 rdelim))

(define %source-dir
  (dirname (dirname (current-source-directory))))

;; From https://guix.gnu.org/en/blog/2023/from-development-environments-to-continuous-integrationthe-ultimate-guide-to-software-development-with-guix/
(define vcs-file?
  ;; Return true if the given file is under version control.
  (or (git-predicate %source-dir)
      (const #t)))                                ;not in a Git checkout

(define-public pot.git
  (package
   (name "pot.git")
   (version "0.0.3")
   (source
    (local-file %source-dir "pot-checkout"
                #:recursive? #t
                #:select? vcs-file?))
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


;;; For guix build -f
(let ((revision "0")
      (version
       (with-input-from-file
           (string-append %source-dir
                          "/pot/res/VERSION")
         read-line))
      (commit
       (if (and (which "git") (which "cut") (which "head"))
           (read-line
            (open-input-pipe "git show HEAD | head -1 | cut -d ' ' -f 2"))
           "0000000000000000000000000000000000000000")))
  (package
   (inherit pot.git)
   (version (git-version version revision commit))
   (arguments
    (list
     ;; There are no unit tests currently.
     #:tests? #f
     #:phases
     #~(modify-phases %standard-phases
                      (add-after 'unpack 'patch-version
                                 (lambda _
                                   (with-output-to-file "pot/res/VERSION"
                                     (lambda _
                                       (display #$version))))))))))
