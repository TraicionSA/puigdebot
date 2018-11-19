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
    await client.change_presence(game=discord.Game(name='susto.exe'))

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
     
     await client.send_message(chan, embed=em)
     mensa = reaction.message.author.mention
     await client.send_message(chan, mensa)
     

@client.event
async def on_message(message):
    if message.content.startswith('.gif') or message.content.startswith('.tag'):
      await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF QUE BUSCAS:octagonal_sign:')

     
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
    #try:
     #DATABASE_URL = os.environ['DATABASE_URL']
     #conn = psycopg2.connect(DATABASE_URL, sslmode='require')
     #cur=conn.cursor()
     #trozo1 = "SELECT url FROM giftable where tag like '%"
     #trozo2 = buscar
     #trozo3 = "%';"
     #consulta =  trozo1+trozo2+trozo3
     #cur.execute("""%s""", (AsIs(consulta),))
     #rows = cur.fetchall()
     #resultado = len(rows)
     #return resultado
     #cur.close()
    e#xcept (Exception, psycopg2.DatabaseError) as error:
        #print(error)
        #return 0
    #finally:
        #if conn is not None:
            #conn.close()
    return 0

#RUN
client.run(os.environ.get('BOT_TOKEN'))
