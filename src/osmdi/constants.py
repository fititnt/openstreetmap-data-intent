# @TODO add other common formats on <syntaxhighlight lang="">
#       see https://pygments.org/docs/formatters/
#       see https://pygments.org/docs/lexers/
#           - Stopped on 'Lexers for .net languages'; needs check others
# import os

import os


_REFVER = "0.2.0"

WIKI_AS_BASE_BOTNAME = os.getenv(
    "WIKI_AS_BASE_BOTNAME", "wiki_as_base-cli-bot/" + _REFVER
)
_WIKI_AS_BASE_BOT_CONTACT_DEFAULT = (
    "https://github.com/fititnt/openstreetmap-data-intent; generic@example.org"
)
WIKI_AS_BASE_BOT_CONTACT = os.getenv(
    "WIKI_AS_BASE_BOT_CONTACT", _WIKI_AS_BASE_BOT_CONTACT_DEFAULT
)
WIKI_AS_BASE_LIB = f"osmdi/{_REFVER}"

_USER_AGENT_MERGED = (
    f"{WIKI_AS_BASE_BOTNAME} ({WIKI_AS_BASE_BOT_CONTACT}) {WIKI_AS_BASE_LIB}"
)

USER_AGENT = os.getenv("USER_AGENT", _USER_AGENT_MERGED)

# CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
CACHE_TTL = int(os.getenv("CACHE_TTL", "82800"))  # 23 hours
CACHE_DBNAME = os.getenv("CACHE_DBNAME", "osmdicache.sqlite")
