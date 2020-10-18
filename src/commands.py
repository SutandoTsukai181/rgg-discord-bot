import os, sys
import zlib, zipfile
from io import BytesIO, StringIO
from math import ceil
from json import loads, dumps
import random

from discord import File, utils, DMChannel
from discord.ext import commands
from dotenv import load_dotenv

from help import *
from utils import *
from reARMP import reARMP
from gmt_converter.main import convert_from_buffer

load_dotenv()

CHANNELS = os.getenv('DISCORD_CHANNELS')

def in_channel(ctx):
    return ctx.message.channel.name in CHANNELS if type(ctx.message.channel) is not DMChannel else True
"""
def has_files(ctx):
    if not len(ctx.message.attachments):
        content = [a.lstrip(' -') for a in ctx.message.content.lower().split(' ')]
        
        for m in ['h', 'help', 'd', 'dir']:
            if m in content:
                return True
        await ctx.send("No files were attached to the message. Aborting.")
        return False
    return True
"""
@commands.command(checks=[in_channel], brief="Converts BIN files", help=HELP['bin'])
async def bin(ctx):
    await ctx.message.channel.send("Unimplemented")

@commands.command(checks=[in_channel], brief="Es Cocaina")
async def pruebala(ctx):
    await ctx.message.channel.send(f"es cocaina {EMOTES['Cocaine']}\n{COKE}")

@commands.command(checks=[in_channel], brief="Based on what?")
async def based(ctx):
    await ctx.message.channel.send(f"Based? Based on what?\n{NAGOSHIBASED}")

@commands.command(checks=[in_channel], brief="...")
async def stare(ctx):
    await ctx.message.channel.send(NAGOSHISTARE)

@commands.command(checks=[in_channel], brief="Professional beef bowl face")
async def ichireal(ctx):
    await ctx.message.channel.send(FAKEICHIBAN)

@commands.command(checks=[in_channel], brief="Nagoshi sent you a dick pic")
async def dickpic(ctx):
    if random.randrange(0, 100) > 50:
        pic = NAGOSHIPIC1
    else:
        pic = NAGOSHIPIC2
    await ctx.message.channel.send(f"I showed you my dick please respond\n{pic}")

@commands.command(checks=[in_channel], brief="Accesses reARMP tool", help=HELP['armp'])
async def armp(ctx):
    def sender(msg):
        return msg.author == ctx.message.author
    
    sysout = sys.stdout
    result = StringIO()
    sys.stdout = result
    
    if not len(ctx.message.attachments):
        await ctx.send("No files were attached to the message. Aborting.")
        return
            
    
    async with ctx.typing():
        files = []
        attachments = ctx.message.attachments
        await ctx.send(content="Converting...")
        try:
            for file in attachments:
                name, ext = split_ext(file.filename)
                
                if ext == 'bin':
                    name += '.json'
                    new_file = dumps(reARMP.exportFile(await file.read()), indent=2, ensure_ascii=False).encode()
                else:
                    name += '.bin'
                    new_file = reARMP.rebuildFile(loads(await file.read()))
                
                if len(new_file) > 8_388_119:
                    data = BytesIO()
                    z = zipfile.ZipFile(file=data, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION)
                    z.writestr(zinfo_or_arcname=name, data=new_file)
                    z.close()
                    new_file = BytesIO(data.getvalue())
                    name += '.zip'
                if type(new_file) is not BytesIO:
                    new_file = BytesIO(new_file)
                files.append(File(new_file, filename=name))
                
        except Exception as err:
            print(err)
            await ctx.send(content="Oopsie woopsie. Something went wrong. Post log?")
            msg = await ctx.bot.wait_for('message', check=sender, timeout=10.0)
            if 'y' in msg.content:
                await ctx.send(file=File(BytesIO(result.getvalue().encode()), filename='log.txt'))
            return
        
        if check_size(files) > 8_388_119:
            await ctx.send(content="Your files are too powerful. (heh)")
            await ctx.send(content="Bot's maximum upload limit is 8MB. Try uploading less files next time. Aborting.")
            return
        await ctx.send(content="Done!", file=files[0])
    sys.stdout = sysout

