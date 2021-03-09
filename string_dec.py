#!/usr/bin/env python3
#MOST LIKELY TO CHANGE DEPENDING ON IMPLEMEMNTATION------------------------------------------
BOTNAME = "Critter 2.0"
dev_id = "191396253299507210" #ID for developer (Gets errors pmed to them)

#Discord Server Info
DISCORD_TOKEN="" #This will change if the code gets posted publicly
DISCORD_GUILD="Chai Château: Redux" #Primary Server Name
DISCORD_MOD_CHANNEL=642810772107427861 #Gets suggestions
DISCORD_WELCOME_CHANNEL=616646216628830222 #Posts welcome message
DISCORD_INVESTIGATION_CHANNEL=644179727677915146 #Announces Investigations
DISCORD_BIRTHDAY_CHANNEL=643164406405922859 #Announces B-days
DISCORD_SEASON_CHANNEL=644179727677915146 #Announces Season Changes
DISCORD_GENERAL_INTRO_CHANNEL=639115120798203909 #Links in welcome message
DISCORD_CHANNEL_DIR_CHANNEL=686009546270834740 #Links in join and leave
DISCORD_QUESTIONS_CHANNEL=636581490825756684 #Links in gift delivery error

DISCORD_BIRTHDAYS_GROUP=807839150501003264 #@'s Birthdays Group in Birthdays
DISCORD_INVESTIGATORS_GROUP=809288411721629757 #@'s Investigators Group in Investigators

channel_directory_link = "<#"+str(DISCORD_CHANNEL_DIR_CHANNEL)+">"
channel_questions_link = "<#"+str(DISCORD_QUESTIONS_CHANNEL)+">"
target_birthdays_grp = "<@&"+str(DISCORD_BIRTHDAYS_GROUP)+">"
target_investigators_grp = "<@&"+str(DISCORD_INVESTIGATORS_GROUP)+">"

help_diamond_emoji = "<:helpdiamond:816002942289051649>"
help_new_emoji = "<:helpnew:816002942658150470>"
gold_medal_emoji = "<:first:816095462473728081>"
silver_medal_emoji = "<:second:816095462457081916>"
bronze_medal_emoji = "<:third:816095462498369586>"
hm_star_emoji = "<:hmstar:816095715323150358>"
horror_bonk_emoji = '<:horrorbonk:817531789135970374>'

#Sheets API Info
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] #I think this is neccessary?
CRITTER_CONFIG_ID="1t9yb9Wu4yKQBp6x3zgULOVrP6qsYe2Spfzr8zaF6UA8" #Critter config DB
SERVER_INVENTORY_DB="1VPCwp7lfDRKGRmRPq6u9LtTQEzlFpblFssnt30vvg7g" #Real inventory DB
#SERVER_INVENTORY_DB="1e7qavkpJOjUCJ5slD6TCvPBUhEglQ4ILVAfV0Cl4EtU" #Test inventory DB

#EMBED STUFF ------------------------------------------------------------------------------
#Embed Colors
pika_yellow=0xfcd127
paddle_red=0xd00047
gacha_color=0x8A6E98
reject_red=14358306
maint_grey=8421504
inv_purple=7815793
buy_indigo=741228
generic_blue=4553629
success_green=1408799
fall_auburn=13531154
help_orange=16015414
function_pink=15222869

