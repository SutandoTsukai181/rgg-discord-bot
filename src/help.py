
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
    """
}

GMT_CMD = ['i', 'o', 'ig', 'og', 'mtn', 'rst', 'rhct', 'aoff', 'rp', 'fc',
           'hn', 'bd','sgmd', 'tgmd', 'd', 'dr', 'ns', 'sf', 'cmb', 'z']

GMT_COMMAND = ['inpath', 'outpath', 'ingame', 'outgame',  'motion', 'reset',
               'resethact', 'addoffset', 'reparent', 'face', 'hand', 'body',
               'sourcegmd', 'targetgmd', 'dir', 'recursive', 'nosuffix', 'safe', 'combine', 'zip']

CMD_TO_COMMAND = dict(zip(GMT_CMD, GMT_COMMAND))

COMMAND_TO_CMD = dict(zip(GMT_COMMAND, GMT_CMD))

GMT_HELP = """```
A tool to convert animations between Yakuza games
Currently supported Games:
  - Yakuza 0:            y0
  - Yakuza Kiwami:       yk1
  - Yakuza Kiwami 2:     yk2
  - Yakuza 3:            y3
  - Yakuza 4:            y4
  - Yakuza 5:            y5
  - Yakuza 6:            y6
  - Yakuza Kenzan:       yken
  - Yakuza Ishin:        yish
  - Yakuza Dead Souls:   yds
  - FOTNS Lost Paradise: fotns
  - Judgment:            je

Note: All Dragon Engine games are the same, so y6 = yk2 = je

optional arguments:
  -h, --help            show this help message and exit
  -ig INGAME, --ingame INGAME
                        source game
  -og OUTGAME, --outgame OUTGAME
                        target game
  -mtn, --motion        output GMT will be used in 'motion' folder (for post-Y5)
  -rst, --reset         reset body position to origin point at the start of the animation

  -rp, --reparent       reparent bones for this gmt between models
  -fc, --face           translate face bones for this gmt between models
  -hn, --hand           translate hand bones for this gmt between models
  -bd, --body           translate body (without face or hand) bones for this gmt between models

  -ns, --nosuffix       do not add suffixes at the end of converted files
  
  -z,  --zip            compress files in a zip before uploading

EXAMPLE
Convert animations from Yakuza 5 to Yakuza 0
(source file is from Y5, target file will be used in Y0):

    .gmt -ig y5 -og y0 (and attach GMT file from Y5)
```"""

COKE = "https://cdn.discordapp.com/attachments/530840773214863360/760600014027227226/coke.mp4"

FAKEICHIBAN = "https://cdn.discordapp.com/attachments/530840773214863360/767357923268493312/unknown.png"

NAGOSHIPIC1 = "https://cdn.discordapp.com/attachments/530840773214863360/767357019522596885/unnamed-3.jpg"

NAGOSHIPIC2 = "https://cdn.discordapp.com/attachments/530840773214863360/767357019815936020/10054965473.jpg"

NAGOSHIBASED = "https://cdn.discordapp.com/attachments/530840773214863360/767360251136966657/nagositoshihiro-5.jpg"

NAGOSHISTARE = "https://cdn.discordapp.com/attachments/530840773214863360/767360285790699520/unknown.png"

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
