##
# pot
#
# @file
# @version 0.1

# Introduction of the 'pot' channel.
channel_intro_commit = 10ed759852825149eb4b08c9b75777111a92048e
channel_intro_signer = 97A2 CB8F B066 F894 9928  CF80 DE9B E0AC E824 6F08

authenticate:
	echo "Authenticating Git checkout..." ;	\
	guix git authenticate					\
	    --cache-key=channels/pot --stats			\
	    "$(channel_intro_commit)" "$(channel_intro_signer)"

# end
