import pickle, datetime, json, traceback
from datetime import date, time
from trawlers import c3abn, ctbn, cchurchchannel, chope, ctct, cword, clocatetv, csky, ctytv, cbetv, cfirstlight, charvest, cpress, csubha, cfilmon


def add_ordinal(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))


days = []
days_js = []

def update_days():
	today = datetime.date.today()

	for d in range(7):
		days.append(today + datetime.timedelta(days=d))

	for d in days:
		human = add_ordinal(d.day)
		human += d.strftime(" %b")

		entry = {"date": d.strftime("%Y-%m-%d"), "day": d.strftime("%A"), "human_date": human}
		days_js.append(entry)


schedules = {}

def update_schedules():
	global schedules


	# charvest.TrawlerHarvest.get_info_for_week()
	# return

	try:
		schedules.update({"46": ctbn.TrawlerTBN.get_info_for_days(days)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"47": cchurchchannel.TrawlerChurchChannel.get_info_for_days(days)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"48": clocatetv.TrawlerLocateTV.get_info_for_days(days, "smile-of-a-child-network")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"49": clocatetv.TrawlerLocateTV.get_info_for_days(days, "jc-tv")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"50": c3abn.Trawler3ABN.get_info_for_days(days)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"51": c3abn.Trawler3ABN.get_info_for_days(days, abn_network_id=5)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"52": c3abn.Trawler3ABN.get_info_for_days(days, abn_network_id=7)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"53": c3abn.Trawler3ABN.get_info_for_days(days, abn_network_id=6)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"54": clocatetv.TrawlerLocateTV.get_info_for_days(days, "daystar-television-network")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"56": clocatetv.TrawlerLocateTV.get_info_for_days(days, "hope-channel")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"57": cword.TrawlerWord.get_info_for_week(date.today())})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"58": clocatetv.TrawlerLocateTV.get_info_for_days(days, "nrb-network")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"59": clocatetv.TrawlerLocateTV.get_info_for_days(days, "loma-linda-llbn")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"60": clocatetv.TrawlerLocateTV.get_info_for_days(days, "cornerstone-television")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"61": ctct.TrawlerTCT.get_info_for_week("tct")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"62": ctct.TrawlerTCT.get_info_for_week("tct-kids")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"63": ctct.TrawlerTCT.get_info_for_week("tct-family")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"64": ctytv.TrawlerTY.get_info_for_week()})
	except Exception,e:
		traceback.print_exc()
		pass

		print "did tytv"

	try:
		schedules.update({"67": cfirstlight.TrawlerFirstlight.get_info_for_days(days)})
	except Exception,e:
		traceback.print_exc()
		pass

	print "did firstlight"

	try:
		schedules.update({"72": clocatetv.TrawlerLocateTV.get_info_for_days(days, "gospel-broadcasting-network")})
	except Exception,e:
		traceback.print_exc()
		pass


	try:
		schedules.update({"74": csky.TrawlerSky.get_info_for_days(days, 585)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"77": clocatetv.TrawlerLocateTV.get_info_for_days(days, "enlace")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"80": clocatetv.TrawlerLocateTV.get_info_for_days(days, "newsmax-tv")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"85": clocatetv.TrawlerLocateTV.get_info_for_days(days, "safe-tv")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"86": clocatetv.TrawlerLocateTV.get_info_for_days(days, "russia-today")})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"92": csky.TrawlerSky.get_info_for_days(days, 580)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"100": csky.TrawlerSky.get_info_for_days(days, 594)})
	except Exception,e:
		traceback.print_exc()
		pass


	try:
		schedules.update({"101": charvest.TrawlerHarvest.get_info_for_week()})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"112": clocatetv.TrawlerLocateTV.get_info_for_days(days, "wtgl")})
	except Exception,e:
		traceback.print_exc()
		pass


	try:
		schedules.update({"123": clocatetv.TrawlerLocateTV.get_info_for_days(days, "family-friendly-entertainment")})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"129": clocatetv.TrawlerLocateTV.get_info_for_days(days, "kchf")})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"140": csubha.TrawlerSubha.get_info_for_week()})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"163": clocatetv.TrawlerLocateTV.get_info_for_days(days, "impact-network")})
	except Exception,e:
		traceback.print_exc()
		pass

		
		
	try:
		schedules.update({"105": clocatetv.TrawlerLocateTV.get_info_for_days(days, "kazq")})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"119": clocatetv.TrawlerLocateTV.get_info_for_days(days, "wgn-local-chicago-cw")})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"110": clocatetv.TrawlerLocateTV.get_info_for_days(days, "golden-eagle-broadcasting")})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"139": cpress.TrawlerPress.get_info_for_days(days)})
	except Exception,e:
		traceback.print_exc()
		pass



	try:
		schedules.update({"150": clocatetv.TrawlerLocateTV.get_info_for_days(days, "jewish-life-tv")})
	except Exception,e:
		traceback.print_exc()
		pass




	try:
		schedules.update({"155": cfilmon.TrawlerFilmon.get_info_for_week(2945)})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"161": cfilmon.TrawlerFilmon.get_info_for_week(793)})
	except Exception,e:
		traceback.print_exc()
		pass



	try:
		schedules.update({"180": clocatetv.TrawlerLocateTV.get_info_for_days(days, "total-living-network")})
	except Exception,e:
		traceback.print_exc()
		pass


	try:
		schedules.update({"200": csky.TrawlerSky.get_info_for_days(days, 595)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"201": csky.TrawlerSky.get_info_for_days(days, 587)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"205": csky.TrawlerSky.get_info_for_days(days, 586)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"206": csky.TrawlerSky.get_info_for_days(days, 592)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"207": csky.TrawlerSky.get_info_for_days(days, 581)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		pass
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"214": clocatetv.TrawlerLocateTV.get_info_for_days(days, "christian-television-network")})
	except Exception,e:
		traceback.print_exc()
		pass

	try:
		schedules.update({"216": cbetv.TrawlerBE.get_info_for_days(days)})
	except Exception,e:
		traceback.print_exc()
		pass
	try:
		schedules.update({"217": clocatetv.TrawlerLocateTV.get_info_for_days(days, "smart-lifestyle-tv")})
	except Exception,e:
		traceback.print_exc()
		pass





	# schedules.update({"56": chope.TrawlerHope.get_info_for_days(days)})
	# schedules.update({"54": csky.TrawlerSky.get_info_for_days(days, 583)})

update_days()
update_schedules()

day_data = {"days": days, "days_js": days_js}

with open('./cache/days.pickle', 'wb+') as days_dump_handle:
	pickle.dump(day_data, days_dump_handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./cache/schedule.pickle', 'wb+') as sched_dump_handle:
	pickle.dump(schedules, sched_dump_handle, protocol=pickle.HIGHEST_PROTOCOL)
