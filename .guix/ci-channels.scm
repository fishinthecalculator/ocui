(append
 (list (channel
        (name 'small-guix)
        (url "https://gitlab.com/orang3/small-guix")
        ;; Enable signature verification:
        (introduction
         (make-channel-introduction
          "940e21366a8c986d1e10a851c7ce62223b6891ef"
          (openpgp-fingerprint
           "D088 4467 87F7 CBB2 AE08  BE6D D075 F59A 4805 49C3"))))
       (channel
        (name 'pot)
        (url "https://github.com/fishinthecalculator/pot")
        (branch "main")
        ;; Enable signature verification:
        (introduction
         (make-channel-introduction
          "10ed759852825149eb4b08c9b75777111a92048e"
          (openpgp-fingerprint
           "97A2 CB8F B066 F894 9928  CF80 DE9B E0AC E824 6F08")))))
 %default-guix-channels)