#Embed Icons
trash_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/deexp8a-e0f06ddd-d9f5-48c4-adef-eadac52d78d6.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWV4cDhhLWUwZjA2ZGRkLWQ5ZjUtNDhjNC1hZGVmLWVhZGFjNTJkNzhkNi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.wuf8zxkEdkbXhuFiMJYyp-5hED4DLlmSGucfGzVnUwM"
shop_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjncnu-9d79ac1c-3221-461d-9715-8b9ec6e87a71.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuY251LTlkNzlhYzFjLTMyMjEtNDYxZC05NzE1LThiOWVjNmU4N2E3MS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.2SdvuFvLaVhioa3LxnVFy2RASXMN_R4obe4fDw9AcgQ"
exchange_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjnco8-7fdcade7-76d3-418b-b43c-69cebc31a28c.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuY284LTdmZGNhZGU3LTc2ZDMtNDE4Yi1iNDNjLTY5Y2ViYzMxYTI4Yy5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.aPrdaa-FpAfH1g832VFxUiM7VrpkYM8-2BXuqSTmo20"
dice_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn83s-dcdbdaf2-6d5a-4e40-afd6-d83ac7e220d5.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuODNzLWRjZGJkYWYyLTZkNWEtNGU0MC1hZmQ2LWQ4M2FjN2UyMjBkNS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.4zIX7yGw_7bJ41z04OzKJUvM0rTFt_xquIetzsypTig"
gift_red_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddswll5-f32d2b99-de79-4c24-a42b-d57547e38095.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZHN3bGw1LWYzMmQyYjk5LWRlNzktNGMyNC1hNDJiLWQ1NzU0N2UzODA5NS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.PB6bld7twft3asU1GM6HgQviRmamT-7hmtqlcAt1fFg"
defeat_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn4bi-87c1daa6-2f60-4dfc-a599-13e6562cf73a.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuNGJpLTg3YzFkYWE2LTJmNjAtNGRmYy1hNTk5LTEzZTY1NjJjZjczYS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.57yK9Bbrl0VJm3RQzsGJwkCSo1IT3iziBj7mveDkpNw"
injury_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddl2zm4-f17538ad-c1f8-494d-8649-7ccc2bbb67cb.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGwyem00LWYxNzUzOGFkLWMxZjgtNDk0ZC04NjQ5LTdjY2MyYmJiNjdjYi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.9mrYsmBsACvo06fipZCExAf6TE6KkLJPESsm4NIAQtU"
error_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn5lm-1798aeb1-d4f4-401b-9a3f-6d2aa94262b7.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuNWxtLTE3OThhZWIxLWQ0ZjQtNDAxYi05YTNmLTZkMmFhOTQyNjJiNy5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.F2xuRnG0tuX1hjZMKaAzlmQrxht_YF0L1qjaPF8_TNQ"
check_red_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjnrx0-4686d32c-ac3a-4885-93a9-ea6cb0a9c1be.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpucngwLTQ2ODZkMzJjLWFjM2EtNDg4NS05M2E5LWVhNmNiMGE5YzFiZS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.Q4LxajZ0smGBMz1RZX2_oVZxleHX_aJv3gNh6dj9IIk"
help_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn835-9f08c08b-bccf-4a41-92f3-8b07181614bb.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuODM1LTlmMDhjMDhiLWJjY2YtNGE0MS05MmYzLThiMDcxODE2MTRiYi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.3Awu1k61Q_gR8-K7tzGcPxNmuaOcQ9yycMGC_PTVJ2U"
inventory_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjnco1-b63d8d18-e9b5-4454-9a16-416e581d83bd.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuY28xLWI2M2Q4ZDE4LWU5YjUtNDQ1NC05YTE2LTQxNmU1ODFkODNiZC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.4lUxOVjABq47E1Zn1bclGW5MnFGNNsyK2UYcEUtQ-4I"
summer_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/deexpgz-913f224b-55c1-4d0f-9189-7c1e603f9b08.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWV4cGd6LTkxM2YyMjRiLTU1YzEtNGQwZi05MTg5LTdjMWU2MDNmOWIwOC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.KLJDD0RQmbJH7owOxkdQCTooMTSJqWhHkhQS9BWK3sM"
gift_orng_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddswlku-408a3413-61b7-4b6b-90aa-ad12a7087182.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZHN3bGt1LTQwOGEzNDEzLTYxYjctNGI2Yi05MGFhLWFkMTJhNzA4NzE4Mi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.rAPRD6sgP-aNk9o1yKAj7jYSRk-aKluW5BeieQO7Zjo"
sell_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn6pz-871e3fcb-c314-4d8f-9398-5f1cd3f23561.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuNnB6LTg3MWUzZmNiLWMzMTQtNGQ4Zi05Mzk4LTVmMWNkM2YyMzU2MS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.jSaeKvN-wh0djAcG9mx9vhdZTD3OyJOSe_1O7Coa9RE"
suggest_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn6pu-4015bd0a-3162-41c8-81bd-5738f7afb654.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuNnB1LTQwMTViZDBhLTMxNjItNDFjOC04MWJkLTU3MzhmN2FmYjY1NC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.QGkRcl8tms-lek_ZaNlD3uRrYk0Lfd-fzAZKuKQpP4Q"
voucher_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/de22h0b-07660744-1efd-43fb-a932-6fbd0a21f0fc.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZTIyaDBiLTA3NjYwNzQ0LTFlZmQtNDNmYi1hOTMyLTZmYmQwYTIxZjBmYy5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.x_YbBilNXLbps-QdLSGIR1nAYyA6WRf6lSd1sX9GmF4"
fall_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/deexp8m-71b4999c-5090-4249-b22b-4af76bc6c519.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWV4cDhtLTcxYjQ5OTljLTUwOTAtNDI0OS1iMjJiLTRhZjc2YmM2YzUxOS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.ZbhnZRgoS9XfkkLGEXFj8PrdCJ4EsxW_fNrH5U5Me-g"
gift_grn_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddswlky-0eeed367-710a-45f5-b321-6fbf5bad763d.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZHN3bGt5LTBlZWVkMzY3LTcxMGEtNDVmNS1iMzIxLTZmYmY1YmFkNzYzZC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.OdVL9zmt6tmoWBKY93Ht7IaqxnzjmcyqbdyKq1CumdI"
trophy_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn81o-74d251d9-61b4-4baf-9894-4fbd315d4439.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuODFvLTc0ZDI1MWQ5LTYxYjQtNGJhZi05ODk0LTRmYmQzMTVkNDQzOS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.qUli8-y0W6SHD4TcN8uKX7_H8OKKlOUdHrYegUtAUYA"
check_grn_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn5lj-c5cfc4f0-333f-4b1c-bcc6-76e57d609d4e.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuNWxqLWM1Y2ZjNGYwLTMzM2YtNGIxYy1iY2M2LTc2ZTU3ZDYwOWQ0ZS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.khRe0XBKwliyyZnRTz6VkyIJBCSSxbMNnz8GG2H01Lc"
calendar_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/de9bp1r-4a6c7667-fd88-4c9f-9dab-f00c3f9a7481.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZTlicDFyLTRhNmM3NjY3LWZkODgtNGM5Zi05ZGFiLWYwMGMzZjlhNzQ4MS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.n_X671nlj_Pdmjd5PaNlY4C5l4eax_bZoZ0axotyxHs"
spring_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/deexq98-071c5904-358d-4833-ab2f-e6b16b7915e0.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWV4cTk4LTA3MWM1OTA0LTM1OGQtNDgzMy1hYjJmLWU2YjE2Yjc5MTVlMC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.FsA_Gd6t3lyROz0noX7xOxIDPHCAACxXA8pQr6JA1jk"
tenant_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn81s-28cc6608-3008-4e1c-9408-25da5b99c163.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuODFzLTI4Y2M2NjA4LTMwMDgtNGUxYy05NDA4LTI1ZGE1Yjk5YzE2My5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.AbPhQblZRfq60OhM2OkiI8_ez0lqP3bEK_W2eimEGFM"
birthday_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddk47ro-31a2209c-3e9b-46e2-b9c9-39ebcad34ddf.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGs0N3JvLTMxYTIyMDljLTNlOWItNDZlMi1iOWM5LTM5ZWJjYWQzNGRkZi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.TlRdMhAFunvxSZxQVP4EksPax1vNmPT9Z2kq6dCzXSI"
egg_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddveu2p-ca10124c-8310-46a9-bb77-f4d3dfdfa9a6.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZHZldTJwLWNhMTAxMjRjLTgzMTAtNDZhOS1iYjc3LWY0ZDNkZmRmYTlhNi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.0Y8_2FDYwiijsGVZ95Kld58Y71ZiXJULFLz3YTTdlHU"
winter_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/de9bp1m-d7cfda7e-3956-4345-83a9-8ac717d75936.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZTlicDFtLWQ3Y2ZkYTdlLTM5NTYtNDM0NS04M2E5LThhYzcxN2Q3NTkzNi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.ZVzkm5RDKz-QnxvhRECkknhY2DwSLb7psshp5V_8vbA"
buy_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn840-3d5da377-59d0-4df0-be80-d550e08d8249.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuODQwLTNkNWRhMzc3LTU5ZDAtNGRmMC1iZTgwLWQ1NTBlMDhkODI0OS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.IFGtAR36h_zlg4aFK9KJaZNhld0umOnScYc0wH-Ghzk"
investigate_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn82x-69aab70f-65bf-4374-99c4-28d537ba2806.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuODJ4LTY5YWFiNzBmLTY1YmYtNDM3NC05OWM0LTI4ZDUzN2JhMjgwNi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.Ipd7M9WK2xXkcp8WevTTpn9HGfW-7jta1gfTuqBSWlA"
maintenance_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjn82s-97bb883e-baa2-43c5-a877-6ade2614bfa8.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpuODJzLTk3YmI4ODNlLWJhYTItNDNjNS1hODc3LTZhZGUyNjE0YmZhOC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.cLQGFA_NQcifhEtGBKG-Tyw8VCoj1vL5cg4pyPXvhg0"
pong_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/de1xypr-734bd2f5-f5ae-4fea-adb2-361a5a78c52e.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZTF4eXByLTczNGJkMmY1LWY1YWUtNGZlYS1hZGIyLTM2MWE1YTc4YzUyZS5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.VYUUem9VU5I4Ir9hI4oKxoWREvfxyvGl5RiBLD3h2D8"
gacha_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddj6u10-0d68ba43-b843-4dc3-bb2c-60f0fdb718fb.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGo2dTEwLTBkNjhiYTQzLWI4NDMtNGRjMy1iYjJjLTYwZjBmZGI3MThmYi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.dS0ynHajYAhWkAPAvxkJZJz2uXZWHvRTxCsbRDQrawE"
balance_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddj6u1p-329d8d16-5451-4be1-bee3-2d895c9bcbcf.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGo2dTFwLTMyOWQ4ZDE2LTU0NTEtNGJlMS1iZWUzLTJkODk1YzliY2JjZi5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.HMDFxbIY2DQ2HnWAd3e9HUYki8tFmSXfxHStW5l5mpI"
inv_event_icon="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/defaqim-5d530aa6-a6df-4a36-8bc2-6edbb236a6ed.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWZhcWltLTVkNTMwYWE2LWE2ZGYtNGEzNi04YmMyLTZlZGJiMjM2YTZlZC5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.Y-tTB9PRUwMXYBiD3SlBbUX33-D3z5UkD52TDWY7Kas"

