from telethon import TelegramClient, events, sync,Button
from telethon.events import NewMessage

from utils import createID,get_file_size,sizeof_fmt
from threads import ThreadAsync,Thread
from worker import async_worker

import asyncio
import base64
import zipfile
import os
import requests
import re
import config
import repouploader
import zipfile
import time
import animate

from repouploader import RepoUploader,RepoUploaderResult
from pydownloader.downloader import Downloader
import shorturl
import xdlink

tl_admin_users = ['reymichel2009','george0x0','Jorgevv','Penelopeplp'] #Poner aqui los user con acceso permanente
godlist = ['reymichel2009','george0x0','Jorgevv','Penelopeplp'] #Poner aqui los admin 

async def get_root(username):
    if os.path.isdir(config.ROOT_PATH+username)==False:
        os.mkdir(config.ROOT_PATH+username)
    return os.listdir(config.ROOT_PATH+username)

async def send_root(bot,ev,username):
    listdir = await get_root(username)
    reply = f'📄 {username}/ ({len(listdir)} 𝖆𝖗𝖈𝖍𝖎𝖛𝖔𝖘) 📄\n\n'
    i=-1
    for item in listdir:
        i+=1
        fname = item
        fsize = get_file_size(config.ROOT_PATH + username + '/' + item)
        prettyfsize = sizeof_fmt(fsize)
        reply += str(i) + ' - ' + fname + ' [' + prettyfsize + ']\n'
    await bot.send_message(ev.chat.id,reply)

def text_progres(index, max):
            try:
                if max < 1:
                    max += 1
                porcent = index / max
                porcent *= 100
                porcent = round(porcent)
                make_text = ''
                index_make = 1
                make_text += '\n'
                while (index_make < 21):
                    if porcent >= index_make * 5:
                        make_text += '█'
                    else:
                        make_text += '░'
                    index_make += 1
                make_text += ''
                return make_text
            except Exception as ex:
                return ''

def porcent(index, max):
    porcent = index / max
    porcent *= 100
    porcent = round(porcent)
    return porcent

async def download_progress(dl, filename, currentBits, totalBits, speed, totaltime, args):
    try:
        bot = args[0]
        ev = args[1]
        message = args[2]

        if True:
            msg = '⚜️ Descargando Archivo....\n'
            msg += '🗃 Archivo: ' + filename + ''
            msg += '\n' + text_progres(currentBits, totalBits) + ' ' + str(porcent(currentBits, totalBits)) + '%\n' + '\n'
            msg += '🗂 Tamaño Total: ' + sizeof_fmt(totalBits) + '\n'
            msg += '📦 Descargado: ' + sizeof_fmt(currentBits) + '\n'
            msg += '🚀 Velocidad: ' + sizeof_fmt(speed) + '/s\n'
            msg += '⏱ Tiempo de descarga: ' + str(time.strftime('%H:%M:%S', time.gmtime(totaltime))) + 's\n\n'
            await bot.edit_message(ev.chat,message,text=msg)

    except Exception as ex:
        print(str(ex))


STORE_UPLOADER = {}
STORE_RESULT = {}
def upload_progress(filename, currentBits, totalBits, speed, totaltime, args):
    try:
        bot = args[0]
        ev = args[1]
        message = args[2]
        loop = args[3]

        if True:
            msg = '⚜️ 𝕾𝖚𝖇𝖎𝖊𝖓𝖉𝖔 𝖆𝖗𝖈𝖍𝖎𝖛𝖔....\n'
            msg += '🗃 𝕬𝖗𝖈𝖍𝖎𝖛𝖔: ' + filename + ''
            msg += '\n' + text_progres(currentBits, totalBits) + ' ' + str(porcent(currentBits, totalBits)) + '%\n' + '\n'
            msg += '🗂 Tamaño Total: ' + sizeof_fmt(totalBits) + '\n'
            msg += '📤 Subido: ' + sizeof_fmt(currentBits) + '\n'
            msg += '🚀 Velocidad: ' + sizeof_fmt(speed) + '/s\n'
            msg += '⏱ Tiempo de descarga: ' + str(time.strftime('%H:%M:%S', time.gmtime(totaltime))) + 's\n\n'
            STORE_UPLOADER[filename] = msg
    
    except Exception as ex:
        print(str(ex))

