
HELP = {
    'bin': """Supported formats: ARMP
Usage: attach the .bin file to the message. The file format will be detected automatically.
    """,
    'armp': """Converts DE armp BIN files to and from JSON.
Usage: attach a .bin or .json to the message.
    """,
    'gmt': """Converts GMT files between Yakuza games
Usage: attach the file to the message and enter the required arguments.\n
For more details, type \'-h\' at the end of the command.
    """,
    'ignore': """Ignores a user for the specified amount of time.\n
Usage: `.ignore <@User> <time><format>`\n
where time can be any valid float number, and format can be either `s` for seconds,
`m` for minutes, or `h` for hours. To revoke the timer, use `.ignore <@User> revoke`.
Using `.ignore <@User> forever` will not set a timer, but the command can still be revoked.

This can be used on users, roles, and channels.
    """,
    'purge': """Purges bot command messages.\n
Usage: `.purge <@User> in <@channel>` or `.purge <@User>`.\n
The first command will remove all messages from a specific user with a Nagoomba command 
in them, in the specified channel.

The second command will remove all command messages from that user server-wide. If the second 
command is used on a channel, it will remove all command *and* bot messages in that channel.

Using `.purge all` will remove all command and bot messages in the server. You can additionally add 
a number at the end of the command to set the check limit (number of messages to be checked for each channel).

This can be used on users, roles, and channels.
    """
}

GMT_CMD = ['i', 'o', 'ig', 'og', 'mtn', 'rst', 'rhct', 'aoff', 'rp', 'fc',
           'hn', 'bd', 'sgmd', 'tgmd', 'd', 'dr', 'ns', 'sf', 'cmb', 'sp', 'z', 'l']

GMT_COMMAND = ['inpath', 'outpath', 'ingame', 'outgame',  'motion', 'reset',
               'resethact', 'addoffset', 'reparent', 'face', 'hand', 'body',
               'sourcegmd', 'targetgmd', 'dir', 'recursive', 'nosuffix', 'safe', 'combine', 'speed', 'zip', 'link']

CMD_TO_COMMAND = dict(zip(GMT_CMD, GMT_COMMAND))

COMMAND_TO_CMD = dict(zip(GMT_COMMAND, GMT_CMD))

GMT_HELP_1 = """```
GMT Converter v0.5.4
By SutandoTsukai181

A tool to convert animations between Yakuza games
Currently supported Games:
  - Yakuza 0:             y0
  - Yakuza Kiwami:        yk1
  - Yakuza Kiwami 2:      yk2
  - Yakuza 3:             y3
  - Yakuza 4:             y4
  - Yakuza 5:             y5
  - Yakuza 6:             y6
  - Yakuza 7:             y7
  - Yakuza Like A Dragon: ylad (same as y7)
  - Yakuza Kenzan:        yken
  - Yakuza Ishin:         yish
  - Yakuza Dead Souls:    yds
  - FOTNS Lost Paradise:  fotns
  - Judgment:             je

Note1: Conversion might not properly work for some specific combinations
Note2: All Dragon Engine games are the same, so y6 = yk2 = je = y7 = ylad

EXAMPLE
Convert animations from Yakuza 5 to Yakuza 0
(source file is from Y5, target file will be used in Y0):

    .gmt -ig y5 -og y0 (and attach GMT file from Y5)
```
(Page 1/3)"""

GMT_HELP_2 = """```
Arguments (1/2):
  -h, --help            show this help message
  -ig INGAME, --ingame INGAME
                        source game
  -og OUTGAME, --outgame OUTGAME
                        target game

  -d, --dir             multiple file mode
  -l LINK, --link LINK
                        URL of input file (only one URL allowed)
  -z, --zip             compress files in a zip before uploading
  -ns, --nosuffix       do not add suffixes at the end of converted files
  
  -cmb, --combine       combine split animations inside a directory
                        (for auth cutscenes, currently works only with Y5 and older games)
                        [WILL NOT CONVERT]

  -sp SPEED, --speed SPEED
                        factor of the animations speed
                        must be in the form of x/y where both x and y are integers
                        [2 will double the speed, 1/2 will change it to half the speed]
```
(Page 2/3)"""

