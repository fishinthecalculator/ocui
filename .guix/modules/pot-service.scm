;;; SPDX-License-Identifier: GPL-3.0-or-later

(define-module (pot-service)
  #:use-module (guix gexp)
  #:use-module (guix packages)
  #:use-module (gnu home services)
  #:use-module (gnu services configuration)
  #:use-module (pot)
  #:use-module (ice-9 string-fun)
  #:export (pot-oci-configuration
            pot-oci-configuration?
            pot-oci-configuration-fields
            pot-oci-configuration-runtime
            pot-oci-configuration-extra-content

            pot-ui-configuration
            pot-ui-configuration?
            pot-ui-configuration-fields
            pot-ui-configuration-refresh-timeout
            pot-ui-configuration-startup-mode
            pot-ui-configuration-extra-content

            pot-configuration
            pot-configuration?
            pot-configuration-fields
            pot-configuration-pot
            pot-configuration-oci
            pot-configuration-ui
            pot-configuration-extra-content

            home-pot-service-type))

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

(define pot-serialize-string serialize-string)

(define (pot-serialize-pot-oci-configuration field-name value)
  (serialize-record->toml "oci" value pot-oci-configuration-fields))

(define (pot-serialize-pot-ui-configuration field-name value)
  (serialize-record->toml "ui" value pot-ui-configuration-fields))

(define (pot-serialize-pot-configuration configuration)
  (mixed-text-file
   "pot.toml"
   (serialize-configuration
    configuration pot-configuration-fields)))

(define-configuration pot-oci-configuration
  (runtime
   (string "docker")
   "The OCI runtime used by @{pot} as a source of information.")
  (extra-content
   (string "")
   "Everything you want to manually add to @code{[oci]}."))

(define-configuration pot-ui-configuration
  (refresh-timeout
   (number 10)
   "The number of seconds after which @code{pot}'s will update its tables.")
  (startup-mode
   (string "containers")
   "@{pot}'s startup mode.")
  (extra-content
   (string "")
   "Everything you want to manually add to @code{[ui]}."))

(define-configuration pot-configuration
  (pot
   (package pot.git)
   "The @code{pot} package to use."
   (serializer empty-serializer))
  (oci
   (pot-oci-configuration (pot-oci-configuration))
   "@{pot}'s OCI runtime configuration.")
  (ui
   (pot-ui-configuration (pot-ui-configuration))
   "@{pot}'s UI configuration.")
  (extra-content
   (string "")
   "Everything you want to manually add to @code{pot.toml}.")
  (prefix pot-))

(define (config->file-like config)
  (list
   (string-append "pot/" (package-version (pot-configuration-pot config)) "/pot.toml")
   (serialize-configuration config pot-configuration-fields)))

(define home-pot-service-type
  (service-type (name 'pot)
                (extensions (list (service-extension
                                   home-xdg-configuration-files-service-type
                                   (compose list config->file-like))
                                  (service-extension home-profile-service-type
                                   (compose list pot-configuration-pot))))
                (default-value (pot-configuration))
                (description
                 "Installs code{pot} in Guix Home's profile and creates a suitable configuration.")))
