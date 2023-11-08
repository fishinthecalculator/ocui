;;; SPDX-License-Identifier: GPL-3.0-or-later

(define-module (pot)
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
  #:use-module (small-guix packages python-xyz)
  #:use-module (ice-9 exceptions)
  #:use-module (ice-9 rdelim)
  #:use-module (ice-9 popen)
  #:use-module (srfi srfi-1))

(define %source-dir (string-append (current-source-directory)
                                   "/../.."))

(define %source-commit
  (guard (ex
          ((eq? (exception-kind ex) 'wrong-type-arg)
           ;; We are in guix pull.
           "0000000000000000000000000000000000000000"))
    (read-line
     (open-input-pipe "git show HEAD | head -1 | cut -d ' ' -f 2"))))

(define-public pot.git
  (let ((version (with-input-from-file
                     (string-append %source-dir
                                    "/pot/res/VERSION")
                   read-line))
        (revision "0"))
    (package
     (name "pot.git")
     (version (git-version version revision %source-commit))
     (source
      (local-file %source-dir "pot-source"
                  #:recursive? #t
                  #:select? (git-predicate %source-dir)))
     (build-system pyproject-build-system)
     (arguments
      (list #:phases #~(modify-phases %standard-phases
                                      (add-after 'unpack 'patch-version
                                                 (lambda _
                                                   (with-output-to-file "pot/res/VERSION"
                                                     (lambda _
                                                       (display #$version)))))
                                      ;; There are no unit tests currently.
                                      (delete 'check))))
     (native-inputs (list poetry))
     (propagated-inputs (list python-textual-0.41))
     (home-page
      "https://github.com/fishinthecalculator/pot")
     (synopsis
      "")
     (description "")
     (license license:gpl3))))

pot.git
