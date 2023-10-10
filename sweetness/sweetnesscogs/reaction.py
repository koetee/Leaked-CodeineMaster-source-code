import disnake
import json
import random
import requests
from disnake.ext import commands
from disnake import Localized
from disnake.enums import ButtonStyle, TextInputStyle

class ReactionView(disnake.ui.View):

    def __init__(self):
        super().__init__()

class reaction_cog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents=disnake.Intents.all(), command_prefix = "!")):
        self.bot = bot

    @commands.slash_command(description = 'Реакции')
    async def reaction(self, inter, тип: str = commands.Param(choices=[
        Localized("Обнять", key="A"), 
        Localized("Поцеловать", key="A"),
        Localized("Гладить", key="A"),
        Localized("Укусить", key="A"),
        Localized("Ударить", key="A"),
        Localized("Обидеться", key="A"),
        Localized("Улыбнуться", key="A"),
        Localized("Чмокнуть", key="A"),
        Localized("Любить", key="A"),
        Localized("Подмигнуть", key="A"),
        Localized("Пощекотать", key="A"),
        Localized("Пощечина", key="A"),
        Localized("Счастье", key="A"),
        Localized("Злость", key="A"),
        Localized("Обида", key="A"),
        Localized("Грусть", key="A"),
        Localized("Усталость", key="A"),
        Localized("Скучать", key="A"),
        Localized("Плакать", key="A"),
        Localized("Смущаться", key="A"),
        Localized("Кушать", key="A"),
        Localized("Спать", key="A")
        ]), пользователь: disnake.Member = None):

        if тип == 'Счастье':
            
            embed = disnake.Embed(title = 'Реакция: Счастье', description=f'{inter.author.mention}, **Счастлив**', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.pinimg.com/originals/4e/4a/ca/4e4aca6054a37384ac0beb7f3937cb01.gif", "https://i.pinimg.com/originals/3d/e0/49/3de049959eddeafc7657abb3b1000794.gif"]))
            return await inter.send(embed = embed)

        if тип == 'Злость':

            embed = disnake.Embed(title = 'Реакция: Злость', description=f'{inter.author.mention}, **Злой**', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.pinimg.com/originals/4a/6c/e2/4a6ce22d688219aa54a0054a01dc8c48.gif", "https://i.pinimg.com/originals/52/c4/d5/52c4d55c27725df1b0a35178ad7cbc08.gif", "https://i.pinimg.com/originals/f8/ce/8a/f8ce8a3d9e831a3136aafec10f40e3ce.gif", "https://i.pinimg.com/originals/60/7a/35/607a354344d527ff5868ad46ace65888.gif", "https://i.pinimg.com/originals/92/82/17/928217aafb58fcca098e849b640955e0.gif", "https://i.pinimg.com/originals/1e/9e/61/1e9e6102dfa99569529255eb0247ea5c.gif", "https://i.pinimg.com/originals/8e/50/1f/8e501f24ea6c0ca10ec3a2d2a5ab3b9e.gif", "https://i.pinimg.com/originals/fc/4d/2d/fc4d2d4559fcf3e0ce58a193f08302c4.gif", "https://i.pinimg.com/originals/46/96/af/4696afb89e604b48939d8cb7ef3ca4af.gif", "https://i.pinimg.com/originals/cf/23/c0/cf23c0bfeeaa93d6d497ced0f3345f1f.gif", "https://i.pinimg.com/originals/2c/e0/c0/2ce0c0331bf809d1381e04322432a82f.gif"]))
            return await inter.send(embed = embed)

        if тип == 'Обида':

            embed = disnake.Embed(title = 'Реакция: Обида', description=f'{inter.author.mention}, **Обиделся**', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.pinimg.com/originals/4a/6c/e2/4a6ce22d688219aa54a0054a01dc8c48.gif", "https://i.pinimg.com/originals/43/91/5b/43915b2d7d46311198a624953a4921e7.gif", "https://i.pinimg.com/originals/c8/bf/65/c8bf65854104f13e8e2cdc9453c5222f.gif", "https://i.pinimg.com/originals/34/24/df/3424df822494d78bc184aae3e14d84e3.gif", "https://i.pinimg.com/originals/dc/dd/62/dcdd62dd737493ba2d4518c051c7f6a6.gif", "https://i.pinimg.com/originals/5a/9a/3f/5a9a3f66719b97906c018818893093d7.gif", "https://i.pinimg.com/originals/63/a5/ec/63a5ecdca6be35c1573e52e4bfacb797.gif", "https://i.pinimg.com/originals/ab/d9/8c/abd98cfb3950fab15e3326a9a4d2ed1e.gif", "https://i.pinimg.com/originals/88/5c/db/885cdbb1e6950cefdc981db000079c85.gif", "https://i.pinimg.com/originals/eb/a7/e0/eba7e031e08314d0d7eee7a16941f997.gif", "https://i.pinimg.com/originals/cf/bc/06/cfbc067a1445d5baa5ca36cc2642a6c4.gif", "https://i.pinimg.com/originals/ab/d8/09/abd80931f9bf97dd7e039cc72e26285f.gif", "https://i.pinimg.com/originals/2a/ed/b9/2aedb9ff34aa111c5789004d22d05a78.gif"]))
            return await inter.send(embed = embed)

        if тип == 'Грусть':

            embed = disnake.Embed(title = 'Реакция: Грусть', description=f'{inter.author.mention}, **Грустит** <:cry:869842607923134464>', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://cdn.discordapp.com/attachments/786908599045062666/786928405802647572/sad11.gif", "https://cdn.discordapp.com/attachments/786908599045062666/786928434159943720/sad10.gif", "https://cdn.discordapp.com/attachments/786908599045062666/786928401097293824/sad8.gif", "https://i.gifer.com/origin/19/1900f80e21e467d37a610794d5d61159_w200.gif",  "https://i.gifer.com/origin/63/63fd77907ba7a983bd3d13fb17a1f42a_w200.gif",  "https://i.gifer.com/origin/31/31343d6885616dc015207b297d5d8547_w200.gif",  "https://i.gifer.com/origin/f8/f841e8721a46bfa2fce363e4de5c74b4_w200.gif",  "https://i.gifer.com/origin/fe/feee3b9080be38052a4ef5fa692e5f1a_w200.gif",  "https://i.gifer.com/origin/c5/c518bb097d1f4013170596fb4c712c77_w200.gif",  "https://i.gifer.com/origin/a9/a9a3eda931c9a7db13c4582237906272_w200.gif",  "https://i.gifer.com/origin/76/76388ec0721058c21fb03d6e833ff2ca_w200.gif",  "https://i.gifer.com/origin/28/2803fba3d7f7ca18c86f98a349feb0dd_w200.gif",  "https://i.gifer.com/origin/c3/c3c088c1dbaf514d63f952ffcae35a90_w200.gif",  "https://i.gifer.com/origin/db/db56569f1959e00a5da45a2d260d7e1c_w200.gif", "https://i.gifer.com/origin/58/58af1592dd330251817c866c750c0b32_w200.gif", "https://i.gifer.com/origin/73/7335d795aefbe0092f593a7f07f824ff_w200.gif", "https://i.gifer.com/origin/80/80ed3585e0b784c36c3302506d864b56_w200.gif", "https://i.pinimg.com/originals/39/4a/dd/394adda37132e4c1bbc68a0a70d483e5.gif", "https://i.pinimg.com/originals/f5/a7/8c/f5a78c110dcf14473d3d2f3b813b1bd5.gif", "https://i.pinimg.com/originals/6a/e4/a0/6ae4a0ce2705f31738917d0ad56f9606.gif", "https://i.pinimg.com/originals/7b/fa/2b/7bfa2bf4d9d81fbc9816f27ce8abe421.gif", "https://i.pinimg.com/originals/57/eb/9a/57eb9a2c94e1b0d7102ac16cdc4ce234.gif", "https://i.pinimg.com/originals/55/7b/f7/557bf718a9685f1522edbefe00a77bb1.gif", "https://i.pinimg.com/originals/79/61/71/796171e6eb9a8152709792d0ce13dfc4.gif", "https://i.pinimg.com/originals/6c/3e/38/6c3e382db9a5ce5461a6f0796d5bd076.gif", "https://i.pinimg.com/originals/81/a3/db/81a3dbccdb72be2e7e20dbbb056addc5.gif", "https://i.pinimg.com/originals/7b/8d/cb/7b8dcbdcc2798fc1e4d34eb4a73ac5f6.gif"]))
            return await inter.send(embed = embed)

        if тип == 'Скучать':

            embed = disnake.Embed(title = 'Реакция: Скучать', description=f'{inter.author.mention}, **Скучает**',color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.gifer.com/origin/2d/2d1110c911d766965cb1b9f19308bb99_w200.gif", "https://i.pinimg.com/originals/28/2d/14/282d146cf60819f6c4dc0d5dd394107d.gif" "https://i.pinimg.com/originals/c0/8e/fe/c08efe7356f36e19ee3e2489c10d31f3.gif" "https://i.pinimg.com/originals/df/1d/2e/df1d2e0e1594c20ec1696b2fa8d69427.gif" "https://i.pinimg.com/originals/a7/e8/e8/a7e8e8f9fd0a8784012d8f14b09da4a8.gif" "https://i.pinimg.com/originals/f5/fa/ac/f5faaccf8cc78a9c6138b3a8f8d875b6.gif" "https://i.pinimg.com/originals/71/75/fe/7175fe4b5e789b94b41a793e2fd4db3d.gif" "https://i.pinimg.com/originals/13/46/a3/1346a31e9251991791639c264b2ce0e5.gif" "https://i.pinimg.com/originals/29/7a/31/297a31dc45ba5402b338d6b7c0d6b5f8.gif" "https://i.pinimg.com/originals/81/b3/9f/81b39f20f9369290a0f3c8148427480e.gif" "https://i.pinimg.com/originals/27/0e/eb/270eeb3b2601c5b3942780875deba98e.gif" "https://i.pinimg.com/originals/fa/81/90/fa8190fce8783a1a4adb54a1a9886768.gif" "https://i.pinimg.com/originals/a1/38/9f/a1389f5050b3fc852219d68266f58cc1.gif"])).set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            return await inter.send(embed = embed)

        if тип == 'Плакать':
            embed = disnake.Embed(title = 'Реакция: Плакать', description = f'{inter.author.mention}, **Плачет**', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(['https://media.discordapp.net/attachments/940215517346680902/942056726587404348/5562b4bed7f4c0513b331384af28f9a4.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942056726587404348/5562b4bed7f4c0513b331384af28f9a4.gif', 'https://media.discordapp.net/attachments/940215517346680902/942056726952296458/a35b8773e58fa122a6a1018c61e3cf47.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942056727283630080/21d2a68c81790403a9acfe17255f0e84.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942057213562855494/bc3f8a43eb724cf9190c727516ab52d8.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942057213835501588/8c7590f4fdaf6629aafb63d666742489.gif'])).set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            return await inter.send(embed = embed)

        if тип == 'Смущаться':
            embed = disnake.Embed(title = 'Реакция: Смущаться', description = f'{inter.author.mention}, **Смущается**', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(['https://cdn.discordapp.com/attachments/940215517346680902/942094423553105980/blushing-16.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942094424211607562/b10159104084d5ecc1585559ed3e551f.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942094425025298492/NIdi.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942094425369247804/755P.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942094425683787837/Srtnu.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942094425981603850/tumblr_n7ed6g5DXi1ra23i2o1_500.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942094426329714698/f1de9ccd5575cda2010cc2431232f3409bc35677_hq.gif'])).set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            return await inter.send(embed = embed)

        if тип == 'Кушать':
            embed = disnake.Embed(title = 'Реакция: Кушать', description = f'{inter.author.mention}, **Кушает**')
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(['https://cdn.discordapp.com/attachments/940215517346680902/942144048632848394/YsqU.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942144048918069288/2d6cb496513924f0a76d81312ecde889.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942144049538822205/10em.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942144050331517030/84PF.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942144050931314698/68747470733a2f2f696d672e776174747061642e636f6d2f73746f72795f70617274732f313034373933303437342f696d616765732f313637313333313338376633396430643832363231353335393732322e676966.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942144051602391130/tumblr_lnc34oiTjU1qdd0yao1_500.gif']))
            return await inter.send(embed = embed)
        if тип == 'Спать':
            embed = disnake.Embed(title = 'Реакция: Спать', description = f'{inter.author.mention}, **Заснул(-а)**', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(['https://cdn.discordapp.com/attachments/940215517346680902/942165028092653668/anime-sleep-81.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942165028440768592/181223_1631.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942165028969259028/anime-sleep-1.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942165029283840000/anime-sleep-90.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942165029560680508/NlqN.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942165029963304960/sleepy-anime.gif', 'https://cdn.discordapp.com/attachments/940215517346680902/942165030709915658/anime-sleep-73.gif'])).set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            return await inter.send(embed = embed)

        if пользователь == inter.author or пользователь == None:
            embed = disnake.Embed(title = f'Реакция: {тип}', description = f'{inter.author.mention}, **Я** не могу **Вас** заставить сделать **это с собой**', color = 3092790)
            return await inter.send(embed = embed)

        if тип == 'Обнять':
            embed = disnake.Embed(description=f'{inter.author.mention}, **Обнял** {пользователь.mention}', color = 3092790)
            embed.set_footer(text = f"{inter.author}", icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://acegif.com/wp-content/gif/anime-hug-52.gif","https://acegif.com/wp-content/gif/anime-hug-38.gif","https://acegif.com/wp-content/gif/anime-hug-79.gif","https://acegif.com/wp-content/gif/anime-hug-12.gif","https://acegif.com/wp-content/gif/anime-hug-15.gif","https://acegif.com/wp-content/gif/anime-hug-20.gif","https://acegif.com/wp-content/gif/anime-hug-81.gif","https://acegif.com/wp-content/gif/anime-hug-21.gif","https://i.pinimg.com/originals/7d/5b/0d/7d5b0d5c810eb942687cdd4ef522687e.gif","https://i.pinimg.com/originals/b5/92/60/b5926059f0a94e7f5e254f6b8efdf2f4.gif","https://i.pinimg.com/originals/3c/8b/8e/3c8b8e69e2b55306ff8ec426ccbc5e4e.gif","https://i.pinimg.com/originals/10/69/92/1069921ddcf38ff722125c8f65401c28.gif","https://i.pinimg.com/originals/e7/78/e7/e778e7381c16d6ed0e647b501fab3648.gif","https://i.pinimg.com/originals/01/71/40/017140d418d6ca03fdb20f82ba8cab94.gif","https://i.pinimg.com/originals/c1/6f/e1/c16fe1dca28cda29db82003c1c67839c.gif","https://i.pinimg.com/originals/e9/d7/da/e9d7da26f8b2adbb8aa99cfd48c58c3e.gif","https://i.pinimg.com/originals/72/99/17/72991736cba02b5f78e441fb1a6fba90.gif","https://i.pinimg.com/originals/7e/dd/ed/7edded2757934756fdc240019d956cb3.gif","https://i.pinimg.com/originals/ea/e1/54/eae154c1c30cc252035e5648f29bf2a1.gif","https://i.pinimg.com/originals/73/7e/3a/737e3a166fd47efd613252867a2ef437.gif"]))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Поцеловать':
            embed = disnake.Embed(title = 'Реакция: Поцеловать', description = f'{inter.author.mention}, **Поцеловал** {пользователь.mention}', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://media.discordapp.net/attachments/736335716614668359/841957280610123816/99c41869ba1551575aefd9c8ffc533de.gif", "https://i.gifer.com/G9IU.gif", "https://media.discordapp.net/attachments/786908599045062666/793503449505202177/kiss_096.gif", "https://i.gifer.com/OICq.gif", "https://media.discordapp.net/attachments/786908599045062666/793503296202735636/kiss_112.gif", "https://media.discordapp.net/attachments/786908599045062666/793502176902250496/kiss_097.gif", "https://i.gifer.com/Jr4.gif", "https://media.discordapp.net/attachments/786908599045062666/793501191887388692/kiss1.gif", "https://media.discordapp.net/attachments/786908599045062666/793501233376788490/tenor_6.gif", "https://i.pinimg.com/originals/9e/27/e7/9e27e700c4dfc0391774b2fcff1df8a8.gif", "https://i.pinimg.com/originals/5b/eb/a6/5beba6684b17c115d3932e5340905d5a.gif", "https://i.pinimg.com/originals/0a/ac/39/0aac390dc598e22578ef476b0f41c0a3.gif", "https://i.pinimg.com/originals/d6/a7/74/d6a77447dcde409dd8bff80a9cb3ee28.gif", "https://i.pinimg.com/originals/31/13/e4/3113e4b762dbcbd7c6d25ffe01298356.gif", "https://i.pinimg.com/originals/d0/cd/64/d0cd64030f383d56e7edc54a484d4b8d.gif", "https://i.pinimg.com/originals/67/a6/5f/67a65f7af96a004463f2fc0a0654b6bd.gif", "https://i.pinimg.com/originals/b9/d6/35/b9d63598a999e14a27e0abb57287f178.gif", "https://i.pinimg.com/originals/d0/8b/c5/d08bc5bec3ebff5805ae2d984c4eccd5.gif", "https://i.pinimg.com/originals/52/6e/fb/526efba8f40105388d5c8f98d1558bd5.gif", "https://i.pinimg.com/originals/c1/e1/98/c1e198a514380ebc2956734024a815c9.gif", "https://i.pinimg.com/originals/4e/92/1c/4e921c6c5f2e0961d394773911c83dd8.gif"]))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Гладить':
            embed = disnake.Embed(description = f'{inter.author.mention}, **Гладит** {пользователь.mention}', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.gifer.com/origin/31/31838530c87e57e7cb4c5491823b75b8_w200.gif", "https://media1.tenor.com/images/857aef7553857b812808a355f31bbd1f/tenor.gif?itemid=13576017", "https://animegif.ru/up/photos/album/nov17/171114_4416.gif", "https://pa1.narvii.com/6570/403a1b651aac3b0ab43cea521770c201ab6e2374_hq.gif", "https://animegif.ru/up/photos/album/nov17/171120_3202.gif", "https://kinogud.files.wordpress.com/2019/08/giphy-1.gif?w=340&h=254", "https://i.pinimg.com/originals/3c/ac/21/3cac213405fcb7dcbd16983b333375f0.gif"]))
            await inter.send(embed = embed)

        if тип == 'Укусить':
            embed = disnake.Embed(title = 'Реакция: Укусить', description=f'{inter.author.mention}, **Укусил** {пользователь.mention}', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://media.tenor.com/images/333c4f19849451c7e1ddff454c9f9372/tenor.gif", "https://media.tenor.com/images/c7a2cae8cc126c2100aa6967cc379e99/tenor.gif", "https://media.tenor.com/images/8dcb92c129d419af60ae0a819c2b2624/tenor.gif", "https://media.tenor.com/images/8260bc43f1522aa93616ff5a4389f139/tenor.gif", "https://media.tenor.com/images/1e3821d132230c8810312f7553354743/tenor.gif", "https://media.tenor.com/images/305e145258e40216348e043de4d17d92/tenor.gif", "https://media.tenor.com/images/c597913f9c0127adb69e137a4ba90132/tenor.gif", "https://media.tenor.com/images/566f5113d70abeccfef712a200ddb35b/tenor.gif", "https://media.tenor.com/images/10334965b4feed4339bbfe93f622377c/tenor.gif", "https://media.tenor.com/images/15f524b4f1660f714abf4d72d9c56733/tenor.gif", "https://media.tenor.com/images/d65c8450c42e69ad37a694a043fee68e/tenor.gif"]))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Ударить':
            embed = disnake.Embed(title = 'Реакция: Ударить', description=f'{inter.author.mention}, **Ударил** {пользователь.mention}', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://media.tenor.com/images/00a3cca756b4bbae191ac33ccc6d7bcf/tenor.gif", "https://media.tenor.com/images/9c14d2d5dd918471954e5946166f3632/tenor.gif", "https://media.tenor.com/images/b11c79cf158d8c9bd6e721676b06ad73/tenor.gif", "https://media.tenor.com/images/5b668436338971d42469d7348a5340e5/tenor.gif", "https://media.tenor.com/images/eb379f98c7ced6d43a16e78dc25ae864/tenor.gif", "https://media.tenor.com/images/359a3a05dbde06a89cdcf494ad62bb5d/tenor.gif", "https://media.tenor.com/images/af3d8ead13bb5b59d0ba1d5efd3fcfa6/tenor.gif", "https://media.tenor.com/images/dfa40524e03f4b982de034980388ed7a/tenor.gif", "https://i.pinimg.com/originals/39/58/88/395888c0e70dd23c5a7bc76122f80088.gif", "https://i.pinimg.com/originals/2b/5d/7b/2b5d7bb1dd4a8e64869c33499c409582.gif", "https://i.pinimg.com/originals/1d/69/0a/1d690a2a0260d5ab8a6345f8d32897a6.gif", "https://i.pinimg.com/originals/16/43/66/1643662a7fbfe1eb9bdbb28307aae5d.gif", "https://i.pinimg.com/originals/5d/8c/3e/5d8c3e22af93ba560d318394ac0a9cc8.gif", "https://i.pinimg.com/originals/45/52/f6/4552f616a20c1b350b7c241e65c761bc.gif", "https://i.pinimg.com/originals/12/2b/6a/122b6af44fe8af50c1588068965374a7.gif", "https://i.pinimg.com/originals/7e/dd/d9/7eddd9138b71f55af25f85f3be76d35a.gif", "https://i.pinimg.com/originals/a8/d1/69/a8d169a5ec6ba89abfc185e288432702.gif", "https://i.pinimg.com/originals/84/2a/d7/842ad7c9f9aa462cddd41898f848e6ab.gif", "https://i.pinimg.com/originals/21/13/1e/21131e4b253b6f962ba44b0988a0a278.gif", "https://i.pinimg.com/originals/8d/e1/fb/8de1fb69956bf44000aa11a0f529d35f.gif", "https://i.pinimg.com/originals/13/5c/77/135c77da480fedcb11d01f2433d9217d.gif", "https://i.pinimg.com/originals/72/6f/c4/726fc4cb66d3749a786cb27c8237dfac.gif"]))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Обидеться':
            embed = disnake.Embed(title = 'Реакция: Обидеться', description=f'{inter.author.mention}, **Обиделся на** {пользователь.mention}', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.pinimg.com/originals/4a/6c/e2/4a6ce22d688219aa54a0054a01dc8c48.gif", "https://i.pinimg.com/originals/43/91/5b/43915b2d7d46311198a624953a4921e7.gif", "https://i.pinimg.com/originals/c8/bf/65/c8bf65854104f13e8e2cdc9453c5222f.gif", "https://i.pinimg.com/originals/34/24/df/3424df822494d78bc184aae3e14d84e3.gif", "https://i.pinimg.com/originals/dc/dd/62/dcdd62dd737493ba2d4518c051c7f6a6.gif", "https://i.pinimg.com/originals/5a/9a/3f/5a9a3f66719b97906c018818893093d7.gif", "https://i.pinimg.com/originals/63/a5/ec/63a5ecdca6be35c1573e52e4bfacb797.gif", "https://i.pinimg.com/originals/ab/d9/8c/abd98cfb3950fab15e3326a9a4d2ed1e.gif", "https://i.pinimg.com/originals/88/5c/db/885cdbb1e6950cefdc981db000079c85.gif", "https://i.pinimg.com/originals/eb/a7/e0/eba7e031e08314d0d7eee7a16941f997.gif", "https://i.pinimg.com/originals/cf/bc/06/cfbc067a1445d5baa5ca36cc2642a6c4.gif", "https://i.pinimg.com/originals/ab/d8/09/abd80931f9bf97dd7e039cc72e26285f.gif", "https://i.pinimg.com/originals/2a/ed/b9/2aedb9ff34aa111c5789004d22d05a78.gif"]))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Улыбнуться':
            embed = disnake.Embed(description=f'{inter.author.mention} **Улыбнулся** {пользователь.mention}', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.pinimg.com/originals/c4/9d/c9/c49dc9422aac61eebbf8ae9d42bb26b7.gif", "https://i.pinimg.com/originals/1f/e9/35/1fe93596a8a0f84078b936305b319c55.gif", "https://i.pinimg.com/originals/6b/fc/bb/6bfcbb252a151933a16fe101c77cc9fa.gif", "https://i.pinimg.com/originals/de/20/ad/de20ad92370bc4b3657010e1db3ecdf0.gif", "https://i.pinimg.com/originals/4e/0a/40/4e0a400d7621b5452854bcae00d9a98e.gif", "https://i.pinimg.com/originals/63/af/95/63af95fffcfb022c921ea30cecda6aa5.gif", "https://i.pinimg.com/originals/8b/99/4b/8b994b9cb72211864190b84f2a2f72f2.gif", "https://i.pinimg.com/originals/4a/10/08/4a1008c8afc04bbc8948c7c77c4b0a50.gif", "https://i.pinimg.com/originals/fa/20/0d/fa200de4feb46078d7de05734362edba.gif", "https://i.pinimg.com/originals/e2/ad/f0/e2adf0a10cc5fe4381dcca1003fd3837.gif", "https://i.pinimg.com/originals/e1/d7/17/e1d717919e620927a0c219d5342d9bc8.gif", "https://i.pinimg.com/originals/c3/01/c6/c301c6a851de4e474f46f3ab0af0d9c7.gif", "https://i.pinimg.com/originals/7a/84/64/7a846448bcd01a67a35c549097119c65.gif", "https://i.pinimg.com/originals/7b/30/a1/7b30a1b11c67a3621a2fbd27a62f47f9.gif"]))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Чмокнуть':
            embed = disnake.Embed(title = 'Реакция: Чмокнуть', description=f'{inter.author.mention} **Чмокнул** {пользователь.mention}', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.pinimg.com/originals/5f/8a/9a/5f8a9a54d356c0b2c59b4b7561fcff62.gif", "https://i.pinimg.com/originals/09/39/ae/0939ae60d616a4c7265da52e4abd0089.gif", "https://i.pinimg.com/originals/65/a6/3a/65a63a319a598ac908960bfc4b6f89ff.gif", "https://i.pinimg.com/originals/ae/97/47/ae9747f76a390d9ce192c8082f61df85.gif", "https://i.pinimg.com/originals/0e/c5/38/0ec5382910e34ca5649f6c328124daa1.gif", "https://i.pinimg.com/originals/50/3b/b0/503bb007a3c84b569153dcfaaf9df46a.gif", "https://i.pinimg.com/originals/58/09/6c/58096c8f671fe5b7e009e333b21cfe02.gif"]))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Любить':
            embed = disnake.Embed(title = 'Реакция: Любить', description=f'{inter.author.mention} **Любит** {пользователь.mention}', color=3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(["https://i.pinimg.com/originals/de/f1/6e/def16e58f6af13e17445de08e1494506.gif", "https://i.pinimg.com/originals/42/92/2e/42922e87b3ec288b11f59ba7f3cc6393.gif", "https://i.pinimg.com/originals/ef/02/d1/ef02d189f05a0ca531ecc6afcb5e8204.gif", "https://i.pinimg.com/originals/41/f4/7e/41f47ee201db2de0d1865ce898ccd781.gif", "https://i.pinimg.com/originals/b6/7f/c2/b67fc226c4d2403423a3dc6cb95eb128.gif", "https://i.pinimg.com/originals/ac/03/e7/ac03e706cc6edf8b13695a8a7badbaab.gif", "https://i.pinimg.com/originals/11/0d/bd/110dbddfd3d662479c214cacb754995d.gif", "https://i.pinimg.com/originals/0a/32/03/0a3203ced13826a92230cc61214318da.gif", "https://i.pinimg.com/originals/fd/af/ba/fdafbad47d6a69cb5d3a90a8b9dff86f.gif", "https://i.pinimg.com/originals/e8/58/67/e858678426357728038c277598871d6d.gif", "https://i.pinimg.com/originals/e2/cc/aa/e2ccaa166f02dc682b1bda52908eb43c.gif"]))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Подмигнуть':
            embed = disnake.Embed(title = 'Реакция: Подмигнуть', description=f'{inter.author.mention} **Подмигивает** {пользователь.mention}', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = json.loads(requests.get('https://some-random-api.ml/animu/wink').text)['link'])
            await inter.send(embed = embed)

        if тип == 'Пощекотать':
            embed = disnake.Embed(title = 'Реакция: Пощекотать', description=f'{inter.author.mention} **Щекочет** {пользователь.mention}', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(['https://i.gifer.com/KVjQ.gif', 'https://i.gifer.com/O4QR.gif', 'https://66.media.tumblr.com/e6d1a1cd2499e37f14118a75d5e36da4/tumblr_og7p24fa3R1vpbklao6_500.gif']))
            await inter.send(пользователь.mention, embed = embed)

        if тип == 'Пощечина':
            embed = disnake.Embed(title = 'Реакция: Пощечина', description=f'{inter.author.mention} **Дал леща** {пользователь.mention}', color = 3092790)
            embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            embed.set_image(url = random.choice(['https://i.gifer.com/79zo.gif', 'https://safebooru.org/images/1882/605143df221803e99f3b5423f1df4c8b76bd8ae9.gif?1964756', 'https://i.kym-cdn.com/photos/images/original/001/040/951/73e.gif', 'https://i.pinimg.com/originals/ea/ef/89/eaef89e2d6534aebddc2364610dc1254.gif', 'https://i.pinimg.com/originals/9b/25/d2/9b25d2df9bda0c68ad80e2cfcc34e4c5.gif', 'https://i.pinimg.com/originals/e1/af/db/e1afdb021c3f837dc8f105c5501f1a1c.gif', 'https://i.pinimg.com/originals/6a/01/9d/6a019dee74f0ef1ed8315db7dba972f7.gif', 'https://i.pinimg.com/originals/88/84/56/888456a32ca21580d340874e7a7a3a8e.gif', 'https://i.pinimg.com/originals/35/35/42/3535424558edb729addffd6f08cc293d.gif']))
            await inter.send(пользователь.mention, embed = embed)

def setup(bot): 
    bot.add_cog(reaction_cog(bot))