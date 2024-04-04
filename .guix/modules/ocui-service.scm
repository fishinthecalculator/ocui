;;; SPDX-License-Identifier: GPL-3.0-or-later

(define-module (ocui-service)
  #:use-module (guix gexp)
  #:use-module (guix packages)
  #:use-module (gnu home services)
  #:use-module (gnu services configuration)
  #:use-module (ocui)
  #:use-module (ice-9 string-fun)
  #:export (ocui-oci-configuration
            ocui-oci-configuration?
            ocui-oci-configuration-fields
            ocui-oci-configuration-runtime
            ocui-oci-configuration-extra-content

            ocui-ui-configuration
            ocui-ui-configuration?
            ocui-ui-configuration-fields
            ocui-ui-configuration-refresh-timeout
            ocui-ui-configuration-startup-mode
            ocui-ui-configuration-extra-content

            ocui-configuration
            ocui-configuration?
            ocui-configuration-fields
            ocui-configuration-ocui
            ocui-configuration-oci
            ocui-configuration-ui
            ocui-configuration-extra-content

            home-ocui-service-type))

;; Turn field names, which are Scheme symbols into strings
(define (uglify-field-name field-name)
  (string-replace-substring (symbol->string field-name) "-" "_"))

(define (serialize-toml-field field-name value)
  #~(string-append #$(uglify-field-name field-name) " = " #$value "\n"))

(define (serialize-string field-name value)
  (if (eq? field-name 'extra-content)
      (string-append value "\n")
      (serialize-toml-field field-name (string-append "\"" value "\""))))

(define (serialize-number field-name value)
  (serialize-toml-field field-name (number->string value)))

(define (serialize-boolean field-name value)
  (serialize-toml-field field-name (if value "true" "false")))

(define (serialize-record->toml name value fields)
  #~(string-append
     "[" #$name "]\n"
     #$(serialize-configuration
        value fields)))

(define ocui-serialize-string serialize-string)

(define (ocui-serialize-ocui-oci-configuration field-name value)
  (serialize-record->toml "oci" value ocui-oci-configuration-fields))

(define (ocui-serialize-ocui-ui-configuration field-name value)
  (serialize-record->toml "ui" value ocui-ui-configuration-fields))

(define (ocui-serialize-ocui-configuration configuration)
  (mixed-text-file
   "ocui.toml"
   (serialize-configuration
    configuration ocui-configuration-fields)))

(define-configuration ocui-oci-configuration
  (runtime
   (string "docker")
   "The OCI runtime used by @{ocui} as a source of information.")
  (extra-content
   (string "")
   "Everything you want to manually add to @code{[oci]}."))

(define-configuration ocui-ui-configuration
  (refresh-timeout
   (number 10)
   "The number of seconds after which @code{ocui}'s will update its tables.")
  (startup-mode
   (string "containers")
   "@{ocui}'s startup mode.")
  (extra-content
   (string "")
   "Everything you want to manually add to @code{[ui]}."))

(define-configuration ocui-configuration
  (ocui
   (package ocui.git)
   "The @code{ocui} package to use."
   (serializer empty-serializer))
  (oci
   (ocui-oci-configuration (ocui-oci-configuration))
   "@{ocui}'s OCI runtime configuration.")
  (ui
   (ocui-ui-configuration (ocui-ui-configuration))
   "@{ocui}'s UI configuration.")
  (extra-content
   (string "")
   "Everything you want to manually add to @code{ocui.toml}.")
  (prefix ocui-))

(define (config->file-like config)
  (list
   (string-append "ocui/" (package-version (ocui-configuration-ocui config)) "/ocui.toml")
   (ocui-serialize-ocui-configuration config)))

(define home-ocui-service-type
  (service-type (name 'ocui)
                (extensions (list (service-extension
                                   home-xdg-configuration-files-service-type
                                   (compose list config->file-like))
                                  (service-extension home-profile-service-type
                                   (compose list ocui-configuration-ocui))))
                (default-value (ocui-configuration))
                (description
                 "Installs @code{ocui} in Guix Home's profile and creates a suitable configuration.")))
