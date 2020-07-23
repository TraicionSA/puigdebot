import discord
import asyncio
import random
from random import randint
import time
import json
import os
import psycopg2
from psycopg2.extensions import AsIs
import requests
import mimetypes
import datetime
from time import sleep

# INFORMATION:
# SERVER.ID: '188966409672458241'
# SERVER.NAME: 'VANDALPC'

client = discord.Client()
global bot_status
bot_status = False
bot_analisis = False


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    game = discord.Game("comiendo pipas")
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.event
async def on_reaction_add(reaction, user):
    #REACCION QUOTE
    if reaction.emoji == '📌':
     nomServ = reaction.message.server
     nomChan = reaction.message.channel
     chan = discord.utils.get(client.get_all_channels(), server__name=str(nomServ), name=str(nomChan))
    
     me = reaction.message.content
     fecha = '{:%Y-%m-%d %H:%M:%S}'.format(reaction.message.timestamp)
     tim = user.name + ' Te ha citado el mensaje con fecha ' + str(fecha)
     em = discord.Embed(description=me, color=0xff0000)
     em.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_url)
     em.set_footer(text=str(tim))
     
     #await client.send_message(chan, embed=em)
     await messageChannel.send(chan, embed=em)
     mensa = reaction.message.author.mention
     #await client.send_message(chan, mensa)
     await messageChannel.send(chan, mensa)
     

