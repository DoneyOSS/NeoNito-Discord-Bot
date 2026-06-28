from tinydb import TinyDB, Query

db = TinyDB('servers.json')
servers = Query()

def serverInfo(serId: int, lang: str = None, prefix: str = None):
    # check it or sm
    serverCheck = db.get(servers.id == serId)

    # new servers typa logic or sm
    if not serverCheck:
        # db shit 
        dataStructure = {
            'id': serId,
            'prefix': prefix if prefix is not None else "-",
            'lang': lang if lang is not None else "en"
        }

        db.insert(dataStructure)
        return dataStructure

    # old servers logic thingy
    update = {}
    if lang is not None:
        update['lang'] = lang
    if prefix is not None:
        update['prefix'] = prefix
    
    if update:
        db.update(update, servers.id == serId)
        serverCheck = db.get(servers.id == serId)

    return serverCheck