import os, json, asyncio, sys

from telethon import TelegramClient, events, Button

from telethon.sync import TelegramClient as TMPTelegramClient

from telethon.errors import FloodWaitError, PhoneNumberFloodError, SessionPasswordNeededError, UsersTooMuchError

from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest

from telethon.tl.functions.messages import ImportChatInviteRequest

from telethon.sessions import StringSession

from importlib import import_module

ADMIN = 0#TUO CHAT ID

API_KEY = "TUO API ID"

API_HASH = "TUO API HASH"

STRING_SESSION = ""

Getter = None

Number = None

TempClient = None

Grab = None

inAdding = False

canAdd = True

AddedUsers = []

if os.path.exists("SSs.json"):

	with open("SSs.json", "r+") as f:		SSs = json.load(f)

else:

	SSs = {}

	with open("SSs.json", "w+") as f:

		json.dump(SSs, f)

	

if os.path.exists("ArchSSs.json"):

	with open("ArchSSs.json", "r+") as f:

		ArchSSs = json.load(f)

else:

	ArchSSs = {}

	with open("ArchSSs.json", "w+") as f:

		json.dump(ArchSSs, f)

	

def saveSS():

	global SSs

	with open("SSs.json", "w+") as f:

		json.dump(SSs, f)

	

def saveArchSS():

	global ArchSSs

	with open("ArchSSs.json", "w+") as f:

		json.dump(ArchSSs, f)

	

async def addUsers(client, Users, group):

	global canAdd, AddedUsers

	AddedUsers = []

	for user in Users:

		if canAdd:

			AddedUsers.append(user)

			try:

				await client(InviteToChannelRequest(group, [user]))

				await asyncio.sleep(0.2)

			except:

				pass

		else:

			break

		

	

async def timeoutAdd(timeout):

	global canAdd

	await asyncio.sleep(timeout)

	canAdd = False

bot = TelegramClient("bot", API_KEY, API_HASH)

@bot.on(events.NewMessage(incoming=True))