@commands.command(checks=[in_channel], brief="Accesses the GMT converter tool", help=HELP['gmt'])
async def gmt(ctx):
    def sender(msg):
        return msg.author == ctx.message.author
    
    def sender_has_files(msg):
        return msg.author == ctx.message.author and len(msg.attachments) > 0
    
    if not len(ctx.message.attachments):
        content = [a.lstrip(' -') for a in ctx.message.content.lower().split(' ')]
        ok = False
        for m in ['h', 'help', 'd', 'dir']:
            if m in content:
                ok = True
                break
        if not ok:
            await ctx.send("No files were attached to the message. Aborting.")
            return
    
    sysout = sys.stdout
    result = StringIO()
    #sys.stdout = result
    with ctx.typing():
        args = ctx.message.content.lower().split(' ')
        args = [COMMAND_TO_CMD.get(a.lstrip(' -'), a.lstrip(' -')) for a in args]
        if 'h' in args or 'help' in args:
            await ctx.send(content=GMT_HELP)
            return
        
        if not 'ig' in args:
            if 'i' in args:
                args[args.index('i')] = 'ig'
            else:
                await ctx.send(content="Provide input game with \'-ig\'. Aborting.")
                return
        
        if not 'og' in args:
            if 'o' in args:
                args[args.index('o')] = 'og'
            else:
                await ctx.send(content="Provide output game with \'-og\'. Aborting.")
                return
        
        zipmode = False
        if 'z' in args:
            zipmode = True
        
        attachments = []
        if 'd' in args:
            await ctx.message.add_reaction(EMOTES['KiryuThumb'])
            await ctx.send(content="Start attaching GMT files. Type `stop` or `s` when done.")
            
            while True:
                try:
                    msg = await ctx.bot.wait_for('message', check=sender, timeout=20.0)
                    if len(msg.attachments):
                        await msg.add_reaction(EMOTES['KiryuThumb'])
                        attachments.extend(msg.attachments)
                    con = msg.content.split(' ')
                    if 's' in con or 'stop' in con:
                        break
                except Exception as err:
                    await ctx.send(content="Request timed out.")
                    break
            await ctx.send(content="Stopped recieving GMTs.")
        
        outgame = ""
        args = args[1:]
        for i in range(len(args)):
            if i >= len(args):
                break
            if args[i] == 'og':
                outgame = args[i + 1]
            if args[i] in ['d', 'dr', 'cmb', 'rhct', 'sf', 'z']:
                args.remove(args[i])
                i -= 1
            elif args[i] in ['sgmd', 'tgmd', 'aoff']:
                args.remove(args[i])
                args.remove(args[i])
                i -= 1
            i += 1
        
        sgmd, tgmd = None, None
        if 'rp' in args or 'fc' in args or 'hn' in args or 'bd' in args:
            await ctx.send(content="Attach **source** GMD.")
            msg_s = await ctx.bot.wait_for('message', check=sender_has_files, timeout=30.0)
            sgmd = await msg_s.attachments[0].read()
            
            await ctx.send(content="Attach **target** GMD.")
            msg_t = await ctx.bot.wait_for('message', check=sender_has_files, timeout=30.0)
            tgmd = await msg_t.attachments[0].read()
        
        args = list(map(lambda a: f"-{a}" if a in GMT_CMD else a, args))
        args.append('-i')
        args.append('\"\"')
        
        await ctx.send(content="Converting...")
        
        files = []
        attachments.extend(ctx.message.attachments)
        
        try:
            for file in attachments:
                data = [] # tuples of (name, file)
                name, ext = split_ext(file.filename)
                if ext not in ['gmt', 'cmt']:
                    if ext == 'zip':
                        z = zipfile.ZipFile(BytesIO(await file.read()), mode='r')
                        for n in z.namelist():
                            if n[-3:] in ['gmt', 'cmt']:
                                data.append((n, z.read(n)))
                    else:
                        continue
                else:
                    data.append((name, await file.read()))
                for d in data:
                    new_name = f"{d[0]}-{outgame}.gmt"
                    new_file = BytesIO(convert_from_buffer(args, d[1], sgmd, tgmd))
                    files.append(File(new_file, filename=new_name))
        except Exception as err:
            print(err)
            await ctx.send(content="Oopsie woopsie. Something went wrong. Post log?")
            msg = await ctx.bot.wait_for('message', check=sender, timeout=10.0)
            if 'y' in msg.content:
                await ctx.send(file=File(BytesIO(result.getvalue().encode()), filename='log.txt'))
            return
        
        if not len(files):
            await ctx.send(content="No files got converted. Aborting.")
            return
        
        i = 1
        if zipmode:
            data = BytesIO()
            z = zipfile.ZipFile(file=data, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION)
            z.writestr(zinfo_or_arcname=files[0].filename, data=files[0].fp.getvalue())
            sub_files = [(z, data)]
            size_z = check_size([files[0]])
            while i < len(files):
                file = files[i]
                name = file.filename
                size = check_size([file])
                if size_z + size > 8_388_119:
                    size_z = 0
                    data = BytesIO()
                    sub_files.append((zipfile.ZipFile(file=data, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION), data))
                sub_files[-1][0].writestr(zinfo_or_arcname=name, data=file.fp.getvalue())
                size_z += size
                if len(sub_files[-1][1].getvalue()) > 8_388_119:
                    await ctx.send(content=f"Failed on uploading \"{name}\"")
                    await ctx.send(content="Your files are too powerful. (heh)")
                    await ctx.send(content="Bot's maximum upload limit is 8MB. Try uploading less files next time. Aborting.")
                    return
                i += 1
            numbers = iter(range(len(sub_files)))
            sub_files = [[File(BytesIO(d[1].getvalue()), filename=f"converted-{next(numbers)}.zip")] for d in sub_files]
        else:
            sub_files = [[files[0]]]
            while i < len(files):
                file = files[i]
                name = file.filename
                size = check_size([file])
                
                if size > 8_388_119:
                    data = BytesIO()
                    z = zipfile.ZipFile(file=data, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION)
                    z.writestr(zinfo_or_arcname=name, data=file.fp.getvalue())
                    z.close()
                    new_file = BytesIO(data.getvalue())
                    size = len(new_file.getvalue())
                    if size > 8_388_119:
                        await ctx.send(content=f"Failed on uploading \"{name}\"")
                        await ctx.send(content="Your files are too powerful. (heh)")
                        await ctx.send(content="Bot's maximum upload limit is 8MB. Try uploading less files next time. Aborting.")
                        return
                    name += '.zip'
                    file = File(new_file, filename=name)
                
                if check_size(sub_files[-1]) + size > 8_388_119 or len(sub_files[-1]) == 10:
                    sub_files.append([])
                sub_files[-1].append(file)
                i += 1
        
        count = len(sub_files)
        for i in range(count):
            await ctx.send(content=f"Sending... ({i+1}/{count})", files=sub_files[i])
        
        await ctx.send(content="Done!")
    
    #result_string = result.getvalue()
    #print(result_string)
    sys.stdout = sysout

FUNCTIONS = [bin, armp, gmt, pruebala, dickpic, ichireal, based, stare]