#Embed Image URLs
cry_togepi_gif="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/ddjca1j-95c2e586-2be7-48c5-8ca7-1792a7387e82.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZGpjYTFqLTk1YzJlNTg2LTJiZTctNDhjNS04Y2E3LTE3OTJhNzM4N2U4Mi5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.x68Uw5WC95VXoofMAGRbgmAM3ZlkEcTwBLlprMaFKcY"
sleep_mon_gif="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/deeyd12-ba7de6cc-cc3b-4124-b301-c5956df6deb6.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWV5ZDEyLWJhN2RlNmNjLWNjM2ItNDEyNC1iMzAxLWM1OTU2ZGY2ZGViNi5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.hoo8lJejuwGYsCrLCMCt3CXxOgp9wagxmS_dwyZH9W8"
clef_comp_gif="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/deeyd16-d9c336bf-7776-4572-ad80-52276050ef3c.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWV5ZDE2LWQ5YzMzNmJmLTc3NzYtNDU3Mi1hZDgwLTUyMjc2MDUwZWYzYy5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.Q7zLl0bVtvf7rdhO85AiXX235uZB1OJntGYtBmCAcLA"
pika_tube_gif="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/deeyd1a-d4e0c987-9d9f-4570-8e8a-1dfa0229a43f.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWV5ZDFhLWQ0ZTBjOTg3LTlkOWYtNDU3MC04ZThhLTFkZmEwMjI5YTQzZi5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.K0H4owrWWvyLSzSCGZ90Q77UK2QDL1X_s4rCWzeNxlQ"
poke_hack_gif="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/deeyd0z-3e4997ee-6a99-42e6-8869-067c622cb087.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWV5ZDB6LTNlNDk5N2VlLTZhOTktNDJlNi04ODY5LTA2N2M2MjJjYjA4Ny5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.qm3gCUsrfltQhWBLk2SS_YqzfPeY4-fiYQlxHP5--xE"
pong_image = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/de1xypi-779e8a8d-76a8-4bd6-b9a3-1c645fed9870.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZTF4eXBpLTc3OWU4YThkLTc2YTgtNGJkNi1iOWEzLTFjNjQ1ZmVkOTg3MC5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.UAg8aCRAbIdoNxKu_B4fRl_Sw26W1jXZ4_Vs316eYpg"
swanna_image = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e79415c0-a34f-4c80-9308-18507a006b0d/defaah4-b9ce6d1f-c4df-42f9-a770-2fd2294a2636.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvZTc5NDE1YzAtYTM0Zi00YzgwLTkzMDgtMTg1MDdhMDA2YjBkXC9kZWZhYWg0LWI5Y2U2ZDFmLWM0ZGYtNDJmOS1hNzcwLTJmZDIyOTRhMjYzNi5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.i_6hiCzcpR-049Wm3gZPMOBZNlIIUyNB-Zy1JkF9k0s"