async def RaspaManager(e):

	global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding, canAdd, AddedUsers

	if e.is_private and e.chat_id == ADMIN:

		if e.text == "/start":

			Getter, Number, TempClient = None, None, None

			await e.respond("**ðŸ¤– Pannello Raspa Bot\n\nâš™ Versione Â» 2.1**", buttons=[[Button.inline("ðŸ“ž Voip", "voip")], [Button.inline("ðŸ‘¥ Ruba", "grab"), Button.inline("âœ” Raspa", "add")]])

		elif Getter != None:

			if Getter == 0:

				Getter = None

				if not e.text in SSs:

					if not e.text in ArchSSs:

						TempClient = TMPTelegramClient(StringSession(), API_KEY, API_HASH)

						await TempClient.connect()

						try:

							await TempClient.send_code_request(phone=e.text, force_sms=False)

							Number = e.text

							Getter = 1

							await e.respond("**ðŸ“© Inserisci Il Codice ðŸ“©**", buttons=[Button.inline("âŒ Annulla", "voip")])

						except PhoneNumberFloodError:

							await e.respond("**âŒ Troppi Tentativi! Prova con un altro numero âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "addvoip")])

						except:

							await e.respond("**âŒ Numero Non Valido âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "addvoip")])

					else:

						await e.respond("**âŒ Voip Archiviato! Riaggiungilo âŒ**", buttons=[[Button.inline("ðŸ“ Voip Archiviati", "arch")], [Button.inline("ðŸ”„ Riprova", "addvoip")]])

				else:

					await e.respond("**âŒ Voip giÃ  aggiunto âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "addvoip")])

			elif Getter == 1:

				try:

					await TempClient.sign_in(phone=Number, code=e.text)

					SSs[Number] = StringSession.save(TempClient.session)

					Getter, Number = None, None

					saveSS()

					await e.respond("**âœ… Voip Aggiunto Correttamente âœ…**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

				except SessionPasswordNeededError:

					Getter = 2

					await e.respond("**ðŸ”‘ Inserisci La Password (2FA) ðŸ”‘**", buttons=[Button.inline("âŒ Annulla", "voip")])

				except:

					Getter, Number = None, None

					await e.respond("**âŒ Codice Errato âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "addvoip")])

			elif Getter == 2:

				try:

					await TempClient.sign_in(phone=Number, password=e.text)

					SSs[Number] = StringSession.save(TempClient.session)

					Getter, Number = None, None

					saveSS()

					await e.respond("**âœ… Voip Aggiunto Correttamente âœ…**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

				except:

					Getter, Number = None, None

					await e.respond("**âŒ Password Errata âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "addvoip")])

			elif Getter == 3:

				Getter = None

				if e.text in SSs:

					await e.respond(f"**ðŸ”§ Gestione Â»** `{e.text}`", buttons=[[Button.inline("ðŸ“ Archivia", "arch;" + e.text), Button.inline("âž– Rimuovi", "del;" + e.text)], [Button.inline("ðŸ”™ Indietro", "voip")]])

				else:

					await e.respond("**âŒ Voip Non Trovato âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "voips")])

			elif Getter == 4:

				Getter = None

				if e.text in ArchSSs:

					await e.respond(f"**ðŸ”§ Gestione Â»** `{e.text}`", buttons=[[Button.inline("âž• Riaggiungi", "add;" + e.text), Button.inline("âž– Rimuovi", "delarch;" + e.text)], [Button.inline("ðŸ”™ Indietro", "voip")]])

				else:

					await e.respond("**âŒ Voip Non Trovato âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "voips")])

			elif Getter == 5:

				Getter == None

				if e.text != None and e.text != "":

					if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):

						if not " " in e.text:

							Grab = e.text

							await e.respond("**âœ… Gruppo Impostato Correttamente âœ…**", buttons=[[Button.inline("âœ” Raspa", "add")], [Button.inline("ðŸ”™ Indietro", "grab")]])

						else:

							await e.respond("**âŒ Al momento puoi inserire un solo gruppo âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "setgrab")])

					else:

						await e.respond("**âŒ Devi inserire un link o una @ di un gruppo âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "setgrab")])

				else:

					await e.respond("**âš ï¸ Formato Non Valido âš ï¸**", buttons=[Button.inline("ðŸ”„ Riprova", "setgrab")])

			elif Getter == 6:

				Getter == None

				if e.text != None and e.text != "":

					if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):

						if not " " in e.text:

							inAdding = True

							canNotify = True

							banned = []

							Users = []

							msg = await e.respond("**âœ… Aggiunta Membri In Corso âœ…**\nATTENDI "+ str(len(SSs) * 120) + " secondi.." , buttons=[Button.inline("âŒ Interrompi", "stop")])

							for SS in SSs:

								isAlive = False

								CClient = TMPTelegramClient(StringSession(SSs[SS]), API_KEY, API_HASH)

								await CClient.connect()

								try:

									me = await CClient.get_me()

									if me == None:

										isAlive = False

									else:

										isAlive = True

								except:

									isAlive = False

								if isAlive:

									async with CClient as client:

										try:

											if "/joinchat/" in Grab:

												if Grab.endswith("/"):

													l = len(Grab) - 2

													Grab = Grab[0:l]

												st = Grab.split("/")

												L = st.__len__() - 1

												group = st[L]

												try:

													await client(ImportChatInviteRequest(group))

												except:

													pass

											else:

												try:

													await client(JoinChannelRequest(Grab))

												except:

													pass

											ent = await client.get_entity(Grab)

											try:

												users = client.iter_participants(ent.id, aggressive=True)

												ent2 = await client.get_entity(e.text)

												users2 = client.iter_participants(ent2.id, aggressive=True)

												Users2 = []

												async for user2 in users2:

													Users2.append(user2.id)

												async for user in users:

													try:

														if not user.bot and not user.id in Users:

															if not user.id in Users2:

																Users.append(user.id)

													except:

														pass

											except:

												await msg.edit("**âŒ Gruppo Non Valido âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "grab")])

												canNotify = False

												break

										except FloodWaitError as err:

											await msg.edit(f"**â³ Attendi altri {err.seconds} prima di riutilizzare il bot â³**", buttons=[Button.inline("ðŸ”™ Indietro", "back")])

											canNotify = False

											break

										except:

											await msg.edit("**âŒ Gruppo Non Trovato âŒ**", buttons=[[Button.inline("â„¹ï¸ PiÃ¹ Info", "info;" + SS)], [Button.inline("ðŸ”„ Riprova", "grab")]])

											canNotify = False

											break

										try:

											if "/joinchat/" in e.text:

												if e.text.endswith("/"):

													l = len(e.text) - 2

													text = e.text[0:l]

												else:

													text = e.text

												st = text.split("/")

												L = st.__len__() - 1

												group2 = st[L]

												try:

													await client(ImportChatInviteRequest(group2))

												except:

													pass

											else:

												try:

													await client(JoinChannelRequest(e.text))

												except:

													pass

											canAdd = True

											await asyncio.gather(addUsers(client, Users, ent2.id), timeoutAdd(120))

											for user in AddedUsers:

												if user in Users:

													Users.remove(user)

										except:

											await msg.edit("**âŒ Gruppo Non Trovato âŒ**", buttons=[[Button.inline("â„¹ï¸ PiÃ¹ Info", "info;" + SS)], [Button.inline("ðŸ”„ Riprova", "add")]])

											canNotify = False

											break

								else:

									banned.append(SS)

									await e.respond(f"**âš ï¸ ATTENZIONE Â»** __Il voip__ `{SS}` __potrebbe essere stato bannato da telegram! Se l' hai solo disconnesso per errore riaggiungilo ;)__")

							if banned.__len__() > 0:

								for n in banned:

									if n in SSs:

										del(SSs[n])

								saveSS()

							inAdding = False

							if canNotify:

								await msg.edit(f"**âœ… Aggiunta Membri Completata âœ…**", buttons=[Button.inline("ðŸ”™ Indietro", "back")])

						else:

							await e.respond("**âŒ Al momento puoi inserire un solo gruppo âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "add")])

					else:

						await e.respond("**âŒ Devi inserire un link o una @ di un gruppo âŒ**", buttons=[Button.inline("ðŸ”„ Riprova", "add")])

				else:

					await e.respond("**âš ï¸ Formato Non Valido âš ï¸**", buttons=[Button.inline("ðŸ”„ Riprova", "add")])

				

			

		

	

@bot.on(events.CallbackQuery())

async def callbackQuery(e):

	global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding

	if e.sender_id == ADMIN:

		if e.data == b"back":

			Getter, Number, TempClient = None, None, None

			await e.edit("**ðŸ¤– Pannello Raspa Bot\n\nâš™ Versione Â» 2.1**", buttons=[[Button.inline("ðŸ“ž Voip", "voip")], [Button.inline("ðŸ‘¥ Ruba", "grab"), Button.inline("âœ” Raspa", "add")]])

		elif e.data == b"stop":

			await e.edit("**âœ… Aggiunta Interrotta âœ…**", buttons=[Button.inline("ðŸ”™ Indietro", "back")])

			python = sys.executable

			os.execl(python, python, *sys.argv)

		elif inAdding:

			await e.answer("âŒÂ» Questa sezione Ã¨ bloccata durante l' aggiunta membri!", alert=True)

		elif e.data == b"voip":

			Getter, Number, TempClient = None, None, None

			await e.edit(f"__ðŸ“ž Voip Aggiunti Â»__ **{SSs.__len__()}**", buttons=[[Button.inline("âž• Aggiungi", "addvoip"), Button.inline("ðŸ”§ Gestisci", "voips")], [Button.inline("ðŸ“ Archiviati", "arch")], [Button.inline("ðŸ”™ Indietro", "back")]])

		elif e.data == b"addvoip":

			Getter = 0

			await e.edit("**â˜Žï¸ Inserisci il numero del voip che desideri aggiungere â˜Žï¸**", buttons=[Button.inline("âŒ Annulla", "voip")])

		elif e.data == b"voips":

			if SSs.__len__() > 0:

				Getter = 3

				msg = "__â˜Žï¸ Invia il numero del voip che vuoi gestire__\n\n**LISTA VOIP**"

				for n in SSs:

					msg += f"\n`{n}`"

				await e.edit(msg, buttons=[Button.inline("âŒ Annulla", "voip")])

			else:

				await e.edit("**âŒ Non hai aggiunto nessun voip âŒ**", buttons=[[Button.inline("âž• Aggiungi", "addvoip")], [Button.inline("ðŸ”™ Indietro", "voip")]])

		elif e.data == b"arch":

			if ArchSSs.__len__() > 0:

				Getter = 4

				msg = f"__ðŸ“ Voip Archiviati Â»__ **{ArchSSs.__len__()}**\n\n__â˜Žï¸ Invia il numero del voip archiviato che vuoi gestire__\n\n**LISTA VOIP ARCHIVIATI**"

				for n in ArchSSs:

					msg += f"\n`{n}`"

				await e.edit(msg, buttons=[Button.inline("âŒ Annulla", "voip")])

			else:

				await e.edit("**âŒ Non hai archiviato nessun voip âŒ**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

		elif e.data == b"grab":

			if Grab == None:

				await e.edit("**âŒ Gruppo Non Impostato âŒ\n\nâ„¹ï¸ Puoi impostarlo usando il bottone qui sotto!**", buttons=[[Button.inline("âœðŸ» Imposta", "setgrab")], [Button.inline("ðŸ”™ Indietro", "back")]])

			else:

				await e.edit(f"__ðŸ‘¥ Gruppo impostato Â»__ **{Grab}**", buttons=[[Button.inline("âœðŸ» Modifica", "setgrab")], [Button.inline("ðŸ”™ Indietro", "back")]])

		elif e.data == b"setgrab":

			Getter = 5

			await e.edit("__ðŸ‘¥ Invia la @ o il link del gruppo da cui vuoi rubare gli utenti!__", buttons=[Button.inline("âŒ Annulla", "back")])

		elif e.data == b"add":

			if SSs.__len__() > 0:

				if Grab != None:

					Getter = 6

					await e.edit("__âž• Invia la @ o il link del gruppo in cui vuoi aggiungere gli utenti!__", buttons=[Button.inline("âŒ Annulla", "back")])

				else:

					await e.edit("**âŒ Impostare il gruppo da cui rubare gli utenti âŒ**", buttons=[[Button.inline("ðŸ‘¥ Ruba", "grab")], [Button.inline("ðŸ”™ Indietro", "back")]])

			else:

				await e.edit("**âŒ Non hai aggiunto nessun voip âŒ**", buttons=[[Button.inline("âž• Aggiungi", "addvoip")], [Button.inline("ðŸ”™ Indietro", "back")]])

		else:

			st = e.data.decode().split(";")

			if st[0] == "arch":

				if st[1] in SSs:

					if not st[1] in ArchSSs:

						ArchSSs[st[1]] = SSs[st[1]]

						saveArchSS()

					del(SSs[st[1]])

					saveSS()

					await e.edit("**âœ… Voip Archiviato Correttamente âœ…**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

				else:

					await e.edit("**âŒ Voip Non Trovato âŒ**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

			elif st[0] == "add":

				if st[1] in ArchSSs:

					SSs[st[1]] = ArchSSs[st[1]]

					saveSS()

					del(ArchSSs[st[1]])

					saveArchSS()

					await e.edit("**âœ… Voip Riaggiunto Correttamente âœ…**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

				else:

					await e.edit("**âŒ Voip Non Trovato âŒ**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

			elif st[0] == "del":

				if st[1] in SSs:

					CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)

					await CClient.connect()

					try:

						me = await CClient.get_me()

						if me != None:

							async with CClient as client:

								await client.log_out()

					except:

						pass

					del(SSs[st[1]])

					saveSS()

					await e.edit("**âœ… Voip Rimosso Correttamente âœ…**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

				else:

					await e.edit("**âŒ Voip GiÃ  Rimosso âŒ**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

			elif st[0] == "delarch":

				if st[1] in ArchSSs:

					CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)

					await CClient.connect()

					try:

						me = await CClient.get_me()

						if me != None:

							async with CClient as client:

								await client.log_out()

					except:

						pass

					del(ArchSSs[st[1]])

					saveArchSS()

					await e.edit("**âœ… Voip Rimosso Correttamente âœ…**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

				else:

					await e.edit("**âŒ Voip GiÃ  Rimosso âŒ**", buttons=[Button.inline("ðŸ”™ Indietro", "voip")])

			elif st[0] == "info":

				await e.answer(f"â„¹ï¸ L' errore Ã¨ avvenuto nel seguente voip Â» {st[1]} â„¹ï¸")

			

		

	

print("mi raccomando, inserisci il token del bot..")

bot.start()

bot.run_until_disconnected()