async def compress(bot,ev,text,message,username):
        await  bot.edit_message(ev.chat,message,'📚Comprimiendo✂️...')
        text = str(text).replace('/rar ','')
        index = 0
        range = 0
        sizemb = 1900
        try:
            cmdtokens = str(text).split(' ')
            if len(cmdtokens)>0:
                index = int(cmdtokens[0])
            range = index+1
            if len(cmdtokens)>1:
                range = int(cmdtokens[1])+1
            if len(cmdtokens)>2:
                sizemb = int(cmdtokens[2])
        except:
            pass
        if index != None:
            listdir = await get_root(username)
            zipsplit = listdir[index].split('.')
            zipname = ''
            i=0
            for item in zipsplit:
                    if i>=len(zipsplit)-1:continue
                    zipname += item
                    i+=1
            totalzipsize=0
            iindex = index
            while iindex<range:
                ffullpath = config.ROOT_PATH + username + '/' + listdir[index]
                totalzipsize+=get_file_size(ffullpath)
                iindex+=1
            zipname = config.ROOT_PATH + username + '/' + zipname
            multifile = zipfile.MultiFile(zipname,config.SPLIT_FILE)
            zip = zipfile.ZipFile(multifile, mode='w')
            while index<range:
                ffullpath = config.ROOT_PATH + username + '/' + listdir[index]
                await bot.edit_message(ev.chat,message,text=f'📚 {listdir[index]} 📚...')
                filezise = get_file_size(ffullpath)
                zip.write(ffullpath)
                index+=1
            zip.close()
            multifile.close()
            return multifile.files