# DICTIONARIES AND LISTS ------------------------------------------------------------------------------------------
# HELP Dictionary (All available commands and explanations of them) by page
help_dict_1 = { #Available to GHOSTS and up
    'help':
        'Review all of ' + BOTNAME + "'s available commands and how to use them",
    'tenant':
        "Roll for a random tenant, which includes both a preview image and link"+
        " to the tenant's application",
    'join_<"role_name">':
        "Add yourself to select roles (check the "+channel_directory_link+" for a "+
        "list of current server roles)",
    'leave_<"role_name">': # ADD ROLE NAMES FOR PRONOUNS ETC.
        "Remove yourself from select roles (check the "+channel_directory_link
        +" for a list of current server roles)",
    'ping':
        'Allows you to play ping-pong with ' + BOTNAME + ' (and check his response time, too)'
}
help_dict_2 = { #Available to TENANTS and up
    'inventory': 'Quickly view your personal Member Database inventory',
    'balance': 'View your current PD and Shard balance',
    'balance_top': 'View a leaderboard showing members with the highest PD balance',
    'balance_critter': "View "+BOTNAME+"'s balance (collected via gift taxes!)",
    'shop': 'View the shop directory page',
    'shop_<"page_number">': 'View individual categories/pages of the shop'
}
help_dict_3 ={ #Available to TENANTS and up
    'buy_<"item">_<"quantity">': 'Purchase items from the shop',
    'sell_<"item">_<"quantity">':
        "Sell items to the shop and receive 1/4th the item's value in return " +
        "(currency type gained will depend on the item sold). You can also trash"+
        " unsellable items from your inventory with this command",
    'gift_<@user>_<"item_name">_<"item_quantity">':
        'Allows you to gift another member any non-Premium/special item in' +
        ' your main inventory. Does not apply to items located in tenant '+
        'inventories. PD is considered an "item" for the sake of gifting',
    'NEWgift_special_<@user>_<"item_name">_<"bag_type">':
        "Gift another member any specialty item in your inventory via a gift "+
        "bag or jumbo gift bag. If gifting shards, you must specify the item as "+
        '"# Shards" (even in the case of 1 Shard).'
}

help_dict_4 = { #Available to TENANTS and up
    'NEWgift_special_menu':
        "Check which items currently in your personal inventory can be gifted "+
        "with gift bags or jumbo gift bags",
    'NEWgift_special_menu_<"bag_type">':
        'View a list of all items that can be gifted with the specified gift '+
        'bag type ("gift bag" or "jumbo gift bag")',
    'exchange_shards_<"quantity">':
        'Exchange Shard(s) for PD (1 Shard = 50PD)',
    'suggest_<"suggestion_here">':
        "If you're not comfortable using the #suggestions channel, you can" +
        " send the mod team a discreet suggestion which will be reviewed "+
        "privately. Your name will appear on the submitted suggestion",
    'NEWodds_<"horror_type">_<"courage_level">_<"optional_items">_<"optional_curses">':
        'Use this command to simulate a horror fight. "Horror type" and "courage' +
        ' level" are always required. Include items and/or curses to see how they'+
        " change your odds"
}
help_dict_5 = { #Available to INTERNS and up
    'investigate_<"location_name">_<"optional_item">_<"optional_curse">':
        'Investigate for a member. Locations are required, but items are ' +
        'optional. Remember to account for any curses the character may be ' +
        "afflicted with. Make sure to identify the user you're rolling for " +
        " (but don't use an @) before executing this command",
    'horror_<"horror_type">_<"courage_level">_<"optional_items">_<"optional_curses">':
        'Use this command to fight a horror. "Horror type" and "courage level" ' +
        'are always required. Include items upon request, and curses if a tenant' +
        " has any. Make sure to identify the user you're rolling for (but don't"+
        " use an @) before executing this command",
    'curse_<"horror_type">':
        'For use if a tenant loses a battle with a horror (of any type)'+
        " and they're afflicted with a curse they already have. " + BOTNAME +
        " will re-roll a new curse for the tenant using all available curses " +
        " that the specified horror can afflict. Make sure to identify the user"+
        " you're rolling for (but don't use an @) before executing this command",
    'NEWraid_<"courage_level">_<"optional_blessings">_<"optional_curses">':
        'Roll a calculated damage output for a tenant fighting in a raid.'+
        ' "Courage level" is always required. Add in blessings and curses if'+
        " a tenant has any. Make sure to identify the user you're rolling for"+
        " (but don't use an @) before executing this command"
}
help_dict_6 = { #Available to INTERNS and up
    'hatch_<"#">_<"patterned_(optional)">_<"color-swapped_(optional)">_<"delta_(optional)">_<"fusion_(optional)">':
        'Hatch mystery eggs. "Number" is always required and specifies the number'+
        ' of eggs to hatch, while "patterned," "color-swapped," "Delta," and "fusion"'+
        ' are all optional if conditions are met. All optional traits can be '+
        'mixed/matched. Be aware that ALL rolled eggs will hatch with traits, if'+
        ' given. Traited eggs are best hatched one at a time to avoid risk of error',
    'gacha':
        "Roll the gacha for a member once they've activated a gacha token. " +
        "Once the item is rolled, place it in the requested tenant's inventory."+
        " Make sure to identify the user you're rolling for (but don't use an @) "+
        "before executing this command",
    'voucher_<optional @user>':
        'Roll a winning value for a redeemed PD voucher. ' +BOTNAME +
        " will automatically add this balance to a user's inventory " +
        "if you choose to @ them when executing this command"
}
help_dict_7 = { #Available to MODS and up
    'inventory_add_<@user>_<"existing member database tab name">':
        'This command must be performed for all new members in the Discord'
        ' before they can use some of ' + BOTNAME + "'s user-personalized "+
        "command functions",
    'inventory_update_<@user>_<"existing member database tab name">':
        'If someone’s Member Database tab name changes, run this command to '+
        'update the stored tab name for ' + BOTNAME + ', too',
    'inventory_view_<@user>':
        'Allows you to view the current Member Database tab name for this user,'+
        ' stored in ' + BOTNAME,
    'maintenance_<0_or_1>':
        'This will allow you to disable (0) or enable (1) ' + BOTNAME +
        ' across the entire server, preventing anyone from using commands',
    'injury_<"random",_or_a_specific_tenant_name">_<"injury_category">':
        'Select either a random or specific tenant and roll them an ' +
        'injury from the chosen category (categories: minor, moderate, severe'+
        ', critical, or random)'
}
help_dict_8 = { #Available to MODS and up
    'key_add_<@user>_<"quantity">':
        "Increases a member's tarnished room key purchase counter. Use this "+
        " command if someone purchases a tarnished room key through dA instead of " + BOTNAME,
    'key_view_<@user>':
        'View the total number of tarnished room keys purchased by this member',
    'key_delete_<@user>_<"quantity">':
        "Remove the specified number of tarnished room keys from a member's total"+
        " amount (useful in the case of an accidental purchase)",
    'NEWcomms_<"channel_or_announcement_type">_<"optional_message">':
        "Allows "+BOTNAME+' to manually make up for any missed announcements. Ent'+
        'er "investigation," "season," or "birthday" to send a belated auto-format'+
        'ted announcement for the specified type. Alternatively, link a channel nam'+
        'e and include a message to send a custom announcement to the specified chan'+
        "nel (don't include quotes surrounding the message, or they'll be included)"
}