@client.event
async def on_message(message):
    messageAuthor = message.author
    messageChannel = message.channel
    # messageTimestamp = message.timestamp

    #MOSTRAR GIF CON REACCION
    if message.content.startswith('.g1f') or message.content.startswith('.t4g'):
     args = message.content.split(" ")
     del args[0]
     buscar = '%\' and tag like \'%'.join(args)
     cantidad = canti(buscar)
     if cantidad == 0:
      #await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF QUE BUSCAS:octagonal_sign:')
      await messageChannel.send(':octagonal_sign:NO ENCUENTRA EL GIF QUE BUSCAS:octagonal_sign:')
     else:
      ran = randint(0,cantidad-1)
      #em = discord.Embed(title='Gif', url=infoUrl(buscar,0), description=infoTag(buscar,0), color=0xff0000)
      #em.set_image(url=infoUrl(buscar,0))
      if infoUrl(buscar,ran) or infoTag(buscar,ran):
       posiArray = ran
       strinPosiArray = posiArray + 1
       stri =  infoUrl(buscar,posiArray) + ' \n**' + str(messageAuthor) + ' buscó: ' + infoTag(buscar,posiArray) + '** __' +str(strinPosiArray) + '/' + str(cantidad) + '__'
       #msg = await client.send_message(message.channel, str(stri))
       msg = await messageChannel.send(str(stri))
       await client.add_reaction(msg, '👈')
       await client.add_reaction(msg, '👉')
       await client.add_reaction(msg, '🔴')
       await client.add_reaction(msg, '🗑')
       await client.delete_message(message)
       while True:
           def check(reaction, user):
              if reaction.count != 1 and reaction.emoji == '👉' and messageAuthor == user:
                  return 1
              if reaction.count != 1 and reaction.emoji == '👈' and messageAuthor == user:
                  return 1
              if reaction.count != 1 and reaction.emoji == '🔴' and messageAuthor == user:
                  return 1
              if reaction.count != 1 and reaction.emoji == '🗑' and messageAuthor == user:
                  return 1
              return 0
           #res = await client.wait_for_reaction(message=msg, timeout=20, check=check)
           res = await client.wait_for('reaction_add', message=msg, timeout=20, check=check)
           
           #REACCION SIN REACCION
           if res is None:
            await client.clear_reactions(msg)
           else:
               #REACCION 👉
               if '{0.reaction.emoji}'.format(res) == '👉':
                #em2 = discord.Embed(title='Gif', url=infoUrl(buscar,ran), description=infoTag(buscar,ran), color=0xff0000)
                #em2.set_image(url=infoUrl(buscar,ran))
                #await client.edit_message(msg, embed=em2)
                posiArray = posiArray + 1
                if posiArray == cantidad:
                 posiArray = 0
                strinPosiArray = posiArray + 1
                stri = infoUrl(buscar,posiArray) + ' \n**' + str(messageAuthor) + ' buscó: ' + infoTag(buscar,posiArray) + '** __' + str(strinPosiArray) + '/' + str(cantidad) + '__'
                await client.edit_message(msg, str(stri))
                await client.clear_reactions(msg)
                await client.add_reaction(msg, '👈')
                await client.add_reaction(msg, '👉')
                await client.add_reaction(msg, '🔴')
                await client.add_reaction(msg, '🗑')

                 
               #REACCION 👈
               if '{0.reaction.emoji}'.format(res) == '👈':
                posiArray = posiArray - 1
                if posiArray == -1:
                 posiArray = cantidad - 1
                strinPosiArray = posiArray + 1
                stri = infoUrl(buscar,posiArray) + ' \n**' + str(messageAuthor) + ' buscó: ' + infoTag(buscar,posiArray) + '** __' + str(strinPosiArray) + '/' + str(cantidad) + '__'
                await client.edit_message(msg, str(stri))
                await client.clear_reactions(msg)
                await client.add_reaction(msg, '👈')
                await client.add_reaction(msg, '👉')
                await client.add_reaction(msg, '🔴')
                await client.add_reaction(msg, '🗑')
               
               #REACCION 🔴
               if '{0.reaction.emoji}'.format(res) == '🔴':
                await client.clear_reactions(msg)
                break
                
               #REACCION 🗑
               if '{0.reaction.emoji}'.format(res) == '🗑':
                await client.clear_reactions(msg)
                await client.delete_message(msg)
                break

       #fin While     
      else:
       await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF QUE BUSCAS:octagonal_sign:')
    
    #METER GIF
    if message.content.startswith('.creategif') or message.content.startswith('.createtag'):
     args = message.content.split(" ")
     del args[0]
     url = args[0]
     del args[0]
     tags = ' '.join(args)
     compo = comprobarUrl(url)
     if compo != None:
      await client.send_message(message.channel, ':octagonal_sign:ESTE GIF YA ESTA EN LA BASE DE DATOS:octagonal_sign:')
     else:
      meter(url,tags)
      mes = str(messageAuthor) + ' ha introducido el gif ' + str(url) + ' con los tags ' + str(tags)
      chann = discord.utils.get(client.get_all_channels(), name='admins')
      await client.send_message(chann, str(mes))
      sleep(5)
      await client.delete_message(message)
    #ACTUALIZAR TAG GIF 
    if message.content.startswith('.updategif') or message.content.startswith('.updatetag'):
     if(message.author.id == '125931468940771328'):
         args = message.content.split(" ")
         del args[0]
         url = args[0]
         del args[0]
         tags = ' '.join(args)
         compo = comprobarUrl(url)
         if compo != None:
          ran = randint(1000,9999)
          await client.send_message(message.channel, '```ESCRIBE ESTE NUMERO PARA ACEPTAR EL UPDATE: '+ str(ran) + '```')
          nume = str(ran)
          if await client.wait_for_message(author=message.author, content=nume):
           actualizar(url,tags)
           mes = str(messageAuthor) + ' ha actualizado el gif ' + str(url) + ' con los tags ' + str(tags)
           chann = discord.utils.get(client.get_all_channels(), name='admins')
           await client.send_message(chann, str(mes))
           sleep(5)
           await client.delete_message(message)
         else:
          await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF EN LA BASE DATOS:octagonal_sign:')
     else:
      await client.send_message(message.channel, ':octagonal_sign:NO TIENES PERMISOS PARA ACTUALIZAR EL GIF:octagonal_sign:')
      
    #COMPROBAR SI EXISTE GIF EN BD
    if message.content.startswith('.comprobargif') or message.content.startswith('.comprobartag'):
     args = message.content.split(" ")
     del args[0]
     url = args[0]
     tags = sacarTag(url)
     compo = comprobarUrl(url)
     if compo != None:
      await client.send_message(message.channel, ':exclamation::exclamation: YA EXISTE EN LA BASE DE DATOS CON ESTOS TAGS: ' + str(tags) + ' :exclamation::exclamation: ')
     else:
      await client.send_message(message.channel, ':grey_exclamation: NO SE ENCUENTRA EL GIF EN LA BASE DATOS :grey_exclamation:')
    
    
    #BORRAR GIF
    if message.content.startswith('.deletegif') or message.content.startswith('.deletetag'):
     if(message.author.id == '125931468940771328'):
         args = message.content.split(" ")
         del args[0]
         url = args[0]
         compo = comprobarUrl(url)
         if compo != None:
          ran = randint(1000,9999)
          await client.send_message(message.channel, '```ESCRIBE ESTE NUMERO PARA CONFIRMAR EL BORRADO: '+ str(ran) + '```')
          nume = str(ran)
          if await client.wait_for_message(author=message.author, content=nume):
           delete(url)
           tags = sacarTag(url)
           mes = str(messageAuthor) + ' ha borrado el gif ' + str(url) + ' con los tags ' + str(tags)
           chann = discord.utils.get(client.get_all_channels(), name='admins')
           await client.send_message(chann, str(mes))
           sleep(5)
           await client.delete_message(message)
         else:
          await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF EN LA BASE DATOS:octagonal_sign:')
     else:
      await client.send_message(message.channel, ':octagonal_sign:NO TIENES PERMISO PARA BORRAR GIF:octagonal_sign:')
      
    #AYUDA  
    if message.content.startswith('.help'):
     help = discord.Embed(title='AYUDA', url='http://lavozpopular.com/wp-content/uploads/2014/09/Muere-Emilio-Bot%C3%ADn.jpg', description='Botin', color=0xff0000)
     help.set_image(url='http://lavozpopular.com/wp-content/uploads/2014/09/Muere-Emilio-Bot%C3%ADn.jpg')
     help.add_field(name='Mostrar Gif', value='.gif tags', inline=True)
     help.add_field(name='Ejemplo Mostrar Gif', value='.gif motos marquez', inline=True)
     help.add_field(name='Guardar Gif', value='.creategif url tags', inline=True)
     help.add_field(name='Ejemplo Guardar Gif', value='.creategif http://wwww.susto.com/imagen.gif susto', inline=True)
     help.add_field(name='Editar tags de Gif', value='.updategif url tags', inline=True)
     help.add_field(name='Ejemplo Editar tags de Gif', value='.updategif http://wwww.susto.com/imagen.gif susto discord', inline=True)
     help.add_field(name='Comprobar si existe Gif', value='.comprobargif url', inline=True)
     help.add_field(name='Ejemplo Comprobar Gif', value='.comprobargif http://wwww.susto.com/imagen.gif', inline=True)
     help.add_field(name='Citar comentario', value='usar emoji 📌', inline=True)
     #channel = message.channel
     await messageChannel.send(embed=help)

    #STATUS BOT 
    if message.content.startswith('.status'):
        args = message.content.split(" ")
        del args[0]
        estado = ' '.join(args)
        #await client.change_presence(game=discord.Game(name=jugando))
        estadoTexto = discord.Activity(estado)
        #await client.change_presence(status=discord.Status.idle, activity=game)
        await client.change_presence(status=discord.Status.online, activity=estadoTexto)
        
    #GAMING BOT 
    if message.content.startswith('.jugando_a'):
        args = message.content.split(" ")
        del args[0]
        jugando = ' '.join(args)
        #await client.change_presence(game=discord.Game(name=jugando))
        game = discord.Game(jugando)
        await client.change_presence(status=discord.Status.idle, activity=game)

     