async def onmessage(bot:TelegramClient,ev: NewMessage.Event,loop,ret=False):

    if ret:return

    proxies = None
    if config.PROXY:
        proxies = config.PROXY.as_dict_proxy()

    username = ev.message.chat.username
    text = ev.message.text

    #if username not in config.ACCES_USERS:
    if username not in tl_admin_users:
        await bot.send_message(ev.chat.id,'🛑🆃🅴 🅵🅰🅻🆃🅰 🅲🅰🅻🅻🅴🛑')
        return

    if not os.path.isdir(config.ROOT_PATH + username):
        os.mkdir(config.ROOT_PATH + username)

    try:
        if ev.message.file:
            message = await bot.send_message(ev.chat.id,'⚙️Procesando Archivo...📝')
            filename = ev.message.file.id + ev.message.file.ext
            if ev.message.file.name:
                filename = ev.message.file.name
            filesave = open(config.ROOT_PATH + username + '/' + filename,'wb')
            chunk_por = 0
            chunkrandom = 100
            total = ev.message.file.size
            time_start = time.time()
            time_total = 0
            size_per_second = 0
            clock_start = time.time()
            async for chunk in bot.iter_download(ev.message,request_size = 1024):
                chunk_por += len(chunk)
                size_per_second+=len(chunk)
                tcurrent = time.time() - time_start
                time_total += tcurrent
                time_start = time.time()
                if time_total>=1:
                   clock_time = (total - chunk_por) / (size_per_second)
                   await download_progress(None,filename,chunk_por,total,size_per_second,clock_time,(bot,ev,message))
                   time_total = 0
                   size_per_second = 0
                filesave.write(chunk)
                pass
            filesave.close()
            await bot.delete_messages(ev.chat,message)
            await send_root(bot,ev,username)
            return
            pass
    except Exception as ex:
        pass

    if '/start' in text:
        reply = '⚜️Uploader-Channel⚜️\nEs un bot para descargas y subidas gratis para el canal King Media\n\n'
        reply += '<a href="https://github.com/reymichel2009">Rey Michel Github</a>\n'
        reply += '<a href="𝖍𝖙𝖙𝖕𝖘://𝖙.𝖒𝖊/reymichel2009">Rey Michel Telegram</a>'
        message = await bot.send_message(ev.chat.id,reply,parse_mode='html')
        pass
    if '/add' in text and username in godlist:
        usernameadd = text.split(' ')[1]
        tl_admin_users.append(usernameadd)
        print(tl_admin_users)
    
    if '/ban' in text and username in godlist:
        usernamedell = text.split(' ')[1]
        tl_admin_users.remove(usernamedell)
        print(tl_admin_users)
    
    if '/Tutorial' in text:
        reply = '⚜️Tutorial⚜️\n𝕰𝖘 𝖚𝖓 𝖇𝖔𝖙 𝖕𝖆𝖗𝖆 𝖊𝖑 𝖒𝖆𝖓𝖊𝖏𝖔 𝖉𝖊 𝖆𝖗𝖈𝖍𝖎𝖛𝖔𝖘 𝖊𝖓 𝖙𝖊𝖑𝖊𝖌𝖆𝖒 (𝖉𝖊𝖘𝖈𝖆𝖗𝖌𝖆𝖘/𝖘𝖚𝖇𝖎𝖉𝖆𝖘)\n\n'
        
        reply += '<a href=" Cuando descarguen todo Tinen q hacer lo siguiente BUSCAN LA CARPETA DONDE SE DESCARGARON LAS COSAS Y AL FINAL DE CADA ARCHIVO BAN A VER Q DISE : "> Ejemplo : ElHombrDToronto2022cssr16.parte1__.rar </a>\n'
        reply += '<a href="TINEN Q CAMBIAR ESO Q DICE "> * parte2__.rar *   POR   * 7z.001 * </a>'
        reply += '<a href=" Ejemplo: "> , </a>'
        reply += '<a href=" ElHombrDToronto2022cssr16.7z.001 "> , </a>'
        reply += '<a href=" ElHombrDToronto2022cssr16.7z.002 "> , </a>'
        reply += '<a href=" ElHombrDToronto2022cssr16.7z.003 "> , </a>'
        reply += '<a href=" Eso seria todo : "> ya deveria descomprimir sin problemas </a>'
        message = await bot.send_message(ev.chat.id,reply,parse_mode='html')
        pass
    
    
    if 'http' in text:
        message = await bot.send_message(ev.chat.id,'⏳Procesando Enlace...🔗')
        dl = Downloader(config.ROOT_PATH + username + '/')
        file = await dl.download_url(text,progressfunc=download_progress,args=(bot,ev,message),proxies=proxies)
        if file:
            if file!='':
                await bot.delete_messages(ev.chat,message)
                await send_root(bot,ev,username)
            else:
                await bot.edit_message(ev.chat,message,text='✅El Enlace es Funcional🔗')
        else:
             await bot.edit_message(ev.chat,message,text='💢El Enlace es Erroneo🔗')
        return

    if '/ls' in text:
        await send_root(bot,ev,username)
        return

    if '/rm' in text:
        message = await bot.send_message(ev.chat.id,'🗑Borrando...')
        text = str(text).replace('/rm ','')
        index = 0
        range = 1
        try:
            cmdtokens = str(text).split(' ')
            if len(cmdtokens)>0:
                index = int(cmdtokens[0])
            range = index+1
            if len(cmdtokens)>1:
                range = int(cmdtokens[1])+1
        except:
            pass
        listdir = await get_root(username)
        while index < range:
              rmfile = config.ROOT_PATH + username + '/' + listdir[index]
              await bot.edit_message(ev.chat,message,text=f'🗑 {listdir[index]} 🗑...')
              os.unlink(rmfile)
              index += 1
        await bot.delete_messages(ev.chat,message)
        message = await bot.send.message(ev.chat.id,'Se ha eliminado satisfactoriamente')
        await send_root(bot,ev,username)
        return

    if '/rar' in text:
        message = await bot.send_message(ev.chat.id,'🛠𝕻𝖗𝖔𝖈𝖊𝖘𝖆𝖓𝖉𝖔...')
        await compress(bot,ev,text,message,username)

    if '/up' in text:
        text = str(text).replace('/up ','')
        index = 0
        range = index+1
        txtname = ''
        try:
            cmdtokens = str(text).split(' ')
            if len(cmdtokens)>0:
                index = int(cmdtokens[0])
            range = index+1
            if len(cmdtokens)>1:
                range = int(cmdtokens[1])+1
            if len(cmdtokens)>2:
                txtname = cmdtokens[2]
        except:
            pass
        message = await bot.send_message(ev.chat.id,'🛠𝕻𝖗𝖔𝖈𝖊𝖘𝖆𝖓𝖉𝖔...')
        listdir = await compress(bot,ev,text,message,username)
        try:
            await bot.edit_message(ev.chat,message,text=f'🖥Creando Cuenta...')
            session:RepoUploader = await repouploader.create_session(config.PROXY)
            resultlist = []
            txtsendname = str(listdir[0]).split('/')[-1].split('.')[0].split('_')[0] + '.txt'
            for fi in listdir:
                  ffullpath = fi
                  ffname = str(fi).split('/')[-1]
                  fsize = get_file_size(ffullpath)
                  if fsize>config.SPLIT_FILE:
                      await bot.edit_message(ev.chat,message,text=f'{ffname} El Archivo Es Demasiado Grande, Debe Comprimir\nSe Cancelo la subida')
                      return
                  await bot.edit_message(ev.chat,message,text=f'📤Subiendo {ffname}...')
                  result:RepoUploaderResult = None
                  def uploader_func():
                      result = session.upload_file(ffullpath,progress_func=upload_progress,progress_args=(bot,ev,message,loop))
                      STORE_UPLOADER[ffname] = None
                      if result:
                        STORE_RESULT[ffname] = result
                  tup = Thread(uploader_func)
                  tup.start()
                  try:
                      while True:
                          try:
                              msg = STORE_UPLOADER[ffname]
                              if msg is None:break
                              await bot.edit_message(ev.chat,message,msg)
                          except:pass
                          pass
                  except:pass
                  STORE_UPLOADER.pop(ffname)
                  try:
                      resultlist.append(STORE_RESULT[ffname])
                      STORE_RESULT.pop(ffname)
                  except:pass
                  index+=1
            if txtname!='':
                txtsendname = txtname
            txtfile = open(txtsendname,'w')
            urls = []
            for item in resultlist:
                urls.append(item.url)
            await bot.edit_message(ev.chat,message,text=f'🖇Generando XdLinks📝...')
            data = xdlink.parse(urls)
            if data:
                txtfile.write(data)
            else:
                txtfile.write('🅴🆁🆁🅾🆁 🆇🅳🅻🅸🅽🅺 P🅰🆁🆂🅴 🆄🆁🅻🆂')
            txtfile.close()
            await bot.delete_messages(ev.chat,message)
            await bot.send_file(ev.chat,txtsendname,
                                caption=f'{txtsendname}',
                                thumb='thumb.png',
                                buttons=[Button.url('🖥ANDI','https://t.me/Andi9919')])
            for fitem in listdir:
                try:
                    os.unlink(fitem)
                except:pass
            os.unlink(txtsendname)
        except Exception as ex:
             await bot.send_message(ev.chat.id,str(ex))
    pass


def init():
    try:
        bot = TelegramClient(
            'bot', api_id=config.API_ID, api_hash=config.API_HASH).start(bot_token=config.BOT_TOKEN)

        print('Bot is Started!')

        try:
            loopevent = asyncio.get_runing_loop();
        except:
            try:
                loopevent = asyncio.get_event_loop();
            except:
                loopevent = None

        @async_worker
        @bot.on(events.NewMessage()) 
        async def process(ev: events.NewMessage.Event):
           await onmessage(bot,ev,loopevent)
           #await onmessage(bot,ev)
           #loopevent.create_task(onmessage(bot,ev,loopevent))
           #t = ThreadAsync(loop=loopevent,targetfunc=onmessage,args=(loopevent,bot,ev))
           #t.start()


        loopevent.run_forever()
    except Exception as ex:
        init()
        conf.procesing = False

if __name__ == '__main__': 
   init()

#
#
