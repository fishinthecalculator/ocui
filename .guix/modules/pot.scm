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
  #:use-module (ice-9 rdelim)
  #:use-module (ice-9 popen)
  #:use-module (srfi srfi-1))

(define %source-dir
  (dirname (dirname (current-source-directory))))

(define %source-version
  (with-input-from-file
      (string-append %source-dir
                     "/pot/res/VERSION")
    read-line))

(define %source-commit
  (if (and (which "git") (which "cut") (which "head"))
      (read-line
       (open-input-pipe "git show HEAD | head -1 | cut -d ' ' -f 2"))
      "0000000000000000000000000000000000000000"))

;; From https://guix.gnu.org/en/blog/2023/from-development-environments-to-continuous-integrationthe-ultimate-guide-to-software-development-with-guix/
(define vcs-file?
  ;; Return true if the given file is under version control.
  (or (git-predicate %source-dir)
      (const #t)))                                ;not in a Git checkout

(define-public pot.git
  (let ((revision "0"))
    (package
     (name "pot.git")
     (version (git-version %source-version revision %source-commit))
     (source
      (local-file %source-dir "pot-checkout"
                  #:recursive? #t
                  #:select? vcs-file?))
     (build-system pyproject-build-system)
     (arguments
      (list
       #:phases #~(modify-phases %standard-phases
                                 (add-after 'unpack 'patch-version
                                            (lambda _
                                              (with-output-to-file "pot/res/VERSION"
                                                (lambda _
                                                  (display #$version)))))
                                 ;; There are no unit tests currently.
                                 (delete 'check))))
     (native-inputs (list poetry))
     (propagated-inputs (list python-appdirs
                              python-textual-0.41
                              python-toml))
     (home-page
      "https://github.com/fishinthecalculator/pot")
     (synopsis
      "")
     (description "")
     (license license:gpl3))))

pot.git