#SACA URL AL BUSCAR POR TAGS            
def infoUrl(buscar,num):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     trozo1 = "SELECT url FROM giftable where tag like '%"
     trozo2 = buscar
     trozo3 = "%';"
     consulta =  trozo1+trozo2+trozo3
     cur.execute("""%s""", (AsIs(consulta),))
     rows = cur.fetchall()
     resultado = rows[num][0]
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            

#SACA TAGS DEL GIF BUSCANDO POR TAGS            
def infoTag(buscar,num):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     trozo1 = "SELECT tag FROM giftable where tag like '%"
     trozo2 = buscar
     trozo3 = "%';"
     consulta =  trozo1+trozo2+trozo3
     cur.execute("""%s""", (AsIs(consulta),))
     rows = cur.fetchall()
     resultado = rows[num][0]
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            

#COMPRUEBA SI ENCUENTRA LA URL A RAIZ DE UNA URL            
def comprobarUrl(url):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""SELECT url FROM giftable where url = \'%s\'""", (AsIs(url),))
     rows = cur.fetchall()
     resultado = rows[0][0]
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
#SACA TAG A RAIZ DE URL            
def sacarTag(url):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""SELECT tag FROM giftable where url = \'%s\'""", (AsIs(url),))
     rows = cur.fetchall()
     resultado = rows[0][0]
     return resultado
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            

#ACTUALIZA TAGS DE GIF
def actualizar(url, tags):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""UPDATE giftable SET tag =\'%s\' where url = \'%s\';""", (AsIs(tags),AsIs(url),))
     conn.commit()
     return True
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()    
            
#BORRA GIF BD          
def delete(url):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""DELETE from giftable where url = \'%s\';""", (AsIs(url),))
     conn.commit()
     return True
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  
            
#METE URL Y TAGS EN BD            
def meter(url, tags):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     cur.execute("""INSERT INTO giftable (url, tag) VALUES (\'%s\', \'%s\');""", (AsIs(url),AsIs(tags),))
     conn.commit()
     return True
     
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  


#SACA LA CANTIDAD DE GIFS CON ESOS TAGS   
def canti(buscar):
    #BD 
    try:
     DATABASE_URL = os.environ['DATABASE_URL']
     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     cur=conn.cursor()
     trozo1 = "SELECT url FROM giftable where tag like '%"
     trozo2 = buscar
     trozo3 = "%';"
     consulta =  trozo1+trozo2+trozo3
     cur.execute("""%s""", (AsIs(consulta),))
     rows = cur.fetchall()
     resultado = len(rows)
     return resultado
     cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#RUN
client.run(os.environ.get('BOT_TOKEN'))