GMT_HELP_3 = """```
Arguments (2/2):
  -i INPATH, --inpath INPATH
                        filename of the main GMT to be used with --resethact
  -mtn, --motion        output GMT will be used in 'motion' folder (for post-Y5)
  -rst, --reset         reset body position to origin point at the start of the animation
  -rhct, --resethact    reset whole hact scene to position of the input GMT
                        (requires multiple files (or a zip) and for -i to be the name of the main 
                        GMT) [overrides --reset]
  -aoff ADDOFFSET, --addoffset ADDOFFSET
                        additional height offset for resetting hact scene (for pre-DE hacts)
                        [will be added to scene height]

  -rp, --reparent       reparent bones for this GMT between models
  -fc, --face           translate face bones for this GMT between models
  -hn, --hand           translate hand bones for this GMT between models
  -bd, --body           translate body (without face or hand) bones for this GMT between models
  -sgmd SOURCEGMD, --sourcegmd SOURCEGMD
                        name of the source GMD for translation, if uploading a zip
  -tgmd TARGETGMD, --targetgmd TARGETGMD
                        name of the target GMD for translation, if uploading a zip
```
(Page 3/3)"""

DISCORD_LINK = 'cdn.discordapp'

COKE = "https://cdn.discordapp.com/attachments/530840773214863360/760600014027227226/coke.mp4"

FAKEICHIBAN = "https://cdn.discordapp.com/attachments/530840773214863360/767357923268493312/unknown.png"

FAKERICHIBAN = "https://cdn.discordapp.com/attachments/766669259949998141/769991149028638730/smug.PNG"

NAGOSHIPIC1 = "https://cdn.discordapp.com/attachments/530840773214863360/767357019522596885/unnamed-3.jpg"

NAGOSHIPIC2 = "https://cdn.discordapp.com/attachments/530840773214863360/767357019815936020/10054965473.jpg"

NAGOSHIBASED = "https://cdn.discordapp.com/attachments/530840773214863360/767360251136966657/nagositoshihiro-5.jpg"

NAGOSHISTARE = "https://cdn.discordapp.com/attachments/530840773214863360/767360285790699520/unknown.png"

CBT = "https://cdn.discordapp.com/attachments/530840773214863360/769985966752268298/1ca30dfeb3b34d76ad220641a3f724f0.jpeg"

BASEDBOT = "https://cdn.discordapp.com/attachments/766669259949998141/769996331736891402/1q9v442.png"

DAY = "https://cdn.discordapp.com/attachments/530840773214863360/760247493698125884/unknown.png"

BASADO1 = "https://cdn.discordapp.com/attachments/766669259949998141/770175971357622312/sombrero.png"

BASADO2 = "https://www.youtube.com/watch?v=q-Rqdgna3Yw"

YMCA = "https://www.youtube.com/watch?v=CS9OO0S5w2k"

RELEASES = "https://cdn.discordapp.com/attachments/637676458856284161/815242651292270632/unknown.png"

WORK_EMOTES = {
    'Y0': '<:Y0:769491151467970590>',
    'YK1': '<:YK1:769492165079859210>',
    'YK2': '<:YK2:769492309695266836>',
    'Y3': '<:Y3:769492778240442388>',
    'Y4': '<:Y4:769492778170056714>',
    'Y5': '<:Y5:769492778161274911>',
    'Y6': '<:Y6:769492778244767764>',
    'Y7': '<:Y7:769492778182770698>',
    'YKEN': '<:YKEN:769492777859547148>',
    'YISH': '<:YISH:769492777821011980>',
    'YDS': '<:YDS:769492780342706207>',
    'FOTNS': '<:FOTNS:769492778085253120>',
    'JE': '<:JE:769493173394210826>'
}