#Sheet Tab Information
non_inv_tabs = [
"Tenant","Shop","Gachapon","Pokemon Hatches","Injuries","JoinableRoles",\
"Variable Config","Investigation Config","Horror Config","Horror Item \
Reward Pool","Investigation Item Reward Pool","User Info","Raid Config",
"Sell/Trash-Only Items","Gifting Items"
]
non_member_tabs = [ "Directory", "Critter" ]

#Emoji Arrays for Reaction Menus
emoji_numbers = [
    "1\u20e3","2\u20e3","3\u20e3","4\u20e3","5\u20e3","6\u20e3","7\u20e3","8\u20e3","9\u20e3",u"\U0001F51F"
]
shop_emoji_numbers = [
    "0\u20e3","1\u20e3","2\u20e3","3\u20e3","4\u20e3","5\u20e3",
    "6\u20e3","7\u20e3","8\u20e3","9\u20e3",u"\U0001F51F"
]
emoji_confirm = [ "\u2705","\u274c"]

#Emoji Array for "Balance Awards"
balance_emoji_medals = [
gold_medal_emoji, silver_medal_emoji, bronze_medal_emoji
]

#Shop Page Info
MAX_SHOP_PAGE = 8 # Max Shop Page
shop_titles = [
    "Character Creation","Investigation","Battle","Healing","Pet-Related",
    "Miscellaneous","OOC","Premium"
] # Shop Page Titles

#Season Arrays (Spring, Summer, Fall, Winter)
season_name = ["Spring","Summer","Fall","Winter"]
season_here = [
"Although slushy snow still coats the ground in some areas of the grounds, there\
's an underlying hint of warmth in the breeze. The days are getting longer, and \
the first hint of regrowth and renewal among the flora is starting to manifest.\
\n\nThe château season is now **spring**, and the wild Pokémon found outside dur\
ing investigations have rotated! Additionally, the Fragmented Stone questline is\
 now closed once more until summer.",
"The pleasantly warm days of late spring have started to give way to increasing\
ly hot temperatures. Plentiful springtime showers are ebbing away into occasional\
 summer thunderstorms, and on clear days the sun blazes long into the humid even\
 ings.\n\nThe château season is now **summer**, and the wild Pokémon found outside \
 during investigations have rotated! Additionally, the Fragmented Stone questlin\
 e is now available for the duration of the season.",
"Though the temperatures are still quite warm, the scent of pumpkin spice and \
sweet maple have taken to the air. Days grow ever shorter, and although it's \
still too early for leaf peeping season, cozy fashion is preparing to make a \
welcome comeback.\n\nThe château season is now **fall**, and the wild Pokémon \
found outside during investigations have rotated! Additionally, the Fragmented \
Stone questline is now closed once more until winter.",
"The trees, now bare, are buffeted by increasingly chilly gusts. A sense of sole\
mn quiet has settled over the grounds, and the sky is more-often-than-not a mass \
of swirling overcast clouds. Occasional flurries sprinkle to the ground, a harbin\
ger of the snowstorms to come.\n\nThe château season is now **winter**, and the wi\
ld Pokémon found outside during investigations have rotated! Additionally, the Fra\
gmented Stone questline is now available for the duration of the season."
]
season_color = [success_green,help_orange,fall_auburn,generic_blue]
season_icons = [spring_icon,summer_icon,fall_icon,winter_icon]

#List of Maintenance Images
maintenance_images = [cry_togepi_gif,sleep_mon_gif,clef_comp_gif,pika_tube_gif,poke_hack_gif]

#Hatch Optional Arguments
valid_hatch_args = ["color-swapped","Delta","patterned","fusion"]

#SHEET LOCATIONS OF USEFUL INFORMATION ------------------------------------------------------------
#Page 1 Commands
TENANT_LIST = "Tenant!A2:E200"
ROLES_LOC = "JoinableRoles!A2:C15"

#Inventory/Balance Commands
USER_INFO_LOC = "User Info!A2:C"
INVENTORY_LOC = "!C9:D56"
PD_BAL_LOC = "!D4:D4"
SHARD_BAL_LOC = "!D5:D5"
CRITTER_BALANCE_LOC = "Critter!W5:W5"

#Shop Command
SHOP_PAGE1 = "SHOP!A2:C"
SHOP_PAGE2 = "SHOP!E2:G"
SHOP_PAGE3 = "SHOP!I2:K"
SHOP_PAGE4 = "SHOP!M2:O"
SHOP_PAGE5 = "SHOP!Q2:S"
SHOP_PAGE6 = "SHOP!U2:W"
SHOP_PAGE7 = "SHOP!Y2:AA"
SHOP_PAGE8 = "SHOP!AC2:AE"
KEY_PRICE_INC_LOC = "Variable Config!G2"
key_name = 'tarnished room key' #Name of the "key" (not a location)

#Trading Commands (Buy, Sell, Gift, Exchange)
ALL_ITEMS_LOC = [SHOP_PAGE1,SHOP_PAGE2,SHOP_PAGE3,SHOP_PAGE4,\
SHOP_PAGE5,SHOP_PAGE6,SHOP_PAGE7,SHOP_PAGE8]
SELL_ITEMS_LOC = "Sell/Trash-Only Items!A3:B"
TRASH_ITEMS_LOC = "Sell/Trash-Only Items!D3:D"
BANNED_GIFT_LOC = "Variable Config!B2:B20"
GIFT_FEE_LOC = "Variable Config!A2"
EXCHANGE_RATE_LOC = "Variable Config!F2"
GIFT_ITEM_GUIDE_REG = "Gifting Items!A3:B"
GIFT_ITEM_GUIDE_JUMBO = "Gifting Items!D3:E"

#Investigation Command
INV_ROOM_RANGE = "!A2:I45"
INV_CONFIG_LOC = "Investigation Config!A1:G20"
SPECIAL_ENCOUNTER_LOC = "Variable Config!H2:H2"

#Horror Command
HORROR_OPT_ITEM_LOC = "Horror Config!B3:C11"
HORROR_OPT_CURSE_LOC = "Horror Config!B12:C21"
HORROR_HP_LOC = "Horror Config!E3:F8"
HORROR_HP_INC_LOC = "Horror Config!E11:F21"
HORROR_COURAGE_LOC = "Horror Config!H3:I8"
HORROR_COURAGE_INC_LOC = "Horror Config!H11:I15"
HORROR_COURAGE_DEC_LOC = "Horror Config!H17:I21"
HORROR_CHANCE_LOC = "Horror Config!K3"
HORROR_CHANCE_MOD_LOC = "Horror Config!K6:L21"
HORROR_SHARD_LOC = "Horror Config!N3:P8"
HORROR_SHARD_MUL_LOC = "Horror Config!N11:O21"
HORROR_ITEM_WIN_LOC = "Horror Item Reward Pool!A1:F"
HORROR_CURSE_LOC = "Horror Config!R3:T21"

#Raid Command
RAID_OPT_BLESS_LOC = "Raid Config!B3:C13"
RAID_OPT_CURSE_LOC = "Raid Config!B14:C21"
RAID_COURAGE_LOC = "Raid Config!E3:F8"
RAID_COURAGE_INC_LOC = "Raid Config!E11:F15"
RAID_COURAGE_DEC_LOC = "Raid Config!E18:F21"
RAID_CHANCE_LOC = "Raid Config!H3"
RAID_CHANCE_MOD_LOC = "Raid Config!H6:I12"
RAID_PD_MUL_LOC = "Raid Config!H16:I21"

#Simple Randomness Commands (Hatch, Gacha, Voucher)
HATCH_LOC = "Pokemon Hatches!A2:D"
SHINY_LOC = "Variable Config!C2"
POKE_TYPES_LOC = "Pokemon Hatches!F2:F"
GACHA_LOC = "Gachapon!A2:A500"
VOUCHER_INFO_LOC = "Variable Config!D2:E20"

#Injury Command
INJURY_INFO_MINOR = "Injuries!A2:B30"
INJURY_INFO_MODERATE = "Injuries!C2:D30"
INJURY_INFO_SEVERE = "Injuries!E2:F30"
INJURY_INFO_CRITICAL = "Injuries!G2:H30"
INJURY_INFO_RANDOM = "Injuries!I2:J30"

#TEXT STRINGS/MESSAGES TO THE USER-------------------------------------------------------------------
#Welcome Message
welcome_str = "Hey <@!%s>, welcome to Chai Château!\nOnce you fill out an introduct\
ion in <#%s>, you'll be given your guest access role—enjoy your stay!:ghost:"

#Generic Error Messages
invalid_tab_name = "It looks like **%s** doesn't exist in the Member Database. I\
 can only link to existing tabs.\n\nCheck your spelling and try again!"
no_inventory_tab = "It looks like **%s**'s inventory tab is not set up correctly.\
\n\nPlease notify a member of the mod team to resolve this issue."
inv_quantity_text = "You have to enter a positive number for quantity!"
unknown_tenant = "Sorry, I don't know who that is."
unknown_role_name = "Sorry, I don't know that role."
no_permission = "Sorry, but you can't do that at your current server rank."
invalid_command = "Hmm, I don't know how to do that.\n\nType `c!help` for a list of valid commands!"
too_many_args = "I wasn't expecting all those arguments! If you need help using \
the command, try `c!help`!"
expect_closing_quote = "If you open a quote for an argument, you need to close \
it!\n\n**Protip**: I only require quotes around arguments that include spaces."
unknown_user = "I don't know who you're referring to; next time try "+'"@"ing \
someone directly!'
missed_argument = "You cannot leave the %s blank."
wrong_argument = "I did not understand what you entered for "
serious_error = "Hmm, I don't know what happened.\n\nThe dev team has been \
notified and will look into it right away."
out_of_element_txt = ("Oops, I can't do that here.\n\nIf you'd like to use my \
commands, make sure you're in the **%s** server!" % DISCORD_GUILD)

#Tenant Command
tenant_text = "You received **[%s](%s)**!"

#Role Commands (join and leave)
join_text = 'You successfully joined the following role(s): **%s**'
unjoin_text = "You tried to join the following role(s), but you're already in them: **%s**"
leave_text = 'You successfully left the following role(s): **%s**'
no_role = "You don't have the **%s** role, so you can't leave it."

#Help Command
help_descr_text = "Click on the # reaction to flip through the pages\n------------------------------------------------------"
help_footer = 'Click on the # reaction to flip through the pages '
help_footer_done = "Too slow; enter c!help again to see another page "
page_error_text = "That's not a valid page number!"

#Inventory Commands
inventory_add_text = "%s's inventory tab name (**%s**) was successfully added to "+BOTNAME+" DB."
inventory_update_text = "%s's inventory tab name was successfully updated from **%s** to **%s** in "+BOTNAME+" DB."
inventory_view_text = "%s's tab name is currently saved as **%s**!"
yes_inventory_tab = "I already have an inventory tab for %s."
inventory_titles = '\n║ {:24s} ║ {:10s} ║\n'.format('"Item"','"Quantity"')
table_linebreak = '╠══════════════════════════╬════════════╣'
table_starter = '╔══════════════════════════╦════════════╗'
table_ender = '╚══════════════════════════╩════════════​╝'
inventory_header = table_starter+inventory_titles+table_linebreak
table_footer = "Click on the # reaction to flip through the pages | Current Page %i/%i"
inventory_footer_done = "Too slow; enter c!inventory again to see another page | Current Page %i/%i"
empty_inventory = "It looks like your inventory is empty."

#Balance Commands
balance_text = "**PokéDollars**: %s\n**Shard(s)**: %s"
critter_balance_text = "Critter has accumulated **%i PD** in pilfered gift taxes!"
balance_top_start = "Top Three:"
balance_leader = "%s**%s:** %i PD\n"
balance_mention_start = "Runner-Ups:"