EMOTES = {
    'MadDogOfDojima': '<:MadDogOfDojima:506552806224822283>',
    'ShockedNishiki': '<:ShockedNishiki:513472835545726998>',
    'OkitaShocked': '<:OkitaShocked:514527978349264936>',
    'KiryuChan': '<:KiryuChan:530842357554348062>',
    'RyomaInterested': '<:RyomaInterested:535874539385782292>',
    'TryAgain': '<:TryAgain:544077753364774912>',
    'Kyodai': '<:Kyodai:562662923495931934>',
    'Munancho': '<:Munancho:565547922343854091>',
    'CharmingFace': '<:CharmingFace:575769495621206037>',
    'Harooka': '<:Harooka:582867733931098112>',
    'aH': '<:aH:582932657068048384>',
    'Yuya': '<:Yuya:582936615157235712>',
    'Revelation': '<:Revelation:582937300791722004>',
    'SleepyKiryu': '<:SleepyKiryu:582937321830088754>',
    'Haruka': '<:Haruka:582937571164946492>',
    'KiryuThumb': '<:KiryuThumb:584751224713379843>',
    'Nugget': '<:Nugget:589784427610112010>',
    'NishikiBruh': '<:NishikiBruh:589784915113934879>',
    'Yulol': '<:Yulol:594447392162447383>',
    'LetDown': '<:LetDown:597355737710329867>',
    'Soijima': '<:Soijima:599255693836681216>',
    'YuyaTime': '<:YuyaTime:610182439784153128>',
    'Annoying': '<:Annoying:621783617001226241>',
    'LeftLegForbiddenOne': '<:LeftLegForbiddenOne:621808538049577021>',
    'RightLegForbiddenOne': '<:RightLegForbiddenOne:621808538066485259>',
    'KiryuForbiddenOne': '<:KiryuForbiddenOne:621808538720927749>',
    'PoleKiryu': '<:PoleKiryu:622176763308408892>',
    'KaoruAngery': '<:KaoruAngery:622379318781280256>',
    'TanimuraEyes': '<:TanimuraEyes:622427345768153101>',
    'Skelebana': '<:Skelebana:636277401919422465>',
    'OdaNoLikeGoddoHand': '<:OdaNoLikeGoddoHand:637812607989973013>',
    'yourebuttugly': '<:yourebuttugly:642785512419098638>',
    'objectionkiryu': '<:objectionkiryu:642785513765470210>',
    'greeddojima': '<:greeddojima:642785513857613845>',
    'sadjima': '<:sadjima:642785515468488724>',
    'SaekoThumbsUp': '<:SaekoThumbsUp:657715170616934401>',
    'peacockyourmom': '<:peacockyourmom:683036625592123441>',
    'harutowtf': '<:harutowtf:683039970536980513>',
    'twoeyedbastard': '<:twoeyedbastard:683040978386681969>',
    'madjima': '<:madjima:684509909248770083>',
    'SmugOda': '<:SmugOda:684514311300972596>',
    'TFWujustplaceholder': '<:TFWujustplaceholder:684514546299568172>',
    'AmazedKiryu': '<:AmazedKiryu:684514697847767044>',
    'RyomaNotAmused': '<:RyomaNotAmused:684514881277394990>',
    'Hapjima': '<:Hapjima:684517622989324322>',
    'hackfraudYokoyama': '<:hackfraudYokoyama:691663094115467355>',
    'IchiWHAT': '<:IchiWHAT:692128431655092314>',
    'IchiMAD': '<:IchiMAD:692129356923011152>',
    'NANI': '<:NANI:695258948831281212>',
    'SaejimaPray': '<:SaejimaPray:697569373392601258>',
    'NagumoBruh': '<:NagumoBruh:698996677704548483>',
    'Suffering': '<:Suffering:699743986998312981>',
    'BRUHjima': '<:BRUHjima:704963129909444618>',
    'UlalaScared': '<:UlalaScared:705218362359414784>',
    'RyujiCool': '<:RyujiCool:708735951874293862>',
    'NishiNani': '<:NishiNani:708736073962094614>',
    'MEENAAAAY': '<:MEENAAAAY:708787577540575242>',
    'KaoruEdgy': '<:KaoruEdgy:708788193545420812>',
    'AkiyamaCannotUnsee': '<:AkiyamaCannotUnsee:711479345759387659>',
    'RUFF': '<:RUFF:713814416725901383>',
    'Haruka_Whatthe': '<:Haruka_Whatthe:714791881296576583>',
    'pain': '<:pain:719508168903753749>',
    'EpicNagoshi': '<:EpicNagoshi:722975977751445555>',
    'KiryuGun': '<:KiryuGun:723331240106917941>',
    'KiryuCalling': '<:KiryuCalling:723331295270273085>',
    'Cocaine': '<:Cocaine:723632592376823819>',
    'smugjima': '<:smugjima:724364537633046579>',
    'consistency': '<:consistency:724366173952540693>',
    'DaigoNaniEyes': '<:DaigoNaniEyes:725066663803879504>',
    'releasesbro': '<:releasesbro:725067259420344431>',
    'BruhWhat': '<:BruhWhat:729893953020624980>',
    'intimacy': '<:intimacy:734658514370297876>',
    'Swolekiyama': '<:Swolekiyama:737376918701342801>',
    'Clownmura': '<:Clownmura:737377151141019719>',
    'cocaine_studio': '<:cocaine_studio:738458771621413054>',
    'horror': '<:horror:741316503948886077>',
    'KiryuStare': '<:KiryuStare:752259147981914172>',
    'KiryuPog': '<:KiryuPog:762998282145234946>',
    'MajimaSlap': '<:MajimaSlap:763033562554695681>',
    'death': '<:death:765535754318512129>',
    'HamuraShock': '<:HamuraShock:765654221785530448>'
}