#Shop Command
shop_menu_text = "If you'd like to see a specific category, type `c!shop \
<page number>` or use the reaction buttons below!"
shop_linebreak = '╠══════════════════════════╬════════════════╣'
shop_starter = '╔══════════════════════════╦════════════════╗'
shop_ender = '╚══════════════════════════╩════════════════​╝'
shop_titles_PD = '\n║ {:24s} ║ {:14s} ║\n'.format('"Item Name"','"PD Price"')
shop_titles_shards = '\n║ {:24s} ║ {:14s} ║\n'.format('"Item Name"','"Shard Price"')
shop_header_PD = shop_starter+shop_titles_PD+shop_linebreak
shop_header_shards = shop_starter+shop_titles_shards+shop_linebreak
shop_footer_done = "Too slow; enter c!shop again to see another page | Current Page %i/%i"

#Trade Commands (Buy, Sell, Exchange)
buy_success_text_pd = "You purchased **%s %s** for **%i** PokéDollars!"
buy_success_text_shards = "You purchased **%s %s** for **%i** Shards!"
sell_success_text_pd = "You sold **%s %s** for **%i** PokéDollars!"
sell_success_text_shards = "You sold **%s %s** for **%i** Shards!"
invalid_shop_item = "You can't %s **%s**!"
no_money_text = "Unfortunately, you don't have enough PD in your inventory \
to complete this transaction.\n\nYou currently have **%i** PD and are **%i** PD short."
no_shards_text = "Unfortunately, you don't have enough shards in your inventory \
to complete this transaction.\n\nYou currently have **%i** shard(s) and are **%i** shard(s) short."
not_enough_shards = "It looks like you're trying to exchange more Shards than you own!\
\n\nYou currently have **%i** shard(s) in your inventory."
exchange_success_text = "You exchanged **%i Shard(s)** for and received **%i PD** in return!"
no_item_text = "It looks like you don't have that many **%s**!\n\nI count **%i** in your inventory."
item_delete_question="The shop won't buy that item, but would you like to delete **%s** **%s** instead?"
item_delete_confirm = "You deleted **%s** **%s**"
item_delete_reject = "You decided not to delete any **%s**"
delete_timeout = 'Too slow; enter `c!sell` again to start over.'

#Gift Command
banned_item_text = "Although all information was entered correctly, %s can't be gifted with this command."
gift_cancel = "The gifting process has been cancelled."
gift_timeout = 'Too slow; enter `c!gift` again to start over.'
gift_bag_timeout = 'Too slow; enter `c!gift special` again to start over.'
gift_tax_expense_text = "Although all the information was entered correctly, you\
 don't have enough PD to cover the **%i** gift fee.\n\nIt looks like you're **%i** short."
gift_self = "I can't let you send a gift to yourself! Try sharing with your friends instead."
gift_receipt_text = "Congratulations! You've successfully gifted **%s**.\n\nHere is a copy \
of your receipt:\n\n**Sender:** %s\n**Recipient:** %s\n**Item:** %s\n**Amount:** \
%i\n**Gift Fee:** %i PD\n\n**TOTAL COST:** %i PD"
gift_bag_receipt_text="Congratulations! You've successfully gifted **%s**.\n\nHere is a copy \
of your receipt:\n\n**Sender:** %s\n**Recipient:** %s\n**Item:** %s\n**Bag Type:** %s"
gift_question_text = "You are about to send **%i %s** to **%s**. Factoring in \
the gift fee, this will cost **%i PD**.\n\nIs this okay?"
gift_bag_question_text = "You are about to send **%s** to **%s** in a **%s**.\
\n\nIs this okay?"
gift_message_text = "Congratulations! **%s** has sent you a gift!\n\n**%i %s** \
has been added to your inventory; enjoy! 🎁"
gift_message_shard_text = "Congratulations! **%s** has sent you a gift!\n\n**%s** \
has been added to your inventory; enjoy! 🎁"
gift_via_help_options = "I can only help you with a **Gift Bag** or a **Jumbo Gift Bag**!"
gift_via_help_descr = "Items in your inventory that you can gift using a bag \
(jumbo bags can also hold aything that a regular bag can hold)"
un_bag_item = "Something went wrong!\n\nEither you don't have any **%s**, or \
this item won't fit in a gift bag of this size."
not_enough_bags = "It looks like you are trying to gift a **%s** in a **%s**, \
but you only have one %s."
no_gift_bags = "You don't have any **%s** in your inventory!"
gift_shards_format = "To gift Shards, make sure to follow proper formatting (# Shards)."
gift_low_shards = "You don't have that many Shards!\n\nYou're trying to send **%i** shard(s)\
, but there are only **%i** shard(s) in your inventory."
gift_bag_shard_lim_text = "Ooops, it looks like you're trying to send more Shard\
s than this gift bag type can hold. A maximum of **15 Shards** will fit in a gift\
 bag, and a maximum of **25 Shards** will fit in a jumbo gift bag."
gift_special_invalid_bag = 'Although you may be able to gift this item, it will \
need to be sent in the appropriately-sized gift bag.\n\nCheck c!gift special \
menu <"gift bag type"> for a list of items you can send (specify either "gift \
bag" or "jumbo gift bag" to execute the command).'
gift_no_shards_dunk = "Somehow, you can feel a sense of overwhelming disappoint\
ment emanating from Critter.\n\n...Why would you go out of your way to gift 0 \
Shards to someone?\n//sad violin music// :pensive: :violin: "
gift_dm_error = "Although the gift was successfully prepared, I wasn't able to \
deliver it to **%s**.\n\nIf you believe this is an error, please let a mod know \
in "+channel_questions_link

#Suggestion Command
suggestion_ack_text = "Thank you for your suggestion!"
suggestion_send_text = "%s\n\n--"
suggestion_footer = "Submitted on · %s"

#Odds Command
banish_odds_text = "By my calculations, if your tenant uses a **Banishing Sigil**, they will have a\n\n\
**100%**\n\nchance to dunk on any horror type! " + horror_bonk_emoji
horr_odds_calc = "By my calculations, if your tenant has a courage of **%s** and\
 fights a **%s**,%s they'll have approximately a\n\n**%s**\n\nchance of winning!"
first_odds_calc = " with **%s**"
sec_odds_calc = " and **%s**"

#Investigation Command
exploration_results_text = "You decide to spend some time investigating the \
**%s**. While there, you find **%s**.\n\n(Remember to follow up with your \
comment chain in your [investigation journal](https://www.deviantart.com/chaistaff/journal/Investigation-842664943)!)"
exploration_results_text_nothing = "You decide to spend some time investigating the \
**%s**. While there, you find **%s**."
invalid_inv_item = "It looks like **%s** isn't a valid item for investigation!"
invalid_inv_curse = "It looks like **%s** isn't a curse that will affect investigation!"
item_or_curse_text = "Only one type of item and one type of curse can be applied to an\
 investigation at a time!\n\nPlease remove the excess variable(s) of these types, and try again."
swanna_encounter_text = "You decide to spend some time investigating the **pond**.\n\n\
It seems like there's nothing really out of the ordinary here today, and you peer\
 into the algae-coated water trying to see your reflection, or spot anything of \
interest under the murk. You contemplate picking up a rock and throwing it into \
the water, just to break the algae blooms on the far side of the pond, but a sud\
den loud *honk* grabs your attention.\n\nWhirling around, you see a large Swanna\
 staring you down. The two of you lock eyes, engaging in a battle of wits. Unfor\
tunately, after a moment, it seems like the Swanna decides actions speak louder\
 than stares. It honks once more and charges at you, beak snapping furiously as\
 it quickly chases you away.\n\nIt's a lovely day at the pond, but you encounte\
r a horrible Swanna."

#Horror Command
invalid_horr_item = "It looks like **%s** isn't an item that will affect horrors!"
invalid_curse = "It looks like **%s** isn't a curse that will affect combat!"
banish_horr_text = "Rather than gamble on an outcome, you take out a **banishing \
sigil** and prepate to remove the seal. You know that the %s won't be able to with\
stand its sheer power—it's a guaranteed victory!\n\n"
horror_challenge_text = "You chose to face the **%s**, knowing that it would take \
at least **%i** successful hit(s) to defeat it!\n\n"
horror_victory_text = "After a long hard battle, you emerge victorious having \
dealt **%s** hit(s) to the %s.\n\n"
horror_failure_text = "Even after giving it your all, you were unable to overcome \
the %s and could only land **%s** hit(s). Somehow, you were able to escape before \
it could overcome you entirely.\n\n"
invalid_courage_level = "The courage level you have enterred does not appear to exist."
invalid_horror_type = "The horror type you have enterred does not appear to exist."
incompat_horr_item = "Although the items were enterred correctly, they're \
incompatible with one another."
incompat_horr_curse = "Although the curses were enterred correctly, they're \
incompatible with one another."
won_shards_text = "_Rewards:_\nYou earned **%i** shard(s)\n"
lost_shards_text = "_Rewards:_\nYou didn't earn any shards\n"
item_prize_text = "You received **%s**"
lost_curse_text = "_Cursed:_\nAfter the battle, you realized you'd been \
afflicted with **%s**!"
lost_nothing_text = "Safe:\nThankfully you managed to get away without getting cursed!"

#Curse and Raid Commands
reroll_curse_text = "Your re-rolled **%s** curse is **%s**."
invalid_raid_bless = "It looks like **%s** isn't a valid blessing for a raid!"
incompat_raid_bless = "Although the blessings were entered correctly, they’re \
incompatible with each other.\n\nTry again using just one!"
raid_challenge_text = "You chose to enter this raid. Based on all entered variables,\
 you have **%i** chances to hit—let's see how many you deal!"
raid_complete_text = "After giving it your all, you managed to land **%i** hit(s)!"
raid_pd_mul_text = "Due to the **%s** at play during this roll, your raid \
thread word count PD earnings will be multiplied by **%.2f**!"

#Hatch Command
hatch_intro_text = "You feel the egg wiggle, and hear noises from inside. A \
moment later, cracks form in the shell's surface…\n\nCongratulations!\n"
hatch_egg_text = "A **%s** hatched from the egg.\n"
hatch_arg_text = ("You can only make eggs **%s**, **%s**, **%s**, and/or **%s** \
!" % (valid_hatch_args[0],valid_hatch_args[1],valid_hatch_args[2],valid_hatch_args[3]))

#Gacha Command
gacha_text = "You enter a token into the gacha and pull a giant lever. A moment \
later, your prize drops out.\n\nYou receive **%s**!"

#Voucher Command
voucher_text = "You scratch off the coating on the ticket, holding your breath...\n\n\
Congratulations! You won **%i PD**!"

#Maintenance Command
maintenance_off_text = "Maintenance mode is now **enabled**."
maintenance_on_text = "Maintenance mode is now **disabled**."
maintenance_wrong_text = "Improper use of **c!maintenance**\nPlease be sure to \
enter a 0 to disable maintenance or a 1 to enable it"
maintenance_block_text = "Sorry, I’m currently in maintenance mode.\n\nMods \
will announce when I’m back online!"

#Injury Command
injury_text = '**%s** has been afflicted with **%s**!\n\n*%s*'
injury_error_text = "I can only process minor, moderate, critical, severe, or \
random injuries!"

#Key Commands
key_add_text = "You've successfully incremented %s's tarnished room key amount by **%s**!"
key_delete_text = "You've successfully decreased %s's tarnished room key amount by **%s**!"
key_view_text = "%s has purchased **%s** tarnished room key(s)!"
not_enough_keys = "You can't delete more keys than a user has stored.\n\n\
%s currently has %s key purchases logged in Critter DB."

#Comms Command
belated_text = "I apologize for not sending this out earlier, but...\n\n"
inv_ann_or_chan = "I didn't recognize that channel name or announcement type. \
If you're referencing a channel,"+' make sure to link it directly (i.e. "#chann\
el-name"). Otherwise, I only support late announcements for birthdays, investiga\
tions, or season changes!'

#Automatic Announcements (Seasons, Birthday,Investigations are Open)
season_chg_text = "You sense a shift in the air, knowing instinctively that **%s** has drawn to a close.\n\n**%s** has begun!"
one_birthday_text = "Get ready to celebrate, because there's one birthday this week! 🎉🎂\n\n"
many_birthday_text = "Get ready to celebrate, because there's more than one birthday this week! 🎉🎂\n\n"
birthday_text = "**%s's** birthday is **%s**!\n"
birth_footer_text = "Be sure to wish them a happy birthday, and consider gifting\
 them something to commemorate the occasion!"
investigations_open_text = "Investigations are now open! 🔎\n\nPay a visit to \
the [investigation journal](https://www.youtube.com/watch?v=dQw4w9WgXcQ) to see what you find!"